"""Check source fidelity, internal links and public assets before publishing."""
from pathlib import Path
from lxml import html
import json
import hashlib

root = Path(__file__).resolve().parents[1]
doc = html.fromstring((root / 'dist/index.html').read_text())
sources = {lang: json.loads((root / f'source/{lang}.json').read_text()) for lang in ['en', 'fr']}
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
        assert (root / 'dist' / url.lstrip('/')).is_file(), f'Missing asset {url}'
for lang in ['fr', 'en']:
    indices = {int(e.attrib['data-source'].split(':')[1]) for e in passages if e.attrib['data-source'].startswith(lang + ':')}
    assert set(range(107,229)).issubset(indices), f'Incomplete detailed program in {lang}'
config = json.loads((root/'registration.json').read_text())
if config['url']:
    assert all(a.attrib['href'] == config['url'] for a in doc.xpath('//*[@data-registration]'))
print(f'PASS: {len(passages)} displayed passages match the official text exactly.')
print('PASS: Both complete detailed programs, internal links, unique IDs and local assets.')
print('Registration:', 'connected' if config['url'] else 'awaiting Google sign-in')
for lang in ['EN','FR']:
    file = root / f'dist/documents/DIALOGIA-2026-{lang}.docx'
    print(f'{lang} booklet SHA-256: {hashlib.sha256(file.read_bytes()).hexdigest()}')
