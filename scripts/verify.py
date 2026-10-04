"""Check source fidelity, internal links and public assets before publishing."""
from pathlib import Path
from lxml import html
import json
import hashlib
import re
import unicodedata
from pypdf import PdfReader
from urllib.parse import urlsplit, parse_qs

root = Path(__file__).resolve().parents[1]
doc = html.fromstring((root / 'dist/index.html').read_text())
sources = {lang: json.loads((root / f'source/{lang}.json').read_text()) for lang in ['en', 'fr']}
institutions = json.loads((root / 'source/institutions.json').read_text())
conference_info = json.loads((root / 'source/conference-info.json').read_text())
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

booklet = root / 'dist/documents/DIALOGIA-2026-FR.pdf'
booklet_hash = hashlib.sha256(booklet.read_bytes()).hexdigest()
pages = [p.extract_text() or '' for p in PdfReader(booklet).pages]
assert len(pages) == 16, 'Expected the 16-page final French booklet'
assert 'PROGRAMME EN UN COUP' in pages[3], 'The programme PDF link must open the overview'
# Pages 2–15 contain the complete programme and abstracts. Page 1 repeats
# the cover information and adds attendance; page 16 lists institutions.
body = [re.sub(r'^DIALOGIA MONTRÉAL.*\n\d+\s*\n', '', p) for p in pages[1:15]]
french_body = sources['fr'][:7] + sources['fr'][8:]
# Apply the organiser's website corrections to the original print text before
# comparing; the supplied downloadable booklet remains the original edition.
booklet_body = ' '.join(body)
booklet_body = booklet_body.replace('Discussants', 'Discutants').replace(
    'Solange Lefebvre',
    'Roselyne Mavungu — Centre de prévention de la radicalisation menant à la violence (CPRMV) à Montréal',
)
booklet_body = booklet_body.replace(
    'Jean-François Roussel',
    'Jean-François Roussel — Institut d’études religieuses de l’Université de Montréal',
)
booklet_body = booklet_body.replace(
    '15 h 15 – 15 h 45 Discussion générale',
    'Ali Mostafa - UCLY Titre à confirmer prochainement 15 h 15 – 15 h 45 Discussion générale',
)
assert normalized(booklet_body) == normalized(' '.join(french_body)), 'Final French PDF/source mismatch after organiser corrections'
assert normalized(conference_info['fr']['attendance']) in normalized(pages[0]), 'Missing final cover attendance'

for lang in ['fr', 'en']:
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
        assert url.path == '/documents/DIALOGIA-2026-FR.pdf', 'A superseded booklet is still linked'
        assert parse_qs(url.query).get('v') == [booklet_hash[:12]], 'Stale PDF cache version'
        if 'data-program-pdf' in link.attrib:
            assert url.fragment == 'page=4', 'Wrong programme overview page'

# English additions are translations of the final French edition, not a new
# official English PDF. Check the facts most likely to drift between languages.
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
assert not doc.xpath('//a[contains(@href,".docx")]'), 'Old Word download remains'
print('PASS: Every substantive booklet passage is on the page, including 24 abstracts per language.')
print('PASS: French programme and abstracts match the final PDF with organiser corrections; English times and authors agree.')
print('PASS: All booklet links use the final French PDF; programme buttons open page 4.')
print('PASS: Internal links, PDF links, unique IDs and local assets.')
print(f'PASS: All {len(institutions)} represented institutions, header logos, supplied conference information and footer credit.')
print('Registration:', 'connected' if config['url'] else 'awaiting Google sign-in')
for lang in ['EN','FR']:
    file = root / f'dist/documents/DIALOGIA-2026-{lang}.pdf'
    print(f'{lang} booklet SHA-256: {hashlib.sha256(file.read_bytes()).hexdigest()}')
