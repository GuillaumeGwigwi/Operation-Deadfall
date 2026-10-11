import asyncio,shutil,tempfile
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 with tempfile.TemporaryDirectory(prefix='atlas-sidebar-') as tmp:
  target=Path(tmp)/'atlas.html';shutil.copy2(ROOT/'site/index.html',target)
  async with async_playwright() as p:
   exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
   b=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
   for width,height in [(1440,1000),(390,844)]:
    page=await b.new_page(viewport={'width':width,'height':height});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(target.as_uri())
    if await page.locator('#list-toggle').get_attribute('aria-expanded')!='true':await page.locator('#list-toggle').click()
    guide=page.locator('#country-guide')
    assert await guide.locator('.guide-link-title').count()==1,'Entrée éditoriale du guide absente'
    assert await guide.locator('.guide-link-description').is_visible()
    assert (await guide.bounding_box())['height']>=64
    await guide.focus();await page.keyboard.press('Enter')
    assert await page.locator('#detail-panel').get_attribute('aria-modal')=='true'
    assert 'Thay' in await page.locator('#detail-title').inner_text()
    await page.locator('#detail-close').click()
    if await page.locator('#list-toggle').get_attribute('aria-expanded')!='true':await page.locator('#list-toggle').click()
    await page.locator('#search').fill('Bezantur');await page.locator('#landmark-list button[data-id="bezantur"]').click()
    assert await page.locator('#detail-title').inner_text()=='Bezantur'
    await page.locator('#detail-close').click();await page.locator('#clear-search').click()
    if await page.locator('#list-toggle').get_attribute('aria-expanded')!='true':await page.locator('#list-toggle').click()
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    await page.screenshot(path=f'/tmp/thay-atlas-menu-{width}.png')
    assert not errors,errors
    await page.close()
   await b.close();print('PASS : entrée guide éditoriale, accès clavier, lecture immersive, recherche et menu PC/mobile sans débordement.')
asyncio.run(main())
