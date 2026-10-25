"""Verify complete continuous books in isolated, offline HTMLs."""
import asyncio,json,shutil,tempfile
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
CASES=[('prelude-cavernes-du-chaos-mj.html',64,'C3','Vinx'),('prelude-dragon-d-alaor-mj.html',39,'M26','Ronnom')]
CHECK_OVERFLOW=r'''p=>{
 const b=p.getBoundingClientRect(),cs=getComputedStyle(p),right=b.right-parseFloat(cs.paddingRight)+1,bottom=b.bottom-parseFloat(cs.paddingBottom)+1;
 const walker=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);let n;const bad=[];
 while(n=walker.nextNode()){
  if(!n.textContent.trim()||n.parentElement.closest('.footnote,.pageNumber'))continue;
  const r=document.createRange();r.selectNodeContents(n);
  for(const box of r.getClientRects())if(box.right>right||box.bottom>bottom)bad.push(n.textContent.slice(0,90));
 }
 for(const im of p.querySelectorAll('img')){const r=im.getBoundingClientRect();if(r.right>right||r.bottom>bottom)bad.push('IMAGE : '+im.alt);}
 return [...new Set(bad)];
}'''
async def main():
 reports=[];shots=ROOT/'sources/site/preludes/verification';shots.mkdir(exist_ok=True)
 async with async_playwright() as pw:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  browser=await pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
  for filename,count,key,term in CASES:
   with tempfile.TemporaryDirectory(prefix='prelude-livre-seul-') as tmp:
    target=Path(tmp)/'livre.html';shutil.copy2(ROOT/'site'/filename,target)
    assert len(list(Path(tmp).iterdir()))==1
    context=await browser.new_context(viewport={'width':1440,'height':1050},offline=True)
    page=await context.new_page();errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    await page.goto(target.as_uri());await page.wait_for_function('window.READER_READY===true')
    data=await page.evaluate('PRELUDE');assert len(data['documents'])==1
    total=len(data['documents'][0]['pages'])
    assert await page.frame_locator('#reader').locator('.page').count()==total
    await page.evaluate('document.getElementById("reader").contentDocument.documentElement.dataset.identity="same-book"')
    await page.locator('[data-filter="room"]').click()
    assert await page.locator('.entry:visible').count()==count
    for room_index,entry in enumerate([e for e in data['entries'] if e['kind']=='room']):
     if room_index%10==0:print('Navigation',filename,room_index,entry['title'],flush=True)
     await page.locator(f'.entry[data-id="{entry["id"]}"]').click()
     await page.wait_for_function('(id)=>window.READER_READY&&document.getElementById("current-title").textContent===PRELUDE.entries.find(e=>e.id===id).title',arg=entry['id'])
     frame=page.frame_locator('#reader')
     anchor=frame.locator('#'+entry['anchor'])
     assert await anchor.count()==1
     actual_page=await anchor.evaluate('e=>e.closest(".page").id')
     assert actual_page=='p'+str(entry['page']+1)
     assert await page.evaluate('document.getElementById("reader").contentDocument.documentElement.dataset.identity')=='same-book'
    # Scroll through every page of the same book and measure actual columns.
    for pi in range(total):
     await page.evaluate('(i)=>goToPage(i)',pi)
     p=page.frame_locator('#reader').locator('#p'+str(pi+1))
     await p.evaluate('e=>e.ownerDocument.fonts.ready')
     await page.evaluate('new Promise(r=>requestAnimationFrame(r))')
     bad=await p.evaluate(CHECK_OVERFLOW)
     assert not bad,(filename,pi+1,bad)
     assert await page.evaluate('BOOK_PAGE')==pi,(filename,pi)
    # Page buttons cross chapter boundaries without resetting the book.
    await page.evaluate('goToPage(0)')
    await page.locator('#next').click();await page.wait_for_function('BOOK_PAGE===1')
    await page.locator('#previous').click();await page.wait_for_function('BOOK_PAGE===0')
    await page.locator('[data-filter="all"]').click()
    await page.locator('#search').fill(term.lower());assert await page.locator('.entry:visible').count()>0
    await page.locator('#search').fill('zz-introuvable');assert await page.locator('#empty').is_visible()
    await page.locator('#clear').click();await page.locator('#search').fill(key)
    room=next(e for e in data['entries'] if e.get('key')==key)
    await page.locator(f'.entry[data-id="{room["id"]}"]').click();await page.wait_for_function('window.READER_READY')
    computed=await page.frame_locator('#reader').locator('.page').first.evaluate('e=>({font:getComputedStyle(e).fontFamily,columns:getComputedStyle(e).columnCount})')
    assert 'BookInsanity' in computed['font'] and computed['columns']=='2'
    await page.screenshot(path=str(shots/(filename+'-desktop.png')))
    for width in [390,650]:
     await page.set_viewport_size({'width':width,'height':844})
     await page.wait_for_function('document.documentElement.scrollWidth<=innerWidth+1')
     await page.locator('#zoom').click();assert await page.locator('#zoom').get_attribute('aria-pressed')=='true'
     assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
     await page.locator('#zoom').click()
     await page.locator('#search').fill(term);assert await page.locator('.entry:visible').count()>0
     await page.locator('.entry:visible').first.click();await page.wait_for_function('window.READER_READY')
     if width==390:
      assert await page.locator('#entries').is_hidden()
      await page.screenshot(path=str(shots/(filename+'-mobile.png')),full_page=True)
    await page.set_viewport_size({'width':1440,'height':1050})
    await page.keyboard.press('/');assert await page.locator('#search').evaluate('e=>document.activeElement===e')
    await page.keyboard.press('Escape');assert await page.locator('#search').input_value()==''
    await page.evaluate('location.hash="unknown-entry"')
    await page.wait_for_function('document.getElementById("current-title").textContent===PRELUDE.entries[0].title')
    assert not errors,errors
    external=[u for u in requests if not (u.startswith('data:') or u.split('#')[0]==target.as_uri())]
    assert not external,external
    report={'file':filename,'continuous_books':1,'locations_opened':count,'all_pages_checked':total,'all_pages_in_same_reader':True,'iframe_reused':True,'desktop':True,'mobile_widths':[390,650],'official_font':computed,'javascript_errors':errors,'external_requests':external,'isolated_offline':True}
    reports.append(report);print(json.dumps(report,ensure_ascii=False),flush=True)
    await context.close()
  await browser.close()
 (shots/'browser-report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
 asyncio.run(main())
