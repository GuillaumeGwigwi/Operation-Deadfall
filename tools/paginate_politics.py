#!/usr/bin/env python3
"""Paginate public tharch HTML with the unmodified official CSS and real fonts.
Run through render_politics.mjs, or: uv run --with playwright python tools/paginate_politics.py
No estimates by character count: Chromium measures every candidate and text rectangle.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources/site/politique'
PAGINATE = r"""async html => {
 const page=document.querySelector('.page');page.replaceChildren();
 const source=document.createElement('div');source.innerHTML=html;
 const text=e=>e.textContent.replace(/\s+/g,'');
 const expected=text(source);
 const groups=[];
 for(const node of [...source.children]) {
   const last=groups.at(-1);
   if(last && /^H[1-6]$/.test(last.at(-1).tagName)) last.push(node);
   else groups.push([node]);
 }
 const ready=async()=>{await Promise.all([...page.querySelectorAll('img')].map(i=>i.decode()));await document.fonts.ready;};
 const overflow=(checkArtwork=false)=>{
   const box=page.getBoundingClientRect(),s=getComputedStyle(page);
   const bounds={left:box.left+parseFloat(s.paddingLeft),right:box.right-parseFloat(s.paddingRight),top:box.top+parseFloat(s.paddingTop),bottom:box.bottom-parseFloat(s.paddingBottom)};
   const bad=[];
   const check=(r,kind)=>{if(r.width && r.height && (r.right>bounds.right+1 || r.left<bounds.left-1 || r.bottom>bounds.bottom+1 || r.top<bounds.top-1))bad.push({kind,x:r.x,y:r.y,right:r.right,bottom:r.bottom,bounds});};
   const walker=document.createTreeWalker(page,NodeFilter.SHOW_TEXT);
   while(walker.nextNode()){if(!walker.currentNode.textContent.trim())continue;const range=document.createRange();range.selectNodeContents(walker.currentNode);for(const r of range.getClientRects())check(r,'text');}
   for(const image of page.querySelectorAll('img')){
     if(image.closest('[data-page-art]')){
       const r=image.getBoundingClientRect();
       if(r.left<box.left-1 || r.right>box.right+1 || r.top<box.top-1 || r.bottom>box.bottom+1)bad.push({kind:'page-art',x:r.x,y:r.y});
     }else check(image.getBoundingClientRect(),'image');
   }
   if(checkArtwork){
     const art=page.querySelector('[data-page-art]'),artist=page.querySelector('.artist');
     if(art){
       const r=art.querySelector('img').getBoundingClientRect();
       const ink={left:r.left,right:r.right,top:Math.max(r.top,box.top+508-parseFloat(art.style.getPropertyValue('--offset'))),bottom:r.bottom};
       const overlaps=(a,b)=>a.left<b.right-1&&a.right>b.left+1&&a.top<b.bottom-1&&a.bottom>b.top+1;
       const walker=document.createTreeWalker(page,NodeFilter.SHOW_TEXT);
       while(walker.nextNode()){
         const node=walker.currentNode;
         if(!node.textContent.trim()||node.parentElement.closest('[data-page-art]'))continue;
         const range=document.createRange();range.selectNodeContents(node);
         for(const rect of range.getClientRects()){
           if(overlaps(rect,ink))bad.push({kind:'text-art collision',text:node.textContent.slice(0,50)});
           if(artist&&!node.parentElement.closest('.artist')&&overlaps(rect,artist.getBoundingClientRect()))bad.push({kind:'credit collision'});
         }
       }
     }
   }
   return bad;
 };
 const pages=[];
 const finish=()=>{if(page.children.length){
   // Search semantic boundaries using the real layout, never CSS column-fill.
   const children=[...page.children];let best=null;
   for(let i=1;i<children.length;i++){
     if(/^H[1-6]$/.test(children[i-1].tagName))continue;
     if(children[i].classList.contains('wide') || children.slice(i).some(e=>e.classList.contains('wide')))continue;
     const split=document.createElement('div');split.className='columnSplit';children[i].before(split);
     if(!overflow().length){
       const box=page.getBoundingClientRect(), middle=box.left+box.width/2;
       const bottoms=[0,0];
       for(const el of page.querySelectorAll('p,h1,h2,h3,h5,table,figure,dl')){
         if(el.closest('.wide,[data-page-art],.artist'))continue;
         for(const r of el.getClientRects())bottoms[r.left<middle?0:1]=Math.max(bottoms[r.left<middle?0:1],r.bottom);
       }
       // Prefer a section opening over a marginally more even paragraph cut.
       const score=Math.abs(bottoms[0]-bottoms[1])+(/^H[23]$/.test(children[i].tagName)?0:20);
       if(bottoms.every(Boolean)&&(!best||score<best.score))best={i,score};
     }
     split.remove();
   }
   if(best){const split=document.createElement('div');split.className='columnSplit';children[best.i].before(split);}
   pages.push(page.innerHTML);page.replaceChildren();
 }};
 for(const original of groups){
   if(original[0].hasAttribute('data-page-break')){finish();continue;}
   let group=original;
   if(original[0].tagName==='H1' && original.at(-1).classList.contains('wide')){
     const opening=document.createElement('div');opening.className='wide';opening.append(...original);group=[opening];
   }
   // Keep title+paragraph as a pagination unit, but keep them DOM siblings:
   // native p+*, p+p, table+* and h3+* cannot cross a .block wrapper.
   page.append(...group);await ready();
   if(!overflow().length)continue;
   group.forEach(n=>n.remove());finish();page.append(...group);await ready();
   if(overflow().length){
     const paragraph=group.at(-1);
     if(paragraph.tagName!=='P' || group.slice(0,-1).some(n=>!/^H[1-6]$/.test(n.tagName)))throw Error('Unbreakable block exceeds an official page');
     paragraph.remove();
     const nodes=[];let length=0;
     const walker=document.createTreeWalker(paragraph,NodeFilter.SHOW_TEXT);
     while(walker.nextNode()){const node=walker.currentNode;nodes.push({node,start:length,end:length+node.length});length+=node.length;}
     const offsets=[0,...[...paragraph.textContent.matchAll(/\S+\s*/g)].map(m=>m.index+m[0].length)];
     const boundary=offset=>{const entry=nodes.find(n=>offset<=n.end);return [entry.node,offset-entry.start];};
     const fragment=(start,end)=>{const range=document.createRange();range.setStart(...boundary(start));range.setEnd(...boundary(end));const p=paragraph.cloneNode(false);p.append(range.cloneContents());return p;};
     let start=0;
     while(start<offsets.length-1){
       let low=start+1,high=offsets.length-1,best=start;
       while(low<=high){const mid=Math.floor((low+high)/2),part=fragment(offsets[start],offsets[mid]);page.append(part);await ready();const fits=!overflow().length;part.remove();if(fits){best=mid;low=mid+1;}else high=mid-1;}
       if(best===start)throw Error('No word fits in an official page');
       page.append(fragment(offsets[start],offsets[best]));start=best;
       if(start<offsets.length-1)finish();
     }
   }
 }
 finish();
 const joined=document.createElement('div');joined.innerHTML=pages.join('');
 if(text(joined)!==expected)throw Error('Pagination changed public text');
 const failures=[];
 for(let i=0;i<pages.length;i++){page.innerHTML=pages[i];await ready();failures.push(...overflow(true).map(r=>({page:i+1,...r})));}
 return {pages,failures};
}"""
def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', action='store_true', help='Capture complete pages without an iframe viewport')
    args = parser.parse_args()
    captures = SRC / 'verification/typography/after'
    if args.capture:
        captures.mkdir(parents=True, exist_ok=True)
        for previous in captures.glob('*.png'):
            previous.unlink()
    data = json.loads((SRC / 'fiches-data.json').read_text())
    css = (SRC / 'homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
    with sync_playwright() as pw:
        candidates = sorted((Path.home() / '.cache/ms-playwright').glob('chromium-*/**/chrome'))
        browser = pw.chromium.launch(executable_path=str(candidates[-1]) if candidates else None, headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1500, 'height': 1300})
        page.route('http**://**', lambda route: route.abort())
        page.set_content('<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>'+css+'</style></head><body><div class="brewRenderer"><div class="pages" lang="fr"><div class="page" id="p1"></div></div></div></body></html>')
        data['tharchPages'] = {}
        failures = []
        for key, html in data['tharchs'].items():
            result = page.evaluate(PAGINATE, html)
            data['tharchPages'][key] = result['pages']
            failures.extend({'region': key, **item} for item in result['failures'])
            if args.capture:
                for number, content in enumerate(result['pages'], 1):
                    page.evaluate('async html=>{document.querySelector(".page").innerHTML=html;await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));}', content)
                    page.locator('.page').screenshot(path=str(captures / f'{key}-{number}.png'))
        browser.close()
    if failures:
        raise RuntimeError(json.dumps(failures, ensure_ascii=False))
    data['pagination'] = {'engine': 'Chromium / official Homebrewery V3', 'overflow': failures, 'counts': {k: len(v) for k,v in data['tharchPages'].items()}}
    (SRC / 'fiches-data.json').write_text(json.dumps(data, ensure_ascii=False, indent=1)+'\n')
    print('Pagination vérifiée : '+json.dumps(data['pagination']['counts']))
if __name__ == '__main__':
    main()
