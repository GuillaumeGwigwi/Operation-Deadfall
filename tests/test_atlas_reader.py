import asyncio,tempfile,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 with tempfile.TemporaryDirectory(prefix='atlas-reader-') as tmp:
  file=Path(tmp)/'atlas.html'; shutil.copy2(ROOT/'site/index.html',file)
  async with async_playwright() as p:
   exe=next(Path('/home/gwi/.cache/ms-playwright/chromium-1208').glob('**/chrome'))
   browser=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
   page=await browser.new_page(viewport={'width':1440,'height':1000})
   errors=[]; page.on('pageerror',lambda e: errors.append(str(e)))
   await page.goto(file.as_uri()); await page.emulate_media(reduced_motion='reduce')
   await page.locator('#landmark-list button[data-id="eltabbar"]').click()
   assert await page.locator('#detail-expand').count()==1,'Bouton Agrandir manquant'
   await page.locator('#detail-expand').click()
   panel=page.locator('#detail-panel'); assert await page.locator('#detail-expand').get_attribute('aria-expanded')=='true'
   box=await panel.bounding_box(); assert box['width']>1440*.85 and box['height']>1000*.9
   assert await panel.get_attribute('role')=='dialog' and await panel.get_attribute('aria-modal')=='true'
   assert await page.locator('#sidebar').evaluate('(e)=>e.inert')
   assert (await page.locator('#detail-section').bounding_box())['height'] >= 44
   options=await page.locator('#detail-section option').evaluate_all("els=>els.map(e=>({value:e.value,text:e.textContent}))")
   ward=next(o for o in options if '1. Quartier' in o['text'])
   await page.locator('#detail-section').select_option(ward['value'])
   await page.wait_for_function("document.getElementById('detail-panel').scrollTop>200")
   await panel.evaluate('e=>e.scrollTop=0')
   await page.screenshot(path='/tmp/thay-atlas-reader-desktop.png')
   await page.keyboard.press('Escape')
   assert await panel.is_visible() and await page.locator('#detail-expand').get_attribute('aria-expanded')=='false'
   assert await panel.get_attribute('data-selected')=='eltabbar'
   await page.locator('#detail-expand').click()
   await page.locator('#detail-close').click(); assert not await panel.is_visible()
   assert not await page.locator('#sidebar').evaluate('(e)=>e.inert')
   await page.set_viewport_size({'width':390,'height':844})
   await page.wait_for_function("document.getElementById('list-toggle').getAttribute('aria-expanded')==='false'")
   if await page.locator('#list-toggle').get_attribute('aria-expanded')!='true': await page.locator('#list-toggle').click()
   await page.locator('#search').fill('eltabbar')
   await page.locator('#landmark-list button[data-id="eltabbar"]').click(); await page.locator('#detail-expand').click()
   box=await panel.bounding_box(); assert box['width']>390*.9 and box['height']>844*.9
   assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
   await page.screenshot(path='/tmp/thay-atlas-reader-mobile.png')
   await page.keyboard.press('Escape'); assert await panel.is_visible()
   await page.keyboard.press('Escape'); assert not await panel.is_visible()
   if await page.locator('#list-toggle').get_attribute('aria-expanded')!='true': await page.locator('#list-toggle').click()
   assert await page.locator('#country-guide').count()==1,'Guide de Thay manquant'
   await page.locator('#country-guide').click()
   assert await panel.get_attribute('data-selected')=='guide-thay'
   assert await page.locator('#detail-expand').get_attribute('aria-expanded')=='true'
   assert 'Bas-Thay' in await page.locator('#detail-body').inner_text()
   await page.locator('#detail-close').click()
   await page.set_viewport_size({'width':1440,'height':1000})
   await page.wait_for_function("document.getElementById('list-toggle').getAttribute('aria-expanded')==='true'")
   await page.locator('#search').fill('Renatta Vott')
   assert await page.locator('#landmark-list button[data-id="eltabbar"]:visible').count()==1,'Recherche dans le texte intégral manquante'
   assert not errors,errors
   print('PASS: lecture presque plein écran, retour fiche, fermeture, arrière-plan inerte et mobile')
   await browser.close()
asyncio.run(main())
