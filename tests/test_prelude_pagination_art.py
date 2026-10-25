import asyncio,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_preludes import PAGINATE
async def main():
 async with async_playwright() as pw:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  b=await pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox']);p=await b.new_page()
  await p.set_content('<style>.page{box-sizing:border-box;width:816px;height:1056px;padding:60px;columns:2}</style><div class="page"></div>')
  rejected=False
  try:await p.evaluate(PAGINATE,['<img width="200" height="1600" alt="Image trop haute">'])
  except Exception as exc:
   assert 'Block larger than an official page' in str(exc);rejected=True
  assert rejected,'La pagination doit détecter une image qui déborde, même sans texte'
  await b.close();print('Image trop haute correctement refusée par la pagination.')
asyncio.run(main())
