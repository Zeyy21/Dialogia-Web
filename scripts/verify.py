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
conference_info = json.loads((root / 'source/conference-info.json').read_text())
booklets = json.loads((root / 'source/booklets.json').read_text())
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
    booklet_hash = hashlib.sha256(booklet.read_bytes()).hexdigest()
    assert booklet_hash == booklets[lang]['sha256'], f'Official {lang} file was modified'
    paragraphs = read_booklet(booklet)
    assert sources[lang] == source_passages(paragraphs, lang), f'{lang} DOCX/source mismatch'
    assert normalized(conference_info[lang]['attendance']) in normalized(' '.join(paragraphs[:7])), f'Missing {lang} cover attendance'
    language = doc.xpath(f'//*[@data-language="{lang}"]')[0]
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
    assert len(papers)==24, f'Expected all 24 abstracts in {lang}'
    assert [len(axis.xpath('.//details[@class="paper"]')) for axis in language.xpath('.//details[@class="abstract-axis"]')] == [5, 6, 5, 8]
    assert 'Wassim Salman' not in language.text_content(), 'Outdated speaker spelling'
    for name in ['Gilles Bibeau', 'Roselyne Mavungu', 'Jean-François Roussel', 'Sultan Al Hosani']:
        assert name in language.text_content(), f'Missing participant: {name}'
    lyse = [paper for paper in papers if 'Lyse Langlois' in paper.xpath('./summary')[0].text_content()]
    assert len(lyse) == 1 and len(lyse[0].xpath('./div/p')) == 3, 'Incomplete Lyse Langlois abstract'
    assert len(language.xpath('.//details[@class="day"]')) == 3
    assert len(language.xpath('.//details[@class="session"]')) == 8
    for link in language.xpath('.//a[contains(@href,"/documents/")]'):
        url = urlsplit(link.attrib['href'])
        assert url.path == booklets[lang]['path'], f'Wrong language or superseded booklet linked in {lang}'
        assert parse_qs(url.query).get('v') == [booklet_hash[:12]], 'Stale booklet cache version'
        assert 'download' in link.attrib, 'Booklet link should download the official Word file'
    overview_links = language.xpath('.//a[@data-open-details]')
    assert len(overview_links) == 2, 'Missing programme navigation buttons'
    assert all(a.attrib['href'] == f'#overview-{lang}' and a.attrib['data-open-details'] == f'overview-{lang}' for a in overview_links)
    assert not language.xpath('.//a[contains(@href,".pdf")]'), 'Superseded PDF is still linked'

# Preserve language-specific wording while checking shared timings and speakers.
timings = {}
authors = {}
for lang in ['fr', 'en']:
    programme = doc.xpath(f'//*[@id="program-{lang}"]')[0].text_content()
    timings[lang] = [re.sub(r'\s+', '', t).lower() for t in re.findall(r'\b\d{1,2}\s*[hH]\s*\d{2}', programme)]
    authors[lang] = [re.split(r' · |, PhD|\. Centre', node.text_content())[0].strip() for node in doc.xpath(f'//*[@data-language="{lang}"]//*[@class="paper-author"]')]
assert timings['fr'] == timings['en'], 'French and English programme times differ'
assert authors['fr'] == authors['en'], 'French and English abstract authors differ'
assert len({item['id'] for item in institutions}) == len(institutions), 'Duplicate institution'
assert 'ulaval' in {item['id'] for item in institutions}
assert 'vechta' not in {item['id'] for item in institutions}, 'Institution absent from the final booklet'
assert next(item for item in institutions if item['id'] == 'trends')['name'] == {'en': 'TRENDS Group', 'fr': 'TRENDS Group'}
config = json.loads((root/'registration.json').read_text())
if config['url']:
    assert all(a.attrib['href'] == config['url'] for a in doc.xpath('//*[@data-registration]'))
print(f'PASS: {len(passages)} displayed passages match the bilingual source text exactly.')
print('PASS: Every substantive booklet passage is on the page, including 24 abstracts per language.')
print('PASS: Both programmes and abstracts match their revised official DOCX; times and authors agree.')
print('PASS: Downloads use unchanged language-matched Word originals; programme buttons open the website overview.')
print('PASS: Internal links, booklet links, unique IDs and local assets.')
print(f'PASS: All {len(institutions)} represented institutions, header logos, supplied conference information and footer credit.')
print('Registration:', 'connected' if config['url'] else 'awaiting Google sign-in')
for lang in ['EN','FR']:
    file = root / f'dist/documents/DIALOGIA-2026-{lang}.docx'
    print(f'{lang} booklet SHA-256: {hashlib.sha256(file.read_bytes()).hexdigest()}')
