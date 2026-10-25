"""Export the already composed Homebrewery books, unchanged, to PDFs."""
import argparse,asyncio,html,json
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
FILES=['prelude-cavernes-du-chaos-mj.html','prelude-dragon-d-alaor-mj.html']
async def main(only=None):
 css=(ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
 reports=[]
 async with async_playwright() as pw:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  browser=await pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
  for filename in FILES:
   if only and filename!={'cavernes':FILES[0],'alaor':FILES[1]}[only]:continue
   soup=BeautifulSoup((ROOT/'site'/filename).read_text(),'html.parser')
   data=json.loads(soup.select_one('#prelude-data').string);pages=data['documents'][0]['pages']
   paper=''.join('<div class="page" id="p'+str(i+1)+'">'+p+'<div class="pageNumber">'+str(i+1)+'</div><div class="footnote">PRÉLUDE · MJ</div></div>' for i,p in enumerate(pages))
   page=await browser.new_page();await page.emulate_media(media='print')
   await page.set_content('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>'+html.escape(data['title'])+' — MJ</title><style>'+css+'</style></head><body><div class="brewRenderer"><div class="pages" lang="fr">'+paper+'</div></div></body></html>',wait_until='load')
   await page.evaluate('document.fonts.ready')
   path=ROOT/'site'/filename.replace('.html','.pdf')
   await page.pdf(path=str(path),width='215.9mm',height='279.4mm',print_background=True,prefer_css_page_size=True,margin={'top':'0','right':'0','bottom':'0','left':'0'})
   pdf=PdfReader(path);counts=[len(p.extract_text().split()) for p in pdf.pages]
   assert len(pdf.pages)==len(pages),(filename,len(pdf.pages),len(pages))
   assert all(n>100 for n in counts),(filename,counts)
   report={'file':str(path),'pages':len(pdf.pages),'page_words':counts,'bytes':path.stat().st_size}
   print(json.dumps(report,ensure_ascii=False),flush=True);reports.append(report)
   await page.close()
  await browser.close()
 report_path=ROOT/'sources/site/preludes/verification/pdf-report.json'
 if only and report_path.exists():
  updated={r['file'] for r in reports};reports=[r for r in json.loads(report_path.read_text()) if r['file'] not in updated]+reports
 report_path.write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--only',choices=['cavernes','alaor']);args=parser.parse_args();asyncio.run(main(args.only))
