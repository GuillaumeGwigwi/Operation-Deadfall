#!/usr/bin/env python3
"""Import user-supplied LOCAL D&D Beyond HTML. Never crawl source pages."""
import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse, unquote

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
SOURCE_HOST = 'media.dndbeyond.com'
LOCAL_STATUSES = ('downloaded', 'cached', 'copied')


def safe_name(value):
    return re.sub(r'[^a-zA-Z0-9._-]+', '-', value).strip('.-') or 'untitled'


def absolute_url(value, source_url):
    if value.startswith('#'):
        return value
    if value.startswith('sources/'):
        value = '/' + value
    return urljoin(source_url, value)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


class AnchoredConverter(MarkdownConverter):
    def convert_hN(self, n, el, text, parent_tags):
        result = super().convert_hN(n, el, text, parent_tags)
        identifier = el.get('id')
        if identifier:
            result = '\n\n<a id="' + html.escape(identifier, quote=True) + '"></a>\n' + result
        return result


def clean_fragment(fragment):
    soup = BeautifulSoup(fragment, 'html.parser')
    for tag in soup.select('script,style,select,iframe,object,embed,base,link,meta'):
        tag.decompose()
    for tag in soup.find_all(True):
        tag.attrs.pop('srcset', None)
        for key in list(tag.attrs):
            if key.lower().startswith('on'):
                del tag.attrs[key]
        for key in ('href', 'src'):
            if str(tag.get(key, '')).strip().lower().startswith(('javascript:', 'data:', 'file:')):
                del tag.attrs[key]
    return soup


def render_markdown(fragment, destination, output, assets, source_url):
    soup = clean_fragment(fragment)
    by_url = {asset['url']: asset for asset in assets}
    for tag in soup.select('a[href],img[src]'):
        key = 'src' if tag.name == 'img' else 'href'
        value = tag[key]
        if value.startswith('#'):
            if destination.name != 'chapter.md':
                tag[key] = os.path.relpath(output / 'chapter.md', destination.parent) + value
            continue
        resolved = absolute_url(value, source_url)
        asset = by_url.get(resolved)
        if asset and asset['status'] in LOCAL_STATUSES:
            tag[key] = os.path.relpath(output / asset['path'], destination.parent)
        else:
            tag[key] = resolved
    body = AnchoredConverter(heading_style='ATX', bullets='-', escape_underscores=False).convert(str(soup)).strip()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text('<!-- Notes MJ : contenu fourni par l’utilisateur, non destiné au partage public. -->\n\n' + body + '\n', encoding='utf-8')


def collect_assets(soup, source_url, source=None):
    assets = {}
    for tag in soup.select('img[src],a[href]'):
        value = tag.get('src') if tag.name == 'img' else tag.get('href')
        url = absolute_url(value, source_url)
        parsed = urlparse(url)
        extension = Path(parsed.path).suffix.lower()
        if extension not in IMAGE_EXTENSIONS:
            continue
        supplied_path = urlparse(value)
        is_local = source is not None and not supplied_path.scheme and not supplied_path.netloc and not value.startswith(('/', '#'))
        if not is_local and (parsed.scheme != 'https' or parsed.hostname != SOURCE_HOST):
            continue
        local_path = None
        if is_local:
            assert source is not None
            parent = Path(source).resolve().parent
            local_path = (parent / unquote(supplied_path.path)).resolve()
            if not local_path.is_relative_to(parent):
                raise ValueError('Local image reference escapes the supplied HTML directory')
        if url in assets:
            continue
        filename = safe_name(Path(unquote(parsed.path)).name)
        audience = 'players' if '-player.' in filename else 'mj'
        category = ('maps/players' if audience == 'players' else 'maps/mj') if filename.startswith('map-') else 'illustrations'
        figure = tag.find_parent('figure')
        credit = figure.select_one('.artist-credit') if figure else None
        caption = figure.find('figcaption') if figure else None
        assets[url] = {
            'url': url, 'path': 'assets/' + category + '/' + filename,
            'audience': audience, 'artist': credit.get_text(' ', strip=True) if credit else '',
            'caption': caption.get_text(' ', strip=True) if caption else '',
            'figure_id': figure.get('id', '') if figure else '',
            'status': 'not_downloaded',
            'kind': 'local' if is_local else 'cdn',
        }
        if local_path is not None:
            assets[url]['local_source'] = str(local_path)
    paths = [asset['path'] for asset in assets.values()]
    if len(paths) != len(set(paths)):
        raise ValueError('Different asset URLs would overwrite the same filename')
    return list(assets.values())


