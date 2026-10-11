"""Check source fidelity, internal links and public assets before publishing."""
from pathlib import Path
from lxml import html
import json
import hashlib
import re
import unicodedata
from booklets import read_booklet, source_passages
from urllib.parse import urlsplit, parse_qs

root = Path(__file__).resolve().parents[1]
doc = html.fromstring((root / 'dist/index.html').read_text())
sources = {lang: json.loads((root / f'source/{lang}.json').read_text()) for lang in ['en', 'fr']}
institutions = json.loads((root / 'source/institutions.json').read_text())
speakers = json.loads((root / 'source/speakers.json').read_text())
people = speakers['people']
assert len(people) == len({p['id'] for p in people}) == len({p['source_media'] for p in people}) == 30, 'Expected 30 unique speaker portraits'
for person in people:
    portrait = root / 'dist' / person['portrait'].lstrip('/')
    assert hashlib.sha256(portrait.read_bytes()).hexdigest() == person['portrait_sha256'], f'Changed portrait: {person["name"]}'
conference_info = json.loads((root / 'source/conference-info.json').read_text())
booklets = json.loads((root / 'source/booklets.json').read_text())
programme_corrections = json.loads((root / 'source/programme-corrections.json').read_text())
passages = doc.xpath('//*[@data-source]')
for element in passages:
    lang, index = element.attrib['data-source'].split(':')
    assert element.text_content() == sources[lang][int(index)], element.attrib['data-source']
ids = doc.xpath('//@id')
assert len(ids) == len(set(ids)), 'Duplicate HTML IDs'
for url in doc.xpath('//@href | //@src'):
    if url.startswith('#'):
        assert url[1:] in ids, f'Missing anchor {url}'
    elif url.startswith('/'):
        assert (root / 'dist' / urlsplit(url).path.lstrip('/')).is_file(), f'Missing asset {url}'

def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())

