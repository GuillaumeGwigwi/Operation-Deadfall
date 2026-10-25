"""Download and extract the publisher's freely distributed public-play guide."""
import hashlib
import json
from pathlib import Path
import urllib.request
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://media.wizards.com/2025/wpn/w35/wpn_dnd_heroes-borderlands-play-guide.pdf'
raw = ROOT / 'raw/prequel-public/heroes-of-the-borderlands/public-play-guide.pdf'
out = ROOT / 'references/prequel-public/heroes-of-the-borderlands/public-play-guide.txt'
request = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(request, timeout=40) as response:
    body = response.read()
assert body.startswith(b'%PDF-'), 'Response is not a PDF'
raw.parent.mkdir(parents=True, exist_ok=True)
raw.write_bytes(body)
reader = PdfReader(raw)
assert not reader.is_encrypted, 'Encrypted PDF; stop'
pages = [page.extract_text() or '' for page in reader.pages]
assert all(page.strip() for page in pages), 'Empty text page; OCR review required'
text = '\n\n'.join(f'--- PAGE {i} ---\n{page}' for i, page in enumerate(pages, 1))
assert 'BORDERLANDS' in text.upper(), 'Unexpected document'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('SOURCE: ' + URL + '\nSCOPE: Public play guidance only. NOT the adventure book.\n\n' + text, encoding='utf-8')
record = {'url': URL, 'scope': 'Official freely distributed public-play guidance, not adventure text', 'raw': str(raw.relative_to(ROOT)), 'extracted': str(out.relative_to(ROOT)), 'page_count': len(pages), 'page_text_chars': [len(p) for p in pages], 'sha256': hashlib.sha256(body).hexdigest()}
manifest = ROOT / 'references/prequel-public/public-play-guide-manifest.json'
manifest.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps(record))
