import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  b=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
  page=await b.new_page()
  await page.goto((ROOT/'site/prelude-cavernes-du-chaos-mj.html').as_uri())
  await page.wait_for_function('window.READER_READY===true')
  first=await page.locator('#current-title').inner_text()
  await page.locator('.entry[data-kind="room"]').first.click()
  await page.evaluate('location.hash="unknown-entry"')
  await page.wait_for_function('location.hash==="#unknown-entry"')
  await page.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
  current=await page.locator('#current-title').inner_text()
  print({'expected':first,'actual':current,'hash':await page.evaluate('location.hash')})
  assert current==first,'Unknown hash should return to initial document'
  await b.close()
asyncio.run(main())
