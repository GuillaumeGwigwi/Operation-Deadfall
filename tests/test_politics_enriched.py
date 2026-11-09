"""Public illustrations and real, reproducible Homebrewery pagination."""
import json
import pytest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources/site/politique'

def test_regions_use_real_reference_tables_and_edge_art():
    data = json.loads((SRC / 'fiches-data.json').read_text())
    for key, html in data['tharchs'].items():
        assert '<h5>Gouvernement</h5>\n<table>' in html, key
        assert '<th align=left scope="col">Repère</th>' in html, key
        assert '<th align=left scope="col">Information</th>' in html, key
        assert '<th>Gouvernement</th>' not in html, key
        assert 'class="block note"' not in html, key
        assert '<td align=left>' in html, key
    for key in ('alaor', 'gauros', 'eltabbar'):
        assert 'data-page-art' in data['tharchs'][key], key
        assert 'imageMaskEdge' in data['tharchs'][key], key


def test_composition_uses_panoramas_and_protects_heading_starts():
    import re
    data = json.loads((SRC / 'fiches-data.json').read_text())
    for key in ('alaor', 'gauros', 'thazalhar'):
        assert 'class="imageMaskEdge1 bottom"' in data['tharchs'][key], key
    for key, html in data['tharchs'].items():
        assert '<h3>' in html and '<h2>' not in html, key
    for key, pages in data['tharchPages'].items():
        assert any('columnSplit' in p for p in pages), key
        for page in pages:
            assert '<h2>' not in page and '<h3>' in page, key
            assert '<div class="block"><h3>' not in page, 'Keep sibling spacing native, not hidden in wrappers'
    assert len(data['tharchPages']['eltabbar']) == 2
    assert 'Gerralt Landman' in data['tharchs']['eltabbar']


def test_every_source_paragraph_and_reference_value_is_preserved():
    import subprocess
    from html.parser import HTMLParser
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(); self.parts = []
        def handle_data(self, data):
            self.parts.append(data)
    def plain(html):
        parser = Text(); parser.feed(html)
        return ''.join(parser.parts).strip()
    import re
    data = json.loads((SRC / 'fiches-data.json').read_text())
    for key, html in data['tharchs'].items():
        source = (SRC / 'tharchs' / f'{key}.md').read_text()
        native = subprocess.check_output(['node', '--input-type=module', '-e',
            "import {hbfm} from 'marked-hbfm/src/index.js';let s='';for await(const c of process.stdin)s+=c;console.log(hbfm.render(s));"],
            input=source, text=True, cwd=ROOT / 'tools/homebrewery')
        for tag in ('h1', 'h2', 'p'):
            expected = [plain(s) for s in re.findall(f'<{tag}>(.*?)</{tag}>', native, re.S)]
            target_tag = 'h3' if tag == 'h2' else tag
            actual = [plain(s) for s in re.findall(f'<{target_tag}>(.*?)</{target_tag}>', html, re.S)]
            assert all(value in actual for value in expected), (key, tag)
        values = [plain(s) for s in re.findall(r'<(?:dt|dd)>(.*?)</(?:dt|dd)>', native, re.S)]
        assert values == [plain(s) for s in re.findall(r'<td\b[^>]*>(.*?)</td>', html, re.S)], key


def test_source_illustrations_are_embedded_with_exact_credits():
    data = json.loads((SRC / 'fiches-data.json').read_text())
    expected = {'alaor': 'Kevin Glint, Álvaro Calvo Escudero', 'delhumide': 'ÁLVARO CALVO ESCUDERO', 'gauros': 'David Frasheski', 'pyarados': 'LOÏC CANAVAGGIA', 'thaymount': 'Loïc Canavaggia, Helge C. Balzer', 'thazalhar': 'Andrey Kuzinskiy', 'eltabbar': 'Sylvain Sarrailh'}
    for key, credit in expected.items():
        html = data['tharchs'][key]
        assert 'data:image/webp;base64,' in html, key
        assert credit in html, key
        assert 'class="artist"' in html, key
        assert 'sources/chapters' not in html

