"""Import supplied French and English DOCX files as downloads and website text.

Usage: python3 scripts/import_booklets.py --fr /path/to/fr.docx --en /path/to/en.docx
Then run render.py and verify.py.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
from booklets import read_booklet, source_passages

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
for lang in ['fr', 'en']:
    parser.add_argument(f'--{lang}', required=True, type=Path)
args = parser.parse_args()
manifest = {}
for lang in ['fr', 'en']:
    original = getattr(args, lang)
    passages = source_passages(read_booklet(original), lang)
    destination = ROOT / f'dist/documents/DIALOGIA-2026-{lang.upper()}.docx'
    shutil.copyfile(original, destination)
    (ROOT / f'source/{lang}.json').write_text(json.dumps(passages, ensure_ascii=False, indent=2) + '\n')
    manifest[lang] = {
        'original_filename': original.name,
        'path': f'/documents/{destination.name}',
        'sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
    }
(ROOT / 'source/booklets.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('Imported both official booklets; downloadable originals are unchanged.')