def heading_fragments(root, level):
    """Split at top-level h2; retain all source nodes in exactly one fragment."""
    groups = []
    current = {'id': 'Introduction', 'title': 'Introduction', 'html': ''}
    for child in root.children:
        if getattr(child, 'name', None) == level:
            if current['html'].strip():
                groups.append(current)
            current = {'id': child.get('id', safe_name(child.get_text())), 'title': child.get_text(' ', strip=True), 'html': ''}
        current['html'] += str(child)
    if current['html'].strip():
        groups.append(current)
    return groups


def entity_fragments(root):
    category = None
    current = None
    entities = []
    for child in root.children:
        name = getattr(child, 'name', None)
        identifier = child.get('id') if name else None
        boundary = name in ('h1', 'h2', 'h3', 'h4')
        level = int(name[1]) if boundary else 99
        if current and level <= current['level']:
            entities.append(current)
            current = None
        if identifier == 'ZulkirDescriptions':
            category = ('zulkirs', 4)
        elif identifier == 'TharchDescriptions':
            category = ('tharchs', 3)
        elif identifier == 'EltabbarsCity':
            category = ('wards', 4)
        elif category and level < category[1]:
            if identifier not in ('ZulkirDescriptions', 'TharchDescriptions', 'EltabbarsCity'):
                category = None
        if category and level == category[1] and not (child.find_parent('table') if name else False):
            current = {'category': category[0], 'level': level, 'id': identifier or safe_name(child.get_text()), 'title': child.get_text(' ', strip=True), 'html': ''}
        if current:
            current['html'] += str(child)
    if current:
        entities.append(current)
    return entities


def validate_image(data):
    """Reject HTTP interstitials and corrupt image data; record true dimensions."""
    import io
    from PIL import Image
    try:
        with Image.open(io.BytesIO(data)) as image:
            details = {'format': image.format, 'width': image.width, 'height': image.height}
            image.verify()
        return details
    except Exception as error:
        raise ValueError('Response is not a valid image: ' + str(error)) from error