def test_all_eleven_regions_have_lossless_browser_pagination():
    from html import unescape
    import re
    data = json.loads((SRC / 'fiches-data.json').read_text())
    assert 'tharchPages' in data, 'Real browser pagination is missing'
    assert set(data['tharchPages']) == set(data['tharchs'])
    text = lambda html: re.sub(r'\s+', '', unescape(re.sub('<[^>]*>', '', html)))
    for key, pages in data['tharchPages'].items():
        assert pages and all(p.strip() for p in pages)
        assert text(''.join(pages)) == text(data['tharchs'][key]), key
    assert data['pagination']['engine'] == 'Chromium / official Homebrewery V3'
    assert data['pagination']['overflow'] == []

@pytest.mark.parametrize('heading', ['h1', 'h2', 'h3'])
def test_browser_paginates_oversized_paragraph_without_losing_words(heading):
    import importlib.util
    from playwright.sync_api import sync_playwright
    spec = importlib.util.spec_from_file_location('paginate_politics', ROOT / 'tools/paginate_politics.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with sync_playwright() as pw:
        exe = sorted((Path.home() / '.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
        browser = pw.chromium.launch(executable_path=str(exe), headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        css = (SRC / 'homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
        page.set_content('<style>'+css+'</style><div class="brewRenderer"><div class="pages"><div class="page"></div></div></div>')
        result = page.evaluate(module.PAGINATE, f'<{heading}>Texte long</{heading}><p>' + 'Le voyageur suit la route. ' * 1500 + '</p>')
        assert len(result['pages']) > 1
        assert not result['failures']
        assert sum(html.count('voyageur') for html in result['pages']) == 1500
        browser.close()

def test_composed_pages_keep_headings_captions_and_exact_paragraphs():
    from playwright.sync_api import sync_playwright
    data = json.loads((SRC / 'fiches-data.json').read_text())
    css = (SRC / 'homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
    with sync_playwright() as pw:
        exe = sorted((Path.home() / '.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
        browser = pw.chromium.launch(executable_path=str(exe), headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1200, 'height': 1400})
        page.set_content('<style>'+css+'</style><div class="brewRenderer"><div class="pages"><div class="page"></div></div></div>')
        for key, pages in data['tharchPages'].items():
            result = page.evaluate('''async ({source,pages})=>{
              const raw=document.createElement('div');raw.innerHTML=source;
              const joined=document.createElement('div');joined.innerHTML=pages.join('');
              const exact=JSON.stringify([...raw.querySelectorAll('p,h1,h2,h3,h5,td,th')].map(e=>e.textContent))===JSON.stringify([...joined.querySelectorAll('p,h1,h2,h3,h5,td,th')].map(e=>e.textContent));
              const errors=[];
              for(const html of pages){
                const p=document.querySelector('.page');p.innerHTML=html;
                await document.fonts.ready;await Promise.all([...p.querySelectorAll('img')].map(i=>i.decode()));
                const middle=p.getBoundingClientRect().left+p.clientWidth/2;
                const tops=[Infinity,Infinity];
                for(const el of p.children){
                  if(el.matches('.wide,.artist,[data-page-art],.columnSplit'))continue;
                  for(const rect of el.getClientRects())tops[rect.left<middle?0:1]=Math.min(tops[rect.left<middle?0:1],rect.top);
                }
                if(!tops.every(Number.isFinite)||Math.abs(tops[0]-tops[1])>1)errors.push('unaligned column tops');
                for(const h of p.querySelectorAll('h3,h5')){
                  const next=h.nextElementSibling;
                  if(!next){errors.push(h.textContent);continue;}
                  const r=document.createRange();r.selectNodeContents(next);
                  const first=r.getClientRects()[0], title=h.getBoundingClientRect();
                  if(!first || Math.abs(first.left-title.left)>6 || first.top<title.bottom-2)errors.push(h.textContent);
                  if(h.tagName==='H3' && (getComputedStyle(h).borderBottomWidth!=='2px' || Math.abs(parseFloat(getComputedStyle(next).marginTop)-6.425)>0.1))errors.push('native heading rhythm');
                }
                const artist=p.querySelector('.artist'), art=p.querySelector('[data-page-art]');
                const overlaps=(a,b)=>a.left<b.right-1 && a.right>b.left+1 && a.top<b.bottom-1 && a.bottom>b.top+1;
                if(art){
                  const image=art.querySelector('img').getBoundingClientRect();
                  const pageBox=p.getBoundingClientRect();
                  const ink={left:image.left,right:image.right,top:Math.max(image.top,pageBox.top+508-parseFloat(art.style.getPropertyValue('--offset'))),bottom:image.bottom};
                  for(const el of p.querySelectorAll('h1,h2,h3,h5,td,th,p')){
                    if(el.closest('[data-page-art]'))continue;
                    const range=document.createRange();range.selectNodeContents(el);
                    for(const rect of range.getClientRects()){
                      if(overlaps(rect,ink))errors.push('text-art collision: '+el.textContent.slice(0,25));
                      if(artist && !el.closest('.artist') && overlaps(rect,artist.getBoundingClientRect()))errors.push('credit collision');
                    }
                  }
                }
                for(const fig of p.querySelectorAll('figure')){
                  const im=fig.querySelector('img').getBoundingClientRect(), cap=fig.querySelector('figcaption').getBoundingClientRect();
                  if(cap.top<im.bottom-2 || Math.abs(cap.left-im.left)>2)errors.push('caption');
                }
              }
              return {exact,errors};
            }''', {'source': data['tharchs'][key], 'pages': pages})
            assert result['exact'], key
            assert not result['errors'], (key, result['errors'])
        browser.close()


def test_isolated_delivery_images_and_pages_are_offline(tmp_path):
    import re
    import shutil
    from playwright.sync_api import sync_playwright
    target = tmp_path / 'dossier.html'
    shutil.copy2(ROOT / 'site/politique-thay.html', target)
    source = target.read_text()
    data = json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>', source, re.S).group(1))
    assert len(data['provinces']) == 11
    requests, errors = [], []
    with sync_playwright() as pw:
        exe = sorted((Path.home() / '.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
        browser = pw.chromium.launch(executable_path=str(exe), headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width':1440,'height':1100})
        page.on('request', lambda request: requests.append(request.url))
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(target.as_uri()+'#provinces')
        for province in data['provinces']:
            page.locator('[data-tharch="'+province['id']+'"]').click()
            page.wait_for_function('(name)=>document.querySelector("#tharch-frame").contentDocument?.querySelector(".page h1")?.textContent===name', arg=province['name'])
            frame = page.frame_locator('#tharch-frame')
            assert frame.locator('.page').count() == len(province['pages'])
            images = frame.locator('.page img')
            for i in range(images.count()):
                assert images.nth(i).evaluate('async image=>{await image.decode();return image.naturalWidth>0 && image.src.startsWith("data:")}')
            if province['id']=='gauros':
                page.screenshot(path='/tmp/politics-enriched-gauros.png')
            page.keyboard.press('Escape')
        assert not errors
        assert all(url.startswith(('data:', target.as_uri())) for url in requests)
        browser.close()
    for image in (SRC / 'assets/regions').glob('*.webp'):
        blob = image.read_bytes()
        assert blob[:4] == b'RIFF' and blob[8:12] == b'WEBP'
        offset = 12
        while offset < len(blob):
            tag, length = blob[offset:offset+4], int.from_bytes(blob[offset+4:offset+8], 'little')
            assert tag not in {b'EXIF', b'XMP ', b'ICCP'}
            offset += 8 + length + length % 2
