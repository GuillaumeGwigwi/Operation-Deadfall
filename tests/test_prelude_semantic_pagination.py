"""Regression: a title must stay with its introduction, including across columns."""
import asyncio,json,sys
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from build_preludes import PAGINATE
AUDIT=r'''()=>{
 const issues=[];
 function ink(e){const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let t;while(t=w.nextNode()){if(!t.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(t);const b=[...r.getClientRects()].find(x=>x.width&&x.height);if(b)return b;}return e.querySelector('img')?.getBoundingClientRect()||e.getBoundingClientRect();}
 for(const h of document.querySelectorAll('.page h1,.page h2,.page h3')){
  const fragments=[...h.getClientRects()];if(fragments.length>1&&fragments.some(r=>Math.abs(r.left-fragments[0].left)>100))issues.push({title:h.textContent,reason:'Titre lui-même coupé entre deux colonnes'});
  let next=h.nextElementSibling;while(next&&/^H[1-6]$/.test(next.tagName))next=next.nextElementSibling;
  if(!next){issues.push({title:h.textContent,reason:'Titre sans introduction sur la page'});continue;}
  if(next.classList.contains('wide'))continue;
  const a=ink(h),b=ink(next);if(Math.abs(a.left-b.left)>100)issues.push({title:h.textContent,reason:'Titre et introduction dans des colonnes différentes'});
 }
 return issues;
}'''
async def main():
 async with async_playwright() as pw:
  exe=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))[-1]
  browser=await pw.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox']);page=await browser.new_page(viewport={'width':1200,'height':1300})
  css='.page{box-sizing:border-box;width:500px;height:400px;padding:20px;columns:2;column-gap:20px;column-fill:auto}.page p{margin:0}.page h3{margin:0;font-size:20px;line-height:24px}.block{display:inline-block;width:100%;break-inside:avoid}.columnSplit{break-after:column;visibility:hidden}'
  await page.set_content('<style>'+css+'</style><div class="page"></div>')
  result=await page.evaluate(PAGINATE,['<div class="block" style="height:320px">Texte précédent.</div>','<h3>La rencontre</h3>','<div class="block" style="height:100px">Introduction de la rencontre.</div>'])
  for fragment in result:
   await page.eval_on_selector('.page','(e,html)=>e.innerHTML=html',fragment)
   issues=await page.evaluate(AUDIT);assert not issues,issues
  print('Régression synthétique : titre et introduction restent ensemble.')
  await page.add_style_tag(content='.page h2{margin:0;font-size:20px;line-height:24px}')
  short=await page.evaluate(PAGINATE,['<div class="block" style="height:260px">Texte précédent.</div>','<h2 id="short-title">Section courte</h2>','<p style="height:40px">Introduction.</p>','<p id="short-end" style="height:80px">Fin de la section courte.</p>'])
  for fragment in short:
   await page.eval_on_selector('.page','(e,html)=>e.innerHTML=html',fragment)
   if await page.locator('#short-title').count():
    assert await page.locator('#short-end').count(), 'Une section courte doit rester entière sur sa page'
    assert await page.evaluate('()=>{const a=document.querySelector("#short-title").getBoundingClientRect();return [...document.querySelector("#short-end").getClientRects()].every(r=>Math.abs(r.left-a.left)<50);}'), 'Une section courte doit rester entière dans sa colonne'
  flow=await page.evaluate(PAGINATE,['<div class="block" style="height:350px">Fin normale de la première colonne.</div>','<div class="block" style="height:100px">Deuxième colonne.</div>'])
  assert len(flow)==1, 'La réserve impression ne doit pas vider la deuxième colonne'
  print('Régression synthétique : les petites sections H2 restent entières, les deux colonnes restent utilisables.')
  official=(ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
  await page.set_content('<style>'+official+'</style><div class="brewRenderer"><div class="pages"><div class="page"></div></div></div>')
  report=[]
  for name in ['prelude-cavernes-du-chaos-mj.html','prelude-dragon-d-alaor-mj.html']:
   soup=BeautifulSoup((ROOT/'site'/name).read_text(),'html.parser');data=json.loads(soup.select_one('#prelude-data').string);problems=[]
   for n,fragment in enumerate(data['documents'][0]['pages'],1):
    await page.eval_on_selector('.page','(e,html)=>e.innerHTML=html',fragment)
    await page.evaluate('async()=>{await document.fonts.ready;await Promise.all([...document.images].map(im=>im.decode()));}')
    problems.extend({'page':n,**issue} for issue in await page.evaluate(AUDIT))
   report.append({'file':name,'pages':len(data['documents'][0]['pages']),'orphan_titles':problems})
  target=ROOT/'sources/site/preludes/verification/semantic-pagination.json';target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps(report,ensure_ascii=False,indent=2));assert not any(r['orphan_titles'] for r in report)
  await browser.close()
asyncio.run(main())