def download_asset(asset, output):
    """No cookies/auth, allowlisted HTTPS only, validated cache, bounded retry."""
    import time
    import urllib.request

    def allowed(url):
        parsed = urlparse(url)
        return parsed.scheme == 'https' and parsed.hostname == SOURCE_HOST and parsed.port in (None, 443) and not parsed.username and not parsed.password

    class SafeRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, response, code, message, headers, newurl):
            if not allowed(newurl):
                raise ValueError('Refusing asset redirect outside the allowlisted HTTPS host')
            return super().redirect_request(request, response, code, message, headers, newurl)

    path = Path(output) / asset['path']
    if not path.resolve().is_relative_to(Path(output).resolve()):
        raise ValueError('Asset path escapes output directory')
    if not allowed(asset['url']):
        raise ValueError('Asset URL is outside the allowlist')
    data = None
    status = 'downloaded'
    if path.exists():
        try:
            data = path.read_bytes()
            validate_image(data)
            status = 'cached'
        except ValueError:
            data = None
    if data is None:
        opener = urllib.request.build_opener(SafeRedirect())
        for attempt in range(3):
            try:
                request = urllib.request.Request(asset['url'], headers={'User-Agent': 'OperationDeadfall-LocalResourceImporter/1.0', 'Accept': 'image/*'})
                with opener.open(request, timeout=40) as response:
                    content_type = response.headers.get('Content-Type', '').split(';')[0].lower()
                    if not content_type.startswith('image/'):
                        raise ValueError('Expected an image Content-Type; got ' + content_type)
                    data = response.read(50 * 1024 * 1024 + 1)
                    if len(data) > 50 * 1024 * 1024:
                        raise ValueError('Asset exceeds the 50 MiB limit')
                    validate_image(data)
                break
            except Exception as error:
                data = None
                asset['error'] = str(error)
                if attempt < 2:
                    time.sleep(attempt + 1)
        if data is None:
            asset['status'] = 'error'
            print('ERROR:', asset['url'], asset['error'], flush=True)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + '.part')
        temporary.write_bytes(data)
        temporary.replace(path)
    asset.update(validate_image(data))
    asset.update({'status': status, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    asset.pop('error', None)
    print(status + ':', asset['path'], len(data), 'bytes', flush=True)


def prepare_asset(asset, output, download):
    """Copy supplied local images, reuse caches, optionally fetch explicit CDN URLs."""
    path = Path(output) / asset['path']
    if not path.resolve().is_relative_to(Path(output).resolve()):
        raise ValueError('Asset path escapes output directory')
    if asset.get('kind') == 'local':
        try:
            data = Path(asset['local_source']).read_bytes()
            details = validate_image(data)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            asset.update(details)
            asset.update(status='copied', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        except (OSError, ValueError) as error:
            asset.update(status='error', error=str(error))
    elif path.exists() and not download:
        try:
            data = path.read_bytes()
            asset.update(validate_image(data))
            asset.update(status='cached', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        except (OSError, ValueError) as error:
            asset.update(status='error', error=str(error))
    elif download:
        download_asset(asset, output)


def import_html(source, output, source_url, download=False):
    source, output = Path(source), Path(output)
    raw_bytes = source.read_bytes()
    raw = raw_bytes.decode('utf-8')
    parsed = BeautifulSoup(raw, 'html.parser')
    root = parsed.select_one('.p-article-content')
    if root is None:
        raise ValueError('Expected a .p-article-content HTML element')
    output.mkdir(parents=True, exist_ok=True)
    original = output / 'original.html'
    if original.exists() and original.read_bytes().replace(b'\r\n', b'\n') != raw_bytes.replace(b'\r\n', b'\n'):
        raise ValueError('Refusing to overwrite a different source; choose a new output directory')
    original.write_bytes(raw_bytes)
    assets = collect_assets(root, source_url, source)
    for asset in assets:
        prepare_asset(asset, output, download)
    sections = heading_fragments(root, 'h2')
    entities = entity_fragments(root)
    links = sorted({absolute_url(a['href'], source_url) for a in root.select('a[href]') if a['href'] and not a['href'].startswith('#')})
    tables = []
    for index, table in enumerate(root.find_all('table'), 1):
        caption = table.find('caption')
        title = caption.get_text(' ', strip=True) if caption else 'Table ' + str(index)
        identifier = table.get('id') or (caption.find(id=True).get('id') if caption and caption.find(id=True) else 'table-' + str(index))
        rows = [[cell.get_text(' ', strip=True) for cell in tr.find_all(['th', 'td'], recursive=False)] for tr in table.find_all('tr')]
        rows = [row for row in rows if row]
        path = output / 'tables' / (f'{index:02d}-' + safe_name(identifier) + '.csv')
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            csv.writer(handle).writerows(rows)
        tables.append({'id': identifier, 'title': title, 'rows': rows, 'csv': str(path.relative_to(output))})
    title_tag = root.find('h1')
    manifest = {
        'source_url': source_url, 'provenance': 'HTML directly supplied by the user; not fetched from D&D Beyond',
        'audience': 'mj', 'title': title_tag.get_text(' ', strip=True) if title_tag else source.stem,
        'source_sha256': hashlib.sha256(raw_bytes).hexdigest(),
        'counts': {'sections': len(sections), 'assets': len(assets), 'tables': len(tables), 'zulkirs': sum(e['category'] == 'zulkirs' for e in entities), 'tharchs': sum(e['category'] == 'tharchs' for e in entities), 'wards': sum(e['category'] == 'wards' for e in entities)},
        'assets': assets, 'sections': [{k: s[k] for k in ('id', 'title')} for s in sections],
        'entities': [{k: e[k] for k in ('id', 'title', 'category')} for e in entities],
        'links': links, 'tables': tables,
    }
    write_json(output / 'manifest.json', manifest)
    write_json(output / 'tables/tables.json', tables)
    write_json(output / 'links.json', links)
    render_markdown(str(root), output / 'chapter.md', output, assets, source_url)
    for index, section in enumerate(sections):
        render_markdown(section['html'], output / 'sections' / (f'{index:02d}-' + safe_name(section['id']) + '.md'), output, assets, source_url)
    for entity in entities:
        render_markdown(entity['html'], output / 'entities' / entity['category'] / (safe_name(entity['id']) + '.md'), output, assets, source_url)
    local = clean_fragment(str(root))
    for tag in local.select('a[href],img[src]'):
        key = 'src' if tag.name == 'img' else 'href'
        value = tag[key]
        if value.startswith('#'):
            continue
        resolved = absolute_url(value, source_url)
        asset = next((a for a in assets if a['url'] == resolved), None)
        tag[key] = asset['path'] if asset and asset['status'] in LOCAL_STATUSES else resolved
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>' + html.escape(manifest['title']) + '</title><style>body{max-width:1000px;margin:2em auto;padding:1em;font:18px/1.6 system-ui}img{max-width:100%;height:auto}table{border-collapse:collapse}td,th{border:1px solid #aaa;padding:.4em}aside{border-left:4px solid #888;padding:1em}.artist-credit{font-size:.8em}.visually-hidden{display:none}</style></head><body><p><strong>Ressource MJ — spoilers. Copie locale du HTML fourni.</strong></p>' + str(local) + '</body></html>'
    (output / 'chapter.html').write_text(page, encoding='utf-8')
    index_lines = ['# ' + manifest['title'], '', 'Ressource MJ : contient des secrets. Ne pas publier ce dossier.', '', '[Chapitre complet Markdown](chapter.md) · [Lecture locale HTML](chapter.html)', '', '## Sections']
    for index, section in enumerate(sections):
        index_lines.append('- [' + section['title'] + '](sections/' + f'{index:02d}-' + safe_name(section['id']) + '.md)')
    for category in ('zulkirs', 'tharchs', 'wards'):
        index_lines += ['', '## ' + category]
        for entity in entities:
            if entity['category'] == category:
                index_lines.append('- [' + entity['title'] + '](entities/' + category + '/' + safe_name(entity['id']) + '.md)')
    index_lines += ['', '## Images et cartes']
    for asset in assets:
        index_lines.append('- [' + Path(asset['path']).name + '](' + (asset['path'] if asset['status'] in LOCAL_STATUSES else asset['url']) + ') — ' + asset['audience'] + ' — ' + asset['artist'] + ' — ' + asset['status'])
    (output / 'README.md').write_text('\n'.join(index_lines) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Local HTML supplied by the user')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-url', required=True, help='Reference only; never fetched')
    parser.add_argument('--download-images', action='store_true', help='Download only explicit image URLs on media.dndbeyond.com')
    args = parser.parse_args()
    result = import_html(args.input, args.output, args.source_url, download=args.download_images)
    print(json.dumps({'output': str(args.output.resolve()), 'counts': result['counts'], 'images': {status: sum(a['status'] == status for a in result['assets']) for status in sorted({a['status'] for a in result['assets']})}}, ensure_ascii=False, indent=2))
    if any(a['status'] == 'error' for a in result['assets']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
