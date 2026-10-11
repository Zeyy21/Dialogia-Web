"""Import supplied French and English official booklets as unchanged downloads.

DOCX imports also replace the website text; PDF imports preserve the curated
website text, which may include subsequent organiser corrections.

Usage: python3 scripts/import_booklets.py --fr /path/to/fr.pdf --en /path/to/en.pdf
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
manifest_path = ROOT / 'source/booklets.json'
previous_manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
imports = []
for lang in ['fr', 'en']:
    original = getattr(args, lang)
    extension = original.suffix.lower()
    if extension not in {'.docx', '.pdf'}:
        parser.error(f'{original}: expected a PDF or DOCX booklet')
    contents = original.read_bytes()
    if extension == '.pdf' and not contents.startswith(b'%PDF-'):
        parser.error(f'{original}: missing PDF header')
    passages = (source_passages(read_booklet(original), lang)
                if extension == '.docx' else None)
    imports.append((lang, original, extension, contents, passages))

manifest = {}
for lang, original, extension, contents, passages in imports:
    destination = ROOT / f'dist/documents/DIALOGIA-2026-{lang.upper()}{extension}'
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, destination)
    if passages is not None:
        (ROOT / f'source/{lang}.json').write_text(json.dumps(passages, ensure_ascii=False, indent=2) + '\n')
    manifest[lang] = {
        'original_filename': original.name,
        'path': f'/documents/{destination.name}',
        'sha256': hashlib.sha256(contents).hexdigest(),
    }
    if extension == '.pdf':
        previous = previous_manifest.get(lang, {})
        text_source = previous.get('text_source')
        if text_source is None and Path(previous.get('path', '')).suffix.lower() == '.docx':
            text_source = previous
        if text_source is not None:
            manifest[lang]['text_source'] = text_source
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('Imported both official booklets; downloadable originals are unchanged.')
