"""Read the official Word booklets without changing their contents."""
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import re

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
TEXT = f"{{{NS['w']}}}t"
TEXT_NODES = {TEXT, f"{{{NS['w']}}}tab", f"{{{NS['w']}}}br"}


def read_booklet(path):
    with ZipFile(path) as archive:
        document = ET.fromstring(archive.read('word/document.xml'))
    paragraphs = []
    for paragraph in document.findall('./w:body//w:p', NS):
        text = ''.join((node.text or '') if node.tag == TEXT else ' '
                       for node in paragraph.iter()
                       if node.tag in TEXT_NODES)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def source_passages(paragraphs, lang):
    # The first cover repeats the title page. Keep its contents line in the
    # established source position; attendance is shown in conference-info.json.
    start = paragraphs.index(paragraphs[0], 1)
    end = paragraphs.index('INSTITUTIONS PARTICIPANTES' if lang == 'fr'
                           else 'PARTICIPATING INSTITUTIONS')
    body = paragraphs[start:end]
    assert body[7] == 'FORMAT', 'Unexpected title-page structure'
    return body[:7] + [paragraphs[start - 1]] + body[7:]
