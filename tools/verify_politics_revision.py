"""Exhaustive rendered-page review on an isolated, offline player artifact."""
import json, re, shutil, tempfile, time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'sources/site/politique/verification'
OUT.mkdir(exist_ok=True)
html = (ROOT/'site/politique-thay.html').read_text()
data = json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>', html, re.S)[1])
report = {'regions': [], 'screenshots': [], 'errors': [], 'externalRequests': []}
GEOMETRY = r'''el => {
 const b=el.getBoundingClientRect(), c=getComputedStyle(el), sx=b.width/el.offsetWidth;
 const bad=[];
 for(const node of el.querySelectorAll('p,h1,h2,h3,h4,h5,li,figure,img,figcaption,.note')) {
  for(const r of node.getClientRects()) if(r.right>b.right+1 || r.bottom>b.bottom+1 || r.left<b.left-1) bad.push({tag:node.tagName,text:node.textContent.slice(0,70),right:r.right-b.right,bottom:r.bottom-b.bottom});
 }
 return {font:c.fontFamily, columns:c.columnCount, bad, images:[...el.querySelectorAll('img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,alt:i.alt})),text:el.innerText};
}'''
with tempfile.TemporaryDirectory(prefix='thay-revision-isolated-') as temp, sync_playwright() as pw:
    target=Path(temp)/'guide.html';shutil.copy2(ROOT/'site/politique-thay.html',target)
    exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
    browser=pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
    for width,height in [(1440,1100),(390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        page.on('request',lambda r: report['externalRequests'].append(r.url) if not r.url.startswith(('file:', 'data:', 'blob:')) else None)
        page.goto(target.as_uri()+'#provinces')
        page.wait_for_selector('[data-tharch]')
        for index, region in enumerate(data['provinces']):
            start=time.perf_counter()
            page.locator('[data-tharch="'+region['id']+'"]').click()
            frame=page.frame_locator('#tharch-frame')
            page.wait_for_function('(name)=>document.querySelector("#tharch-frame").contentDocument?.querySelector(".page h1")?.textContent===name',arg=region['name'])
            frame.locator('.page').first.evaluate('async el=>{await el.ownerDocument.fonts.ready;await Promise.all([...el.ownerDocument.images].map(i=>i.decode()))}')
            page.wait_for_function('document.querySelector("#tharch-viewport").clientHeight>0')
            pages=frame.locator('.page')
            metrics=pages.evaluate_all('els=>els.map('+GEOMETRY+')')
            elapsed=round((time.perf_counter()-start)*1000,1)
            expected=region.get('pages',[region['html']])
            assert len(metrics)==len(expected),(region['id'],len(metrics),len(expected))
            for metric in metrics:
                assert 'BookInsanity' in metric['font'] and metric['columns']=='2',metric
                assert not metric['bad'],(region['id'],metric['bad'])
                assert all(i['loaded'] for i in metric['images']),region['id']
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            report['regions'].append({'id':region['id'],'viewport':width,'pages':len(metrics),'ready_ms':elapsed,'images':sum(len(m['images']) for m in metrics)})
            if width==1440:
                # Reopen the exact iframe document in a tall review surface: a
                # locator screenshot across an iframe's clipped scrollport can
                # produce a black strip despite valid page geometry.
                review=browser.new_page(viewport={'width':1000,'height':1300})
                review.set_content(page.locator('#tharch-frame').evaluate('f=>f.contentDocument.documentElement.outerHTML'))
                review.locator('.page').first.evaluate('async el=>{await el.ownerDocument.fonts.ready;await Promise.all([...el.ownerDocument.images].map(i=>i.decode()))}')
                for n in range(pages.count()):
                    image=OUT/f'{region["id"]}-{n+1}.png'
                    review.locator('.page').nth(n).screenshot(path=str(image))
                    report['screenshots'].append(str(image))
                review.close()
            elif region['id'] in ['alaor','eltabbar','thaymount']:
                page.screenshot(path=str(OUT/f'{region["id"]}-mobile.png'))
            page.locator('#tharch-close').click()
            page.wait_for_function('!document.querySelector("#tharch-reader").open')
        page.locator('#province-search').fill('Brenna')
        assert page.locator('[data-tharch]:visible').count()==1
        assert page.locator('[data-tharch]:visible').get_attribute('data-tharch')=='delhumide'
        page.close()
    browser.close()
assert len(report['regions'])==22
assert not report['errors'] and not report['externalRequests'],report
(OUT/'revision-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='screenshots'},ensure_ascii=False,indent=2))
