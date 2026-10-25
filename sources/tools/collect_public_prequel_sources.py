"""Archive public official overviews only; never fetch paid book chapters."""
import hashlib
import json
from pathlib import Path
import urllib.request
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ('heroes-of-the-borderlands', 'contents', 'https://www.dndbeyond.com/sources/dnd/hotb'),
    ('heroes-of-the-borderlands', 'official-overview', 'https://www.dndbeyond.com/posts/2031-what-is-heroes-of-the-borderlands-your-gateway-to'),
    ('dragon-delves', 'contents', 'https://www.dndbeyond.com/sources/dnd/drde'),
    ('dragon-delves', 'official-product', 'https://wpn.wizards.com/en/products/dragon-delves'),
]

def main():
    records = []
    for book, slug, url in PAGES:
        record: dict = {'book': book, 'slug': slug, 'url': url, 'scope': 'public overview or contents, NOT full adventure text'}
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=40) as response:
                body = response.read()
                record.update(status=response.status, final_url=response.url)
            soup = BeautifulSoup(body, 'html.parser')
            title = soup.title.get_text(' ', strip=True) if soup.title else ''
            if any(x in title.lower() for x in ('just a moment', 'access denied', 'sign in')):
                raise ValueError('Access barrier: ' + title)
            container = soup.select_one('.p-article-content') or soup.select_one('main')
            if container is None:
                raise ValueError('No article or main content found; not archiving a shell')
            for element in container.select('script, style, nav, noscript'):
                element.decompose()
            text = container.get_text('\n', strip=True)
            if len(text) < 200:
                raise ValueError('Insufficient readable public content')
            raw_dir = ROOT / 'raw' / 'prequel-public' / book
            out_dir = ROOT / 'references' / 'prequel-public' / book
            raw_dir.mkdir(parents=True, exist_ok=True)
            out_dir.mkdir(parents=True, exist_ok=True)
            raw_path = raw_dir / (slug + '.html')
            text_path = out_dir / (slug + '.txt')
            raw_path.write_bytes(body)
            text_path.write_text('SOURCE: ' + url + '\nSCOPE: Public overview or contents only; not a complete book.\n\n' + text + '\n', encoding='utf-8')
            pdfs = [{'text': a.get_text(' ', strip=True), 'href': a['href']} for a in soup.select('a[href]') if '.pdf' in str(a['href']).lower()]
            record.update(title=title, raw=str(raw_path.relative_to(ROOT)), extracted=str(text_path.relative_to(ROOT)), bytes=len(body), text_chars=len(text), sha256=hashlib.sha256(body).hexdigest(), pdf_links=pdfs)
        except Exception as exc:
            record['error'] = str(exc)
        records.append(record)
        print(json.dumps(record, ensure_ascii=False))
    manifest = ROOT / 'references' / 'prequel-public' / 'manifest.json'
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({'scope': 'Public official reference material only. Full books not acquired.', 'sources': records}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if not any('extracted' in record for record in records):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
