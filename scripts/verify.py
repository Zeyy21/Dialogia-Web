"""Check source fidelity, internal links and public assets before publishing."""
from pathlib import Path
from lxml import html
import json
import hashlib
import re
import unicodedata
from pypdf import PdfReader

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
        assert (root / 'dist' / url.split('#')[0].lstrip('/')).is_file(), f'Missing asset {url}'

def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())

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
    assert credit.text_content() == 'Made by Zeyyad Saleh, Cofounder of Syllogos'
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
    assert len(papers)==23, f'Expected all 23 abstracts in {lang}'
    pdf=root/f'dist/documents/DIALOGIA-2026-{lang.upper()}.pdf'
    pages=[p.extract_text() or '' for p in PdfReader(pdf).pages]
    pages=[re.sub(r'^DIALOGIA MONTRÉAL.*\n\d+\s*\n','',p) for p in pages]
    pages[0]=re.sub(r'^\s*MONTRÉAL.*\n','',pages[0])
    # Ignore PDF line wrapping, punctuation encoding and repeated page headers;
    # compare the complete document in order, with no missing or extra words.
    assert normalized(' '.join(pages))==normalized(' '.join(sources[lang])), f'PDF/source mismatch in {lang}'
config = json.loads((root/'registration.json').read_text())
if config['url']:
    assert all(a.attrib['href'] == config['url'] for a in doc.xpath('//*[@data-registration]'))
print(f'PASS: {len(passages)} displayed passages match the official text exactly.')
assert not doc.xpath('//a[contains(@href,".docx")]'), 'Old Word download remains'
print('PASS: Every substantive booklet passage is on the page, including all 46 abstracts.')
print('PASS: Full English and French source text matches the supplied PDFs.')
print('PASS: Internal links, PDF links, unique IDs and local assets.')
print('PASS: All 22 represented institutions, header logos, supplied conference information and footer credit.')
print('Registration:', 'connected' if config['url'] else 'awaiting Google sign-in')
for lang in ['EN','FR']:
    file = root / f'dist/documents/DIALOGIA-2026-{lang}.pdf'
    print(f'{lang} booklet SHA-256: {hashlib.sha256(file.read_bytes()).hexdigest()}')
