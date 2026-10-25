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
  await page.evaluate('document.getElementById("reader").contentDocument.documentElement.dataset.testIdentity="original"')
  await page.locator('.entry[data-kind="room"]').first.click()
  await page.wait_for_function('document.getElementById("reader-status").textContent.includes("Hors connexion")')
  identity=await page.evaluate('document.getElementById("reader").contentDocument.documentElement.dataset.testIdentity')
  print('Identité du document après navigation:',identity)
  assert identity=='original','Each room must reuse the loaded official stylesheet and fonts'
  await b.close()
asyncio.run(main())
