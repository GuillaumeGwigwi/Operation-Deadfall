"""Recheck final compiled bytes after editorial/typographic fixes."""
import asyncio,json,hashlib,shutil,tempfile
from pathlib import Path
from playwright.async_api import async_playwright
from test_prelude_browser import CASES,CHECK_OVERFLOW
ROOT=Path(__file__).resolve().parents[1]
async def main():
 reports=[]
 async with async_playwright() as pw:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  b=await pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
  for filename,expected,key,term in CASES:
   with tempfile.TemporaryDirectory() as tmp:
    original=ROOT/'site'/filename;copy=Path(tmp)/'livre.html';shutil.copy2(original,copy)
    c=await b.new_context(offline=True,viewport={'width':1440,'height':1050})
    page=await c.new_page();errors=[];external=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
    await page.goto(copy.as_uri());await page.wait_for_function('window.READER_READY')
    navigated=await page.evaluate('''async()=>{
     const rooms=PRELUDE.entries.filter(e=>e.kind==='room');
     const fd=document.getElementById('reader').contentDocument;
     for(const entry of rooms){
      document.querySelector('.entry[data-id="'+entry.id+'"]').click();
      do{await new Promise(requestAnimationFrame);}while(!window.READER_READY);
      const h=fd.getElementById(entry.anchor);
      if(!h||h.closest('.page').id!=='p'+(entry.page+1)||document.getElementById('current-title').textContent!==entry.title)throw Error('Ancre erronée '+entry.key);
      if(document.getElementById('reader').contentDocument!==fd)throw Error('Livre rechargé');
     }
     return rooms.length;
    }''')
    assert navigated==expected
    data=await page.evaluate('PRELUDE');total=len(data['documents'][0]['pages'])
    assert await page.frame_locator('#reader').locator('.page').count()==total
    for pi in range(total):
     await page.evaluate('(i)=>goToPage(i)',pi);await page.evaluate('new Promise(requestAnimationFrame)')
     bad=await page.frame_locator('#reader').locator('#p'+str(pi+1)).evaluate(CHECK_OVERFLOW)
     assert not bad,(filename,pi,bad)
    await page.evaluate('goToPage(0)');await page.locator('#next').click();await page.wait_for_function('BOOK_PAGE===1')
    await page.locator('#previous').click();await page.wait_for_function('BOOK_PAGE===0')
    await page.locator('#search').fill(term.lower());assert await page.locator('.entry:visible').count()>0
    for width in [390,650]:
     await page.set_viewport_size({'width':width,'height':844})
     await page.wait_for_function('document.documentElement.scrollWidth<=innerWidth+1')
     if await page.locator('#entries').is_hidden():await page.locator('#toc-toggle').click()
     await page.locator('.entry:visible').first.click();await page.wait_for_function('window.READER_READY')
     await page.locator('#zoom').click();assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
     await page.locator('#zoom').click()
    assert not errors and not external,(errors,external)
    report={'file':filename,'html_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'source_sha256':data['source_sha256'],'rooms_navigated_in_final_book':navigated,'all_pages_without_overflow':total,'one_continuous_book':True,'same_document':True,'offline_isolated':True,'mobile':[390,650],'errors':errors,'external_requests':external}
    reports.append(report);print(json.dumps(report,ensure_ascii=False),flush=True)
    await c.close()
  await b.close()
 (ROOT/'sources/site/preludes/verification/final-report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
asyncio.run(main())