for lang in ['fr', 'en']:
    booklet = root / 'dist' / booklets[lang]['path'].lstrip('/')
    booklet_bytes = booklet.read_bytes()
    assert booklet.suffix.lower() == '.pdf' and booklet_bytes.startswith(b'%PDF-'), f'Official {lang} booklet must be a PDF'
    booklet_hash = hashlib.sha256(booklet_bytes).hexdigest()
    assert booklet_hash == booklets[lang]['sha256'], f'Official {lang} file was modified'
    text_source = booklets[lang]['text_source']
    source_booklet = root / 'dist' / text_source['path'].lstrip('/')
    assert hashlib.sha256(source_booklet.read_bytes()).hexdigest() == text_source['sha256'], f'Base {lang} text source was modified'
    paragraphs = read_booklet(source_booklet)
    expected_passages = source_passages(paragraphs, lang)
    for index, replacement in programme_corrections[lang].items():
        assert index.isdecimal() and int(index) < len(expected_passages), f'Invalid {lang} programme correction index: {index}'
        assert isinstance(replacement, str) and replacement.strip(), f'Empty {lang} programme correction: {index}'
        expected_passages[int(index)] = replacement
    assert sources[lang] == expected_passages, f'{lang} base DOCX and approved programme corrections/source mismatch'
    assert normalized(conference_info[lang]['attendance']) in normalized(' '.join(paragraphs[:7])), f'Missing {lang} cover attendance'
    language = doc.xpath(f'//*[@data-language="{lang}"]')[0]
    profiles = language.xpath('.//*[@data-person]')
    assert [profile.attrib['data-person'] for profile in profiles] == [p['id'] for p in people], f'Incomplete speaker gallery in {lang}'
    for profile, person in zip(profiles, people):
        assert profile.xpath('.//h3')[0].text_content() == person['name']
        assert profile.xpath('.//img/@src') == [person['portrait']], f'Portrait/name mismatch: {person["name"]}'
        assert profile.xpath('.//img/@alt') == [person['name']]
        assert profile.xpath('.//*[@class="speaker-affiliation"]')[0].text_content() == person['affiliation'][lang]
        assert profile.xpath('.//*[@class="speaker-roles"]')[0].text_content() == ' · '.join(speakers['roles'][role][lang] for role in person['roles'])
    gallery = language.xpath(f'.//*[@id="speakers-{lang}"]')[0]
    assert gallery.getnext().attrib['id'] == f'international-{lang}', 'Speaker gallery must precede institutions'
    assert language.xpath(f'.//nav[@class="section-nav"]/a[@href="#speakers-{lang}"]'), 'Missing speaker navigation'
    cards = language.xpath('.//*[@data-institution]')
    assert [card.attrib['data-institution'] for card in cards] == [i['id'] for i in institutions], f'Incomplete institution list in {lang}'
    for card, institution in zip(cards, institutions):
        assert card.xpath('.//h4')[0].text_content() == institution['name'][lang]
        assert card.xpath('./a/@href') == [institution['url']]
        assert card.xpath('.//img/@src') == [institution['logo']]
    assert len(language.xpath('.//header//a[@class="organizer-link"]')) == 4, 'Organising logos must be inside the menu bar'
    credit = language.xpath('.//*[@class="footer-credit"]/a')[0]
    assert credit.text_content() == 'Designed by Zeyyad Saleh, Cofounder of Syllogos'
    assert credit.attrib['href'] == 'https://syllogos.io/'
    for key, text in conference_info[lang].items():
        node = language.xpath(f'.//*[@data-conference-info="{lang}:{key}"]')
        assert len(node) == 1 and node[0].text_content() == text, f'Missing or changed conference information: {lang}:{key}'
    indices = {int(e.attrib['data-source'].split(':')[1]) for e in passages if e.attrib['data-source'].startswith(lang + ':')}
    # Cover contents line, repeated Rationale label, and the colour legend in
    # the printed timetable add no information to the corresponding web sections.
    redundant_print_labels = {7, 17, 36, 37, 38, 39, 40}
    required = set(range(len(sources[lang]))) - redundant_print_labels
    assert required.issubset(indices), f'Missing booklet content in {lang}: {required-indices}'
    papers=doc.xpath(f'//*[@data-language="{lang}"]//details[contains(concat(" ",normalize-space(@class)," ")," paper ")]')
    assert len(papers)==25, f'Expected all 25 abstracts in {lang}'
    assert [len(axis.xpath('.//details[@class="paper"]')) for axis in language.xpath('.//details[@class="abstract-axis"]')] == [6, 6, 5, 8]
    jaume = [paper for paper in papers if paper.xpath('./summary//span[@class="paper-author"]')[0].text_content().startswith('Jaume Flaquer Garcia')]
    assert len(jaume) == 1, f'Missing or duplicated Jaume abstract in {lang}'
    assert papers[papers.index(jaume[0]) + 1].xpath('./summary//span[@class="paper-author"]')[0].text_content().startswith('Raphaël Georgy'), f'Jaume abstract must precede Raphaël in {lang}'
    expected_title = ('La prédication à l’épreuve de l’intelligence artificielle' if lang == 'fr'
                      else 'Preaching in the Age of Artificial Intelligence: Challenges and Implications')
    assert jaume[0].xpath('./summary//span[@class="paper-title"]')[0].text_content() == expected_title
    assert len(jaume[0].xpath('./div/p')) == (1 if lang == 'fr' else 4), f'Incomplete Jaume abstract in {lang}'
    session_one = language.xpath('.//details[@class="session"]')[0]
    programme_speakers = [node.text_content() for node in session_one.xpath('.//p[@class="speaker"]')]
    assert sum(name.startswith('Jaume Flaquer Garcia') for name in programme_speakers) == 1
    jaume_position = next(i for i, name in enumerate(programme_speakers) if name.startswith('Jaume Flaquer Garcia'))
    assert programme_speakers[jaume_position + 1].startswith('Raphaël Georgy'), f'Jaume must precede Raphaël in Session 1 in {lang}'
    jaume_programme = session_one.xpath('.//p[@class="speaker" and starts-with(text(),"Jaume Flaquer Garcia")]')[0]
    assert jaume_programme.getnext().text_content() == 'Preaching in the Age of Artificial Intelligence: Challenges and Implications'
    assert 'Wassim Salman' not in language.text_content(), 'Outdated speaker spelling'
    for name in ['Gilles Bibeau', 'Roselyne Mavungu', 'Jean-François Roussel', 'Sultan Al Hosani']:
        assert name in language.text_content(), f'Missing participant: {name}'
    lyse = [paper for paper in papers if 'Lyse Langlois' in paper.xpath('./summary')[0].text_content()]
    assert len(lyse) == 1 and len(lyse[0].xpath('./div/p')) == 3, 'Incomplete Lyse Langlois abstract'
    assert len(language.xpath('.//details[@class="day"]')) == 3
    assert len(language.xpath('.//details[@class="session"]')) == 8
    booklet_links = language.xpath('.//a[contains(@href,"/documents/") or contains(@href,".pdf") or contains(@href,".docx")]')
    assert booklet_links, f'Missing {lang} booklet download links'
    for link in booklet_links:
        url = urlsplit(link.attrib['href'])
        assert url.path == booklets[lang]['path'], f'Wrong language or superseded booklet linked in {lang}'
        assert parse_qs(url.query).get('v') == [booklet_hash[:12]], 'Stale booklet cache version'
        assert 'download' in link.attrib, 'Booklet link should download the official PDF file'
    overview_links = language.xpath('.//a[@data-open-details]')
    assert len(overview_links) == 2, 'Missing programme navigation buttons'
    assert all(a.attrib['href'] == f'#overview-{lang}' and a.attrib['data-open-details'] == f'overview-{lang}' for a in overview_links)

