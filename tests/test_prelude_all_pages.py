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
  expected=await page.evaluate('PRELUDE.documents.reduce((n,d)=>n+d.pages.length,0)')
  actual=await page.frame_locator('#reader').locator('.page').count()
  print('Pages du livre dans le lecteur:',actual,'attendues:',expected)
  assert actual==expected and actual>1,'Le lecteur doit contenir tout le livre, pas remplacer une fiche par une autre'
  await b.close()
asyncio.run(main())
