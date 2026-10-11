#!/usr/bin/env python3
"""Batch import local user-supplied HTML files; never crawl the source website."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlparse, urlunparse, unquote

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_source import import_html, render_markdown, safe_name, write_json

DEFAULT_BASE = 'https://www.dndbeyond.com/sources/dnd/aud/'


def slug_for_input(path):
    stem = safe_name(path.stem)
    return re.sub(r'^chapter-(\d+)(?=-|$)', lambda match: 'chapter-' + match[1].zfill(2), stem, flags=re.I)


def input_order(path):
    slug = slug_for_input(path).lower()
    priority = 0 if slug.startswith('introduction') else 1 if slug.startswith('chapter-') else 2 if slug.startswith('appendix-') else 3
    return priority, slug


def infer_source(soup, path, overrides) -> tuple[str, str]:
    override = overrides.get(path.name)
    canonical = soup.select_one('link[rel="canonical"][href]')
    if override:
        return str(override), 'explicit-map'
    if canonical:
        return str(canonical['href']), 'html-canonical'
    title = soup.find('h1')
    text = title.get_text(' ', strip=True) if title else path.stem
    chapter = re.match(r'Chapter\s+(\d+)\s*:\s*(.+)', text, re.I)
    if chapter:
        name = 'chapter-' + str(int(chapter[1])) + '-' + re.sub(r'[^a-z0-9]+', '-', chapter[2].lower()).strip('-')
    elif re.match(r'Appendix\s+[A-Z]\s*:', text, re.I):
        name = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    else:
        name = re.sub(r'^chapter-0+(\d+)', r'chapter-\1', path.stem)
    return DEFAULT_BASE + name, 'inferred-not-fetched'


def collect_entries(root):
    nodes = list(root.children)
    entries = []
    for index, node in enumerate(nodes):
        if getattr(node, 'name', None) not in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            continue
        level = int(node.name[1])
        end = index + 1
        while end < len(nodes):
            tag = nodes[end]
            if getattr(tag, 'name', None) in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and int(tag.name[1]) <= level:
                break
            end += 1
        entries.append({'anchor': node.get('id', ''), 'title': node.get_text(' ', strip=True), 'level': level, 'html': ''.join(str(n) for n in nodes[index:end])})
    return entries


def relink_imports(output, pages):
    """Rewrite links only to imported pages and anchors actually present locally."""
    known = {page['source_url'].split('#')[0].rstrip('/'): page for page in pages}
    rewritten = 0
    for page in pages:
        chapter = output / page['directory']
        files = [chapter / 'chapter.html'] + list(chapter.rglob('*.md'))
        for path in files:
            text = path.read_text(encoding='utf-8')
            for url, target in known.items():
                pattern = re.compile(re.escape(url) + r'(?P<fragment>#[A-Za-z0-9_.%:-]+)?(?=[)\s"<>]|$)')
                def replace(match):
                    nonlocal rewritten
                    fragment = match.group('fragment') or ''
                    if fragment and fragment[1:] not in target['anchors']:
                        return match.group(0)
                    suffix = 'chapter.html' if path.suffix == '.html' else 'chapter.md'
                    destination = output / target['directory'] / suffix
                    rewritten += 1
                    return os.path.relpath(destination, path.parent) + fragment
                text = pattern.sub(replace, text)
            path.write_text(text, encoding='utf-8')
    return rewritten


def import_directory(input_directory, output, download=False, source_map=None):
    input_directory, output = Path(input_directory).resolve(), Path(output).resolve()
    if not input_directory.is_dir():
        raise ValueError('Input directory does not exist: ' + str(input_directory))
    files = sorted([p for p in input_directory.iterdir() if p.is_file() and p.suffix.lower() in ('.html', '.htm')], key=input_order)
    output.mkdir(parents=True, exist_ok=True)
    overrides = source_map or {}
    items, pages, catalog = [], [], []
    used = set()
    for source in files:
        record: dict[str, Any] = {'input': str(source), 'status': 'pending'}
        try:
            raw_bytes = source.read_bytes()
            raw = raw_bytes.decode('utf-8')
            if not raw.strip():
                record.update(status='skipped', reason='Empty file; waiting for supplied content')
                items.append(record)
                continue
            soup = BeautifulSoup(raw, 'html.parser')
            root = soup.select_one('.p-article-content')
            if root is None:
                raise ValueError('No .p-article-content element. Save the article HTML or a full page containing it.')
            source_url, provenance = infer_source(soup, source, overrides)
            parsed_url = urlparse(source_url)
            if parsed_url.scheme != 'https' or parsed_url.hostname != 'www.dndbeyond.com':
                raise ValueError('Reference URL must be an HTTPS URL on www.dndbeyond.com')
            source_url = urlunparse(parsed_url._replace(fragment='', query='')).rstrip('/')
            slug = slug_for_input(source)
            chapter = output / 'chapters' / slug
            digest = hashlib.sha256(raw_bytes).hexdigest()
            original = chapter / 'original.html'
            if original.exists() and original.read_bytes().replace(b'\r\n', b'\n') != raw_bytes.replace(b'\r\n', b'\n'):
                chapter = output / 'chapters' / (slug + '-rev-' + digest[:12])
            if chapter in used:
                raise ValueError('Filename collision after normalization; rename one input file')
            used.add(chapter)
            manifest = import_html(source, chapter, source_url, download=download)
            if manifest['source_sha256'] != digest or source.read_bytes() != raw_bytes:
                raise ValueError('Input changed during import; rerun once the file has finished saving')
            local = BeautifulSoup((chapter / 'chapter.html').read_text(encoding='utf-8'), 'html.parser').select_one('.p-article-content')
            expected = BeautifulSoup(str(root), 'html.parser')
            for tag in expected.select('script,style,select,iframe,object,embed,base,link,meta'):
                tag.decompose()
            if local is None or expected.get_text(' ', strip=True) != local.get_text(' ', strip=True):
                raise ValueError('Text preservation check failed')
            entries = collect_entries(root)
            for number, entry in enumerate(entries, 1):
                filename = f'{number:03d}-' + safe_name(entry['anchor'] or entry['title']) + '.md'
                destination = chapter / 'entries' / filename
                render_markdown(entry['html'], destination, chapter, manifest['assets'], source_url)
                catalog.append({'chapter': manifest['title'], 'title': entry['title'], 'anchor': entry['anchor'], 'level': entry['level'], 'path': str(destination.relative_to(output)), 'source_url': source_url + ('#' + entry['anchor'] if entry['anchor'] else '')})
            directory = str(chapter.relative_to(output))
            page = {'directory': directory, 'source_url': source_url, 'title': manifest['title'], 'anchors': [t['id'] for t in root.select('[id]')]}
            pages.append(page)
            record.update(status='imported', directory=directory, title=manifest['title'], source_url=source_url, url_provenance=provenance, counts=manifest['counts'], entries=len(entries), source_sha256=digest, text_verified=True, image_errors=[a for a in manifest['assets'] if a['status'] == 'error'])
            record['images_pending'] = [a['url'] for a in manifest['assets'] if a['status'] == 'not_downloaded']
            record['link_warnings'] = [{'href': str(a['href']), 'reason': 'Anchor absent in the supplied original HTML; preserved without guessing a replacement'} for a in root.select('a[href]') if str(a['href']).startswith('#') and str(a['href']) != '#' and unquote(str(a['href'])[1:]) not in page['anchors']]
            print('Imported:', source.name, '->', directory, flush=True)
        except Exception as error:
            record.update(status='error', reason=str(error))
            print('ERROR:', source.name, str(error), flush=True)
        items.append(record)
    rewritten = relink_imports(output, pages)
    totals = {'inputs': len(files), 'imported': sum(i['status'] == 'imported' for i in items), 'skipped': sum(i['status'] == 'skipped' for i in items), 'errors': sum(i['status'] == 'error' for i in items), 'image_errors': sum(len(i.get('image_errors', [])) for i in items), 'catalog_entries': len(catalog), 'rewritten_local_links': rewritten}
    totals.update(images_pending=sum(len(i.get('images_pending', [])) for i in items), link_warnings=sum(len(i.get('link_warnings', [])) for i in items), assets=sum(i.get('counts', {}).get('assets', 0) for i in items), tables=sum(i.get('counts', {}).get('tables', 0) for i in items))
    report = {'input_directory': str(input_directory), 'output_directory': str(output), 'download_images': download, 'counts': totals, 'files': items, 'scope': 'Only locally supplied HTML; source pages and linked stat blocks are never fetched'}
    write_json(output / 'import-report.json', report)
    write_json(output / 'catalog.json', catalog)
    write_json(output / 'pages.json', pages)
    lines = ['# Index des ressources locales — MJ', '', 'Secrets et contenus du livre : usage local privé.', '', '## Pages importées']
    html_links = []
    for page in pages:
        lines.append('- [' + page['title'] + '](' + page['directory'] + '/README.md) — [HTML](' + page['directory'] + '/chapter.html)')
        html_links.append('<li><a href="' + html.escape(page['directory'] + '/chapter.html', quote=True) + '">' + html.escape(page['title']) + '</a></li>')
    lines += ['', '## Suivi', '', '- [Rapport d’import](import-report.json)', '- [Catalogue des rubriques](catalog.json)', '', 'Fichiers vides : ' + str(totals['skipped']) + '. Erreurs : ' + str(totals['errors']) + '. Erreurs images : ' + str(totals['image_errors']) + '.']
    lines += ['', 'Images restant à récupérer : ' + str(totals['images_pending']) + '. Liens vers des ancres absentes du HTML original : ' + str(totals['link_warnings']) + '. Voir le rapport pour les références exactes.']
    (output / 'INDEX.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    page_html = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Operation Deadfall — Ressources MJ</title><style>body{max-width:900px;margin:3em auto;padding:1em;font:18px/1.6 system-ui}</style></head><body><h1>Operation Deadfall — Ressources MJ</h1><p>Contient des spoilers. Usage local privé.</p><ul>' + ''.join(html_links) + '</ul><p>Consulter import-report.json pour les fichiers vides et les erreurs.</p></body></html>'
    (output / 'index.html').write_text(page_html, encoding='utf-8')
    return report


def main():
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=default_root / 'raw')
    parser.add_argument('--output', type=Path, default=default_root)
    parser.add_argument('--source-map', type=Path, help='Optional JSON mapping input filenames to exact reference URLs')
    parser.add_argument('--download-images', action='store_true', help='Explicitly download linked CDN images; no source pages are fetched')
    args = parser.parse_args()
    mapping = json.loads(args.source_map.read_text(encoding='utf-8')) if args.source_map else {}
    report = import_directory(args.input, args.output, download=args.download_images, source_map=mapping)
    print(json.dumps(report['counts'], ensure_ascii=False, indent=2))
    if report['counts']['errors'] or report['counts']['image_errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
