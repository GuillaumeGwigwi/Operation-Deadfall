"""Build two private, standalone prelude readers with official Homebrewery CSS.
Run: uv run --with playwright --with beautifulsoup4 python3 tools/build_preludes.py
"""
import argparse,asyncio,base64,gzip,hashlib,html,json,re,subprocess
from pathlib import Path
from bs4 import BeautifulSoup,Tag
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/site/preludes'
CSS=ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css'
PAGINATE=r'''async (blocks)=>{
 const page=document.querySelector('.page');
 const pages=[];let nodes=[];
 function fits(){
  const b=page.getBoundingClientRect(),cs=getComputedStyle(page);
  // Reserve two lines at the end of the final column for paged printing.
  // The first column must remain fully usable; the official CSS is unchanged.
  const printGuard=2*(parseFloat(cs.lineHeight)||16);
  const right=b.right-parseFloat(cs.paddingRight)+1,bottom=b.bottom-parseFloat(cs.paddingBottom)+1;
  const middle=b.left+b.width/2;
  function outside(box){return box.right>right||box.bottom>bottom||(box.right>middle&&box.bottom>bottom-printGuard);}
  const walk=document.createTreeWalker(page,NodeFilter.SHOW_TEXT);
  let t;while(t=walk.nextNode()){
   if(!t.textContent.trim())continue;
   const r=document.createRange();r.selectNodeContents(t);
   for(const box of r.getClientRects())if(outside(box))return false;
  }
  for(const el of page.querySelectorAll('table,.block,img'))for(const b2 of el.getClientRects())if(outside(b2))return false;
  return true;
 }
 function put(){page.innerHTML=nodes.join('');}
 async function ready(){await Promise.all([document.fonts.ready,...[...page.querySelectorAll('img[src]')].map(im=>im.decode())]);}
 function commit(){if(nodes.length){pages.push(nodes.join(''));nodes=[];put();}}
 function descriptor(html){const t=document.createElement('template');t.innerHTML=html;const el=t.content.firstElementChild;return {html,tag:el.tagName,heading:/^H[1-6]$/.test(el.tagName),image:!!el.querySelector('img')||el.tagName==='IMG',wide:el.classList.contains('wide'),words:el.textContent.trim().split(/\s+/).filter(Boolean).length};}
 const ds=blocks.map(descriptor),units=[];
 for(let i=0;i<ds.length;){
  if(!ds[i].heading){units.push({blocks:[ds[i].html],heads:0,keepColumn:false});i++;continue;}
  const start=i;while(i<ds.length&&ds[i].heading)i++;
  const heads=i-start;
  if(i<ds.length){const image=ds[i].image;i++;if(image&&i<ds.length&&ds[i].tag==='P')i++;}
  let end=i;while(end<ds.length&&!ds[end].heading)end++;
  const candidate=ds.slice(start,end);
  const shortRoom=['H2','H3'].includes(ds[start+heads-1].tag)&&!candidate.some(d=>d.image||d.wide)&&candidate.reduce((n,d)=>n+d.words,0)<=150;
  if(shortRoom)i=end;
  units.push({blocks:ds.slice(start,i).map(d=>d.html),heads,keepColumn:shortRoom});
 }
 for(const unit of units){
  // Native Homebrewery blocks keep titles and short scenes together even
  // when a later full-width illustration rebalances the preceding columns.
  const wideIndex=unit.blocks.findIndex(html=>descriptor(html).wide);
  if(unit.heads&&wideIndex<0)unit.blocks=['<div class="block pagination-unit">'+unit.blocks.join('')+'</div>'];
  else if(unit.heads&&wideIndex===unit.heads){
   unit.blocks=['<div class="wide pagination-unit">'+unit.blocks.slice(0,wideIndex+1).join('')+'</div>',...unit.blocks.slice(wideIndex+1)];
  }
  const start=nodes.length;
  nodes.push(...unit.blocks);put();await ready();
  if(fits())continue;
  nodes.splice(start);put();commit();
  nodes=[...unit.blocks];put();await ready();
  if(!fits())throw Error('Block larger than an official page: '+page.textContent.slice(0,120));
 }
 commit();return pages;
}'''

