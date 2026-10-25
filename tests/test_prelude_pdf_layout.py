"""Check actual PDF glyphs, not only the browser's screen layout."""
import asyncio,json
from pathlib import Path
import pypdfium2 as pdfium
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as pw:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  browser=await pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox']);page=await browser.new_page()
  await page.emulate_media(media='print')
  css=(ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
  await page.set_content('<style>'+css+'</style><div class="brewRenderer"><div class="pages"><div class="page"></div></div></div>')
  box=await page.eval_on_selector('.page','e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {width:r.width,height:r.height,left:parseFloat(s.paddingLeft),right:parseFloat(s.paddingRight),top:parseFloat(s.paddingTop),bottom:parseFloat(s.paddingBottom)}}')
  await browser.close()
 reports=[]
 for name in ['prelude-cavernes-du-chaos-mj.pdf','prelude-dragon-d-alaor-mj.pdf']:
  doc=pdfium.PdfDocument(ROOT/'site'/name);bad=[]
  for n,p in enumerate(doc,1):
   text=p.get_textpage();sx=p.get_width()/box['width'];sy=p.get_height()/box['height'];left=box['left']*sx-3;right=p.get_width()-box['right']*sx+3
   offenders=[]
   for i in range(text.count_chars()):
    x0,y0,x1,y1=text.get_charbox(i);char=text.get_text_range(i,1)
    # The official ornamental drop capital intentionally hangs in the margin.
    left_overflow=x0<left and not (y1-y0>20 and x0>=left-15)
    if char.strip() and y0>box['bottom']*sy and y1<p.get_height()-box['top']*sy and (left_overflow or x1>right):offenders.append(i)
   if offenders:
    i=offenders[0];bad.append({'page':n,'characters_outside_body':len(offenders),'context':text.get_text_range(max(0,i-25),70)})
   text.close();p.close()
  doc.close();reports.append({'file':name,'body_overflow':bad})
 path=ROOT/'sources/site/preludes/verification/pdf-layout.json';path.write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');print(json.dumps(reports,ensure_ascii=False,indent=2));assert not any(x['body_overflow'] for x in reports), 'Du texte dépasse le corps du PDF imprimé'
asyncio.run(main())
