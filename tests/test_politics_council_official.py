import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def test_official_council():
    with sync_playwright() as pw:
        exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
        browser=pw.chromium.launch(executable_path=str(exe),args=['--no-sandbox'])
        for width in [1440,390]:
            page=browser.new_page(viewport={'width':width,'height':1100})
            page.goto((ROOT/'site/politique-thay.html').as_uri()+'#conseil')
            assert page.locator('#reader-frame').count()==1, 'Council must use the actual official renderer, not .hb-body imitation'
            for i in range(8):
                page.locator('.zulkir-card').nth(i).click()
                name=page.locator('#reader-title').inner_text()
                page.wait_for_function('(name)=>document.querySelector("#reader-frame").contentDocument?.querySelector("h1")?.textContent===name',arg=name)
                body=page.frame_locator('#reader-frame').locator('.page')
                body.evaluate('async el=>{await el.ownerDocument.fonts.ready;await Promise.all([...el.querySelectorAll("img")].map(i=>i.decode()))}')
                metrics=body.evaluate('el=>({font:getComputedStyle(el).fontFamily,columns:getComputedStyle(el).columnCount,w:el.clientWidth,sw:el.scrollWidth,h:el.clientHeight,sh:el.scrollHeight,bottom:Math.max(...[...el.querySelectorAll("p,h1,img,.note")].map(n=>n.getBoundingClientRect().bottom-el.getBoundingClientRect().top))})')
                assert 'BookInsanity' in metrics['font'] and metrics['columns']=='2',metrics
                assert metrics['sw']<=metrics['w'] and metrics['sh']<=metrics['h'] and metrics['bottom']<metrics['h']-40,metrics
                assert body.locator('img').count()==1
                assert body.locator('.note').count()==0, 'Reference facts should be composed as native tables, not repeated heavy callouts'
                assert body.locator('table').count()==(0 if i==1 else 1)
                if i!=1:
                    assert body.locator('h5 + table').count()==1, 'A table title is an h5, not a colspan header'
                    assert body.locator('thead th').all_text_contents()==['Repère','Information']
                    assert body.locator('thead th[colspan]').count()==0
                    assert body.locator('thead th').evaluate_all("els=>els.every(e=>getComputedStyle(e).textAlign==='left')")
                    assert body.locator('h5').evaluate("e=>getComputedStyle(e).fontFamily.includes('ScalySansSmallCaps')")
                    assert body.locator('h5 + table').evaluate("e=>parseFloat(getComputedStyle(e).marginTop)>0")
                    assert body.locator('table + p').evaluate("e=>parseFloat(getComputedStyle(e).marginTop)>0")
                if i not in [4,6]:
                    assert body.locator('[data-mask-source="official-imageMaskCenter6"]').count()==1
                    assert body.locator('img').get_attribute('src').startswith('data:image/webp;base64,'), 'Use the reviewed baked watercolor alpha, not a costly full-page mask layer'
                assert 'Solbera' not in body.locator('p').first.evaluate("el=>getComputedStyle(el,'::first-letter').fontFamily"), 'A short office subtitle is not a chapter opening'
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                if i==0:page.evaluate('window.councilDocument=document.querySelector("#reader-frame").contentDocument')
                else:assert page.evaluate('window.councilDocument===document.querySelector("#reader-frame").contentDocument')
                page.locator('#reader-close').click()
            page.close()
        browser.close()
if __name__=='__main__':
    test_official_council()
    print('PASS : huit zulkirs en thème officiel, iframe persistant, images et géométrie PC/mobile.')