def documents(spec):
    """Keep all chapters in one flow; map each heading into that same book."""
    soup=BeautifulSoup(spec['html'],'html.parser')
    source_dir=ROOT/'sources/propositions/preludes-thay'
    for image in soup.select('img'):
        src=image.get('src','')
        if src.startswith('data:image/'):
            continue
        path=(source_dir/src).resolve()
        if not path.is_relative_to(ROOT) or path.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):
            raise ValueError('Illustration locale autorisée attendue : '+src)
        mime={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'}[path.suffix.lower()]
        image['src']='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
    for node in list(soup.select('p')):
        if node.get_text(strip=True) in ('\\page','\\column'):
            node.decompose()
    entries=[]
    for node in list(soup.children):
        if not isinstance(node,Tag) or node.name not in ('h1','h2','h3'):
            continue
        title=node.get_text(' ',strip=True)
        room=re.search(r'\(((?:[A-K]|M)\d+)\)$',title)
        if node.name=='h3' and not room:
            continue
        anchor=f'book-entry-{len(entries):03d}'
        node['id']=anchor
        level=int(node.name[1]);texts=[]
        for sibling in node.next_siblings:
            if isinstance(sibling,Tag) and re.fullmatch(r'h[1-6]',sibling.name) and int(sibling.name[1])<=level:
                break
            texts.append(sibling.get_text(' ',strip=True) if isinstance(sibling,Tag) else str(sibling))
        entries.append({'id':f'e{len(entries):03d}','anchor':anchor,'kind':'room' if room else 'topic','key':room.group(1) if room else None,'title':title,'text':' '.join(texts),'document':0})
    blocks=[str(n) for n in soup.children if isinstance(n,Tag)]
    return [{'title':spec['title'],'blocks':blocks,'entries':entries}]

async def build(only=None):
    subprocess.run(['node',str(ROOT/'tools/homebrewery/render_preludes.mjs')],check=True,cwd=ROOT)
    specs=json.loads((SOURCE/'rendered.json').read_text())
    if only:specs=[spec for spec in specs if spec['id']==only]
    if not specs:raise ValueError('Prélude inconnu')
    css=CSS.read_text();encoded=base64.b64encode(gzip.compress(css.encode(),mtime=0)).decode()
    report=[]
    async with async_playwright() as pw:
        exes=sorted(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
        browser=await pw.chromium.launch(executable_path=str(exes[-1]),headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1200,'height':1300})
        await page.set_content('<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>'+css+'</style></head><body><div class="brewRenderer"><div class="pages"><div class="page"><h1>Document</h1><p>Texte de mesure avec les polices officielles.</p></div></div></div></body></html>')
        await page.evaluate('document.fonts.ready')
        for spec in specs:
            docs=documents(spec);entries=[]
            for i,doc in enumerate(docs):
                book_entries=doc.pop('entries')
                pages=await page.evaluate(PAGINATE,doc.pop('blocks'))
                doc['pages']=pages
                doc['text']=BeautifulSoup(' '.join(pages),'html.parser').get_text(' ',strip=True)
                anchors={}
                for pi,fragment in enumerate(pages):
                    for heading in BeautifulSoup(fragment,'html.parser').select('[id]'):
                        anchors[heading['id']]=pi
                for entry in book_entries:
                    entry['page']=anchors[entry['anchor']]
                    entries.append(entry)
            data={'id':spec['id'],'title':spec['title'],'audience':'MJ','source_sha256':hashlib.sha256((ROOT/'sources/propositions/preludes-thay'/spec['source']).read_bytes()).hexdigest(),'entries':entries,'documents':docs}
            template=(SOURCE/'index.template.html').read_text()
            payload={'TITLE':html.escape(spec['title']),'REGION':html.escape(spec['region']),'LEVEL':html.escape(spec['level']),'CSS':(SOURCE/'reader.css').read_text(),'DATA':json.dumps(data,ensure_ascii=False).replace('<','\\u003c'),'OFFICIAL':encoded,'JS':(SOURCE/'reader.js').read_text()}
            for key,value in payload.items():template=template.replace('@@'+key+'@@',value)
            assert not re.search(r'@@[A-Z]+@@',template)
            target=ROOT/'site'/spec['file'];target.write_text(template,encoding='utf-8')
            report.append({'file':str(target),'bytes':target.stat().st_size,'documents':len(docs),'pages':sum(len(d['pages']) for d in docs),'rooms':sum(e['kind']=='room' for e in entries),'official_css_sha256':hashlib.sha256(css.encode()).hexdigest(),'pagination':'Measured with official CSS and loaded fonts in Chromium'})
            print(json.dumps(report[-1],ensure_ascii=False))
        await browser.close()
    report_path=SOURCE/'build-report.json'
    if only and report_path.exists():
        updated={r['file'] for r in report};report=[r for r in json.loads(report_path.read_text()) if r['file'] not in updated]+report
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--only',choices=['cavernes','alaor']);args=parser.parse_args();asyncio.run(build(args.only))
