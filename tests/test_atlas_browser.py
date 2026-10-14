import asyncio,json,shutil,tempfile
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 isolated=tempfile.TemporaryDirectory(prefix='thay-atlas-seul-')
 standalone=Path(isolated.name)/'atlas-partage.html'
 shutil.copy2(ROOT/'site/atlas-de-thay.html',standalone)
 assert len(list(Path(isolated.name).iterdir()))==1
 async with async_playwright() as p:
  exe=next(Path('/home/gwi/.cache/ms-playwright/chromium-1208').glob('**/chrome'))
  browser=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1000},has_touch=True)
  errors=[]; requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda r: requests.append(r.url))
  await page.goto(standalone.as_uri(),wait_until='load')
  await page.locator('#map-image').evaluate('(e)=>e.decode()')
  await page.emulate_media(reduced_motion='reduce')
  data=await page.evaluate('window.THAY_ATLAS')
  ref=json.loads((ROOT/'sources/site/atlas/positions.json').read_text())
  async def verify_alignment():
   errors=await page.evaluate('''(ref) => {
    const image=document.getElementById('map-image').getBoundingClientRect();
    return ref.anchors.map(a => {
      const marker=document.querySelector(`.map-marker[data-id="${a.id}"] .glyph`).getBoundingClientRect();
      const targetX=image.left+a.pixel[0]/ref.width*image.width;
      const targetY=image.top+a.pixel[1]/ref.height*image.height;
      return {id:a.id,error:Math.hypot(marker.left+marker.width/2-targetX,marker.top+marker.height/2-targetY)};
    });
   }''',ref)
   assert len(errors)==46
   assert max(e['error'] for e in errors)<.1,errors
   return errors
  await verify_alignment()
  print('PASS: 46 glyphes centrés sur les ancres relevées de la carte originale')
  assert len(data['landmarks'])==46
  assert await page.locator('.map-marker').count()==46
  assert await page.locator('#landmark-list button').count()==46
  await page.screenshot(path='/tmp/thay-atlas-desktop.png')
  # Every public entry must open, include the exact generated Homebrewery HTML, and have valid media.
  for place in data['landmarks']:
   await page.locator(f'#landmark-list button[data-id="{place["id"]}"]').click()
   assert await page.locator('#detail-panel').get_attribute('data-selected')==place['id']
   assert await page.locator('#detail-title').inner_text()==place['name']
   assert await page.locator('#detail-body .note').count()==1
   assert await page.locator('#detail-body > h2:visible').count()==0
   assert await page.locator('#detail-media figcaption').count()==0
   visible_text=await page.locator('body').inner_text()
   for redundant in ['Le viseur indique','Repère placé à titre indicatif','Détail de la carte géographique','Francesca Baerald','Jeff Dee']:
    assert redundant not in visible_text,(place['id'],redundant)
   for img in await page.locator('#detail-media img').all():
    await img.evaluate('(e)=>e.decode()')
    assert await img.evaluate('(e)=>e.naturalWidth>0')
    assert (await img.get_attribute('alt') or '').strip(), f'Illustration sans description : {place["id"]}'
   await page.keyboard.press('Escape')
   assert not await page.locator('#detail-panel').is_visible()
  print('PASS: 46 fiches, contenu Homebrewery, médias et fermeture Échap')
  await page.locator('#category').select_option('province')
  assert await page.locator('.map-marker:visible').count()==11
  assert await page.locator('#landmark-list button:visible').count()==11
  await page.locator('#clear-search').click()
  await page.locator('#search').fill('bezantur')
  assert await page.locator('#landmark-list button:visible').count()>=1
  await page.locator('#search').fill('zzz-no-result')
  assert await page.locator('.map-marker:visible').count()==0
  assert await page.locator('#empty-state').is_visible()
  await page.locator('#clear-search').click()
  await verify_alignment()
  assert await page.locator('.map-marker:visible').count()==46
  z=float(await page.locator('#map-stage').get_attribute('data-zoom'))
  await page.locator('#zoom-in').click()
  assert float(await page.locator('#map-stage').get_attribute('data-zoom'))>z
  await page.locator('#reset-view').click()
  assert float(await page.locator('#map-stage').get_attribute('data-zoom'))==1
  await page.locator('#map-stage').focus()
  await page.keyboard.press('+')
  assert float(await page.locator('#map-stage').get_attribute('data-zoom'))>1
  transform=await page.locator('#map-world').get_attribute('style')
  await page.keyboard.press('ArrowLeft')
  assert await page.locator('#map-world').get_attribute('style')!=transform
  await page.mouse.move(800,350)
  await page.mouse.wheel(0,-150)
  zoom_before_drag=await page.locator('#map-stage').get_attribute('data-zoom')
  assert float(zoom_before_drag)>1
  transform=await page.locator('#map-world').get_attribute('style')
  await page.mouse.move(800,350); await page.mouse.down(); await page.mouse.move(850,390,steps=8); await page.mouse.up()
  assert await page.locator('#map-world').get_attribute('style')!=transform
  assert not await page.locator('#detail-panel').is_visible()
  await verify_alignment()
  print('PASS: clavier, molette et déplacement souris sans ouverture involontaire')
  await page.locator('#reset-view').click()
  await page.locator('#search').fill('bezantur')
  marker=page.locator('.map-marker[data-id="bezantur"]'); await marker.click()
  assert await page.locator('#detail-panel').get_attribute('data-selected')=='bezantur'
  await page.screenshot(path='/tmp/thay-atlas-detail.png')
  print('PASS: filtres, recherche, état vide, zoom, reset et repère carte')
  await page.goto(standalone.as_uri()+'#lieu=eltabbar')
  assert await page.locator('#detail-panel').get_attribute('data-selected')=='eltabbar'
  await page.goto(standalone.as_uri()+'#lieu=unknown')
  assert not await page.locator('#detail-panel').is_visible()
  assert await page.locator('#feedback').inner_text()
  if await page.locator('#clear-search').is_visible(): await page.locator('#clear-search').click()
  await page.set_viewport_size({'width':390,'height':844})
  await page.locator('#reset-view').click()
  await verify_alignment()
  await page.screenshot(path='/tmp/thay-atlas-mobile.png')
  cdp=await page.context.new_cdp_session(page)
  before=float(await page.locator('#map-stage').get_attribute('data-zoom'))
  await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':100,'y':350,'id':1},{'x':260,'y':490,'id':2}]})
  await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':50,'y':310,'id':1},{'x':310,'y':530,'id':2}]})
  await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
  assert float(await page.locator('#map-stage').get_attribute('data-zoom'))>before
  await page.locator('#reset-view').click()
  print('PASS: pincement tactile en émulation mobile Chromium')
  if await page.locator('#list-toggle').get_attribute('aria-expanded')!='true': await page.locator('#list-toggle').click()
  await page.locator('#search').fill('eltabbar')
  await page.locator('#landmark-list button[data-id="eltabbar"]').click()
  assert await page.locator('#detail-panel').is_visible()
  await page.screenshot(path='/tmp/thay-atlas-mobile-detail.png')
  assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
  await page.locator('#detail-close').click()
  print('PASS: liens profonds valides/invalides et interface mobile sans débordement')
  assert not errors,errors
  remote=[r for r in requests if r.startswith(('http:','https:'))]; assert not remote,remote
  bad=[r for r in requests if '/sources/' in r]; assert not bad,bad
  external=[r for r in requests if not r.startswith('data:') and r.split('#')[0]!=standalone.as_uri()]
  assert not external,external
  print('PASS: HTML copié seul hors du projet, aucune ressource externe, aucune erreur JS')
  print('TOTAL',len(data['landmarks']), 'REQUÊTES',len(requests))
  await browser.close()
 isolated.cleanup()
asyncio.run(main())
