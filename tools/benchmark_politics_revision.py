"""Compare committed delivery with rebuilt delivery in the same offline browser."""
import json, statistics, subprocess, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'sources/site/politique/verification/performance-before-after.json'
def ready(p):
    p.wait_for_function('()=>{const d=document.querySelector("#tharch-frame").contentDocument;return d?.querySelector("h1")?.textContent===document.querySelector("#tharch-title").textContent}')
    p.evaluate('async()=>{const d=document.querySelector("#tharch-frame").contentDocument;await d.fonts.ready;await Promise.all([...d.images].map(i=>i.decode()));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))}')
report=[]
with tempfile.TemporaryDirectory() as temp, sync_playwright() as pw:
    old=Path(temp)/'before.html';old.write_bytes(subprocess.check_output(['git','show','HEAD:site/politique-thay.html'],cwd=ROOT))
    new=Path(temp)/'after.html';new.write_bytes((ROOT/'site/politique-thay.html').read_bytes())
    exe=next((Path.home()/'.cache/ms-playwright').glob('chromium-*/**/chrome'))
    browser=pw.chromium.launch(executable_path=str(exe),args=['--no-sandbox'])
    for width in [1440,390]:
        for label,path in [('before',old),('after',new)]:
            page=browser.new_page(viewport={'width':width,'height':1000})
            page.goto(path.as_uri()+'#provinces')
            page.evaluate('window.start=performance.now();document.querySelector(".province-card").click()')
            ready(page)
            first=page.evaluate('performance.now()-start')
            page.evaluate('window.saved=document.querySelector("#tharch-frame").contentDocument;window.loads=0;document.querySelector("#tharch-frame").addEventListener("load",()=>loads++)')
            values=[]
            for i in range(11):
                page.evaluate('window.start=performance.now();document.querySelector("#tharch-next").click()');ready(page)
                values.append(round(page.evaluate('performance.now()-start'),1))
            entry=dict(version=label,viewport=width,first_open_ms=round(first,1),navigation_ms=values,median_ms=round(statistics.median(values),1),max_ms=max(values),same_document=page.evaluate('saved===document.querySelector("#tharch-frame").contentDocument'),iframe_reloads=page.evaluate('loads'))
            report.append(entry);print(json.dumps(entry));page.close()
    browser.close()
OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(report,indent=2)+'\n')
