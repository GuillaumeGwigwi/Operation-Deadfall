"""Real offline Chromium regression and timings; no shared build output is written.

uv run --with playwright --with pytest pytest -s tests/test_politics_performance.py
POLITICS_BENCHMARK_ONLY=1 records a pre-fix baseline without identity assertions.
"""
import json
import os
import re
import statistics
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def isolated_html(tmp_path):
    # Freeze the delivered public payload, exercise the current template only.
    delivered = (ROOT / 'site/politique-thay.html').read_text()
    template = (ROOT / 'sources/site/politique/index.template.html').read_text()
    for token, element in [('PUBLIC_DATA', 'politics-data'), ('IMAGES', 'politics-images'),
                           ('OFFICIAL_HB_CSS_GZIP', 'official-hb-style')]:
        payload = re.search(r'<script id="' + element + r'"[^>]*>(.*?)</script>', delivered, re.S).group(1)
        template = template.replace('{{' + token + '}}', payload)
    target = tmp_path / 'isolated.html'
    target.write_text(template)
    return target


def test_multipage_and_public_body_search(tmp_path):
    target = isolated_html(tmp_path)
    html = target.read_text()
    match = re.search(r'(<script id="politics-data"[^>]*>)(.*?)(</script>)', html, re.S)
    data = json.loads(match.group(2))
    province = data['provinces'][0]
    province['pages'] = [province['html'], '<h2>Suite</h2><p>RepereRegressionDeuxiemePage</p>']
    html = html[:match.start(2)] + json.dumps(data).replace('<', '\\u003c') + html[match.end(2):]
    target.write_text(html)
    with sync_playwright() as pw:
        executable = next((Path.home() / '.cache/ms-playwright').glob('chromium-*/**/chrome'))
        browser = pw.chromium.launch(executable_path=str(executable), args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        page.goto(target.as_uri() + '#provinces')
        page.locator('.province-card').first.click()
        settle(page)
        assert page.frame_locator('#tharch-frame').locator('.page').count() == 2
        dimensions = page.evaluate("""() => {
          const f=document.getElementById('tharch-frame'), pages=[...f.contentDocument.querySelectorAll('.page')];
          return {frame:parseFloat(f.style.height),bottom:pages.at(-1).getBoundingClientRect().bottom};
        }""")
        assert dimensions['frame'] >= dimensions['bottom'], 'Last page is clipped by iframe height'
        page.keyboard.press('Escape')
        page.locator('#province-search').fill('RepereRegressionDeuxiemePage')
        assert page.locator('.province-card:visible').count() == 1
        browser.close()


def settle(page):
    page.wait_for_function("""() => {
      const f=document.getElementById('tharch-frame'), h=f.contentDocument?.querySelector('.page h1');
      return h && h.textContent===document.getElementById('tharch-title').textContent;
    }""")
    page.evaluate("""async () => {
      const d=document.getElementById('tharch-frame').contentDocument;
      await d.fonts.ready;
      await Promise.all([...d.images].map(i=>i.decode().catch(()=>{})));
      await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
    }""")


@pytest.mark.parametrize('width,height', [(1440, 1000), (390, 844)])
def test_region_document_persists_offline(tmp_path, width, height):
    target = isolated_html(tmp_path)
    with sync_playwright() as pw:
        executable = next((Path.home() / '.cache/ms-playwright').glob('chromium-*/**/chrome'))
        browser = pw.chromium.launch(executable_path=str(executable), args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': width, 'height': height})
        errors, requests = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: requests.append(request.url))
        page.goto(target.as_uri() + '#provinces')
        page.evaluate("document.querySelector('.province-card').click()")
        settle(page)
        page.evaluate("""() => {
          window.savedDocument=document.getElementById('tharch-frame').contentDocument;
          window.savedStyle=savedDocument.querySelector('style');
          window.frameLoads=0;
          document.getElementById('tharch-frame').addEventListener('load',()=>frameLoads++);
        }""")
        timings = []
        for _ in range(11):
            page.evaluate("window.started=performance.now();document.getElementById('tharch-next').click()")
            settle(page)
            timings.append(page.evaluate('performance.now()-started'))
        evidence = page.evaluate("""() => ({
          sameDocument:savedDocument===document.getElementById('tharch-frame').contentDocument,
          sameStyle:savedStyle===document.getElementById('tharch-frame').contentDocument.querySelector('style'),
          frameLoads
        })""")
        report = dict(viewport=width, samples_ms=timings, median_ms=statistics.median(timings),
                      max_ms=max(timings), **evidence)
        print('POLITICS_PERFORMANCE ' + json.dumps(report))
        if not os.environ.get('POLITICS_BENCHMARK_ONLY'):
            assert evidence['sameDocument'], 'Region navigation replaced the iframe Document'
            assert evidence['sameStyle'], 'Official CSS was recreated on region navigation'
            assert evidence['frameLoads'] == 0
        # Burst navigation must commit only the latest selection.
        page.evaluate("for(let i=0;i<5;i++)document.getElementById('tharch-next').click()")
        settle(page)
        page.locator('#tharch-zoom').click()
        assert page.locator('#tharch-zoom').get_attribute('aria-pressed') == 'true'
        page.locator('#tharch-zoom').click()
        page.wait_for_function("document.getElementById('tharch-scroll').scrollWidth<=document.getElementById('tharch-scroll').clientWidth+1")
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=f'/tmp/politics-performance-{width}.png')
        page.keyboard.press('Escape')
        assert not page.locator('#tharch-reader').evaluate('d=>d.open')
        page.locator('.province-card').first.click()
        settle(page)
        if not os.environ.get('POLITICS_BENCHMARK_ONLY'):
            assert page.evaluate("savedDocument===document.getElementById('tharch-frame').contentDocument")
        assert not errors
        assert all(url.startswith((target.as_uri(), 'data:')) for url in requests), requests
        browser.close()
