import asyncio,tempfile,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 with tempfile.TemporaryDirectory(prefix='atlas-search-') as tmp:
  path=Path(tmp)/'atlas.html';shutil.copy2(ROOT/'site/atlas-de-thay.html',path)
  async with async_playwright() as p:
   exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
   browser=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
   for width,height in [(1440,1000),(390,844)]:
    page=await browser.new_page(viewport={'width':width,'height':height});errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
    await page.goto(path.as_uri());await page.locator('#search').wait_for(state='attached')
    if await page.locator('#list-toggle').get_attribute('aria-expanded')=='true':await page.locator('#list-toggle').click()
    assert await page.locator('#search').is_visible(),'La recherche doit rester visible quand les lieux sont repliés'
    await page.locator('#search').fill('bezantur')
    assert await page.locator('#list-toggle').get_attribute('aria-expanded')=='true'
    first=page.locator('#landmark-list button:visible').first
    assert await first.get_attribute('data-id')=='bezantur','Le nom exact doit apparaître en premier'
    await first.click();assert await page.locator('#detail-title').inner_text()=='Bezantur'
    await page.locator('#detail-close').click()
    await page.locator('#search').fill('Crystal Ball')
    await page.locator('#landmark-list button[data-id="eltabbar"]').click()
    assert 'Crystal Ball' in await page.locator('#detail-body').inner_text()
    await page.locator('#detail-close').click();await page.locator('#search').fill('zzzzzz');assert await page.locator('#empty-state').is_visible()
    await page.locator('#clear-search').click();assert await page.locator('#landmark-list button:visible').count()==46
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    await page.locator('#list-toggle').click();assert await page.locator('#search').is_visible()
    await page.screenshot(path=f'/tmp/thay-atlas-search-{width}.png')
    assert not errors,errors;assert all(u.startswith(path.as_uri()) or u.startswith('data:') for u in requests),requests
    await page.close()
   await browser.close();print('PASS : recherche toujours visible PC/mobile, ouverture des résultats, priorité au nom exact, texte des fiches, état vide, effacement ; aucun réseau ni erreur JS.')
asyncio.run(main())