# Preserve language-specific wording while checking shared timings and speakers.
timings = {}
authors = {}
for lang in ['fr', 'en']:
    programme = doc.xpath(f'//*[@id="program-{lang}"]')[0].text_content()
    timings[lang] = [re.sub(r'\s+', '', t).lower() for t in re.findall(r'\b\d{1,2}\s*[hH]\s*\d{2}', programme)]
    authors[lang] = [re.split(r' · |\s*—\s*|, PhD|\. Centre', node.text_content())[0].strip() for node in doc.xpath(f'//*[@data-language="{lang}"]//*[@class="paper-author"]')]
assert timings['fr'] == timings['en'], 'French and English programme times differ'
assert authors['fr'] == authors['en'], 'French and English abstract authors differ'
assert len({item['id'] for item in institutions}) == len(institutions), 'Duplicate institution'
assert 'ulaval' in {item['id'] for item in institutions}
assert 'loyola' in {item['id'] for item in institutions}, 'Missing Universidad Loyola'
assert 'vechta' not in {item['id'] for item in institutions}, 'Institution absent from the final booklet'
assert next(item for item in institutions if item['id'] == 'trends')['name'] == {'en': 'TRENDS Group', 'fr': 'TRENDS Group'}
config = json.loads((root/'registration.json').read_text())
if config['url']:
    assert all(a.attrib['href'] == config['url'] for a in doc.xpath('//*[@data-registration]'))
print(f'PASS: {len(passages)} displayed passages match the bilingual source text exactly.')
print('PASS: Every substantive booklet passage is on the page, including 25 abstracts per language.')
print('PASS: Jaume Flaquer Garcia precedes Raphaël Georgy in both programmes and abstract lists.')
print('PASS: Both programmes and abstracts match the preserved DOCX text plus approved programme corrections; times and authors agree.')
print('PASS: Downloads use unchanged language-matched final PDFs; programme buttons open the website overview.')
print('PASS: Internal links, booklet links, unique IDs and local assets.')
print(f'PASS: All {len(institutions)} represented institutions, header logos, supplied conference information and footer credit.')
print(f'PASS: All {len(people)} unique speaker profiles, bilingual captions and matching portrait hashes.')
print('Registration:', 'connected' if config['url'] else 'awaiting Google sign-in')
for lang in ['EN','FR']:
    file = root / 'dist' / booklets[lang.lower()]['path'].lstrip('/')
    print(f'{lang} booklet SHA-256: {hashlib.sha256(file.read_bytes()).hexdigest()}')
