import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {hbfm} from 'marked-hbfm/src/index.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const src=path.join(root,'sources/site/politique');
const data=JSON.parse(fs.readFileSync(path.join(src,'public-data.json'),'utf8'));
const council=data.council;
const fiches={};
for (const {id,name} of council) {
  if (!/^[a-z0-9-]+$/.test(id)) throw Error('Identifiant invalide');
  const md=fs.readFileSync(path.join(src,'fiches',id+'.md'),'utf8');
  const errors=hbfm.validate(md);
  if (errors.length) throw Error(`${id}: ${JSON.stringify(errors)}`);
  // Les fiches sont affichées une à une dans le même lecteur : les ancres générées feraient doublon.
  const html=hbfm.render(md).replace(/ id="[^"]*"/g,'');
  if (!html.startsWith(`<h1>${name}</h1>`)) throw Error(`${id}: titre attendu « ${name} »`);
  if (id !== 'invocation' && !html.includes('class="block note"')) throw Error(`${id}: charges personnelles manquantes`);
  if (/<script|<iframe|<img|style=|https?:\/\/|\.\.\/|sources\//i.test(html)) throw Error(`${id}: ressource ou contenu non portable`);
  fiches[id]=html;
}
const tharchs={};
const regionImages=JSON.parse(fs.readFileSync(path.join(src,'region-images.public.json'),'utf8'));
const escapeHtml=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const figureFor=(key,wide=false)=>{
  const image=regionImages[key];
  if(!image)return '';
  if(image.file!==`assets/regions/${key}.webp`)throw Error('Chemin image non approuvé');
  const bytes=fs.readFileSync(path.join(src,image.file));
  if(bytes.toString('ascii',8,12)!=='WEBP')throw Error('Format image non valide');
  return `<figure class="${wide?'wide':'block'}"><img src="data:image/webp;base64,${bytes.toString('base64')}" alt="${escapeHtml(image.caption)}" style="width:100%;height:auto"><figcaption>${escapeHtml(image.caption)}<br>${key.endsWith('-map')?'Cartographie':'Illustration'} : ${escapeHtml(image.credit)}</figcaption></figure>`;
};
for (const {id,name,ruler,capital} of data.provinces) {
  if (!/^[a-z0-9-]+$/.test(id)) throw Error('Identifiant provincial invalide');
  const md=fs.readFileSync(path.join(src,'tharchs',id+'.md'),'utf8');
  const errors=hbfm.validate(md);
  if (errors.length) throw Error(`${id}: ${JSON.stringify(errors)}`);
  const html=hbfm.render(md).replace(/ id="[^"]*"/g,'');
  if (!html.startsWith(`<h1>${name}</h1>`) || !html.includes(ruler) || !html.includes(capital)) throw Error(`${id}: province, gouverneur ou capitale manquants`);
  if (!html.includes('class="block note"') || /<script|<iframe|<img|style=|https?:\/\/|\.\.\/|sources\//i.test(html)) throw Error(`${id}: fiche non valide ou non portable`);
  // Transpose the source definition list, verbatim, into a useful PHB table.
  let composed=html.replace(/<div class="block note"><h5>(.*?)<\/h5>\s*<dl>(.*?)<\/dl><\/div>/s, (_,title,definitions)=>{
    const rows=[...definitions.matchAll(/<dt>(.*?)<\/dt><dd>(.*?)<\/dd>/gs)];
    if(!rows.length)throw Error(`${id}: empty provincial reference table`);
    // Match the native Blank/snippets.js Table: h5 caption, then Markdown
    // alignment markers. Both columns contain prose, not centred quantities.
    const tableMd=`##### ${title}\n| Repère | Information |\n|:---|:---|\n${rows.map(([,label,value])=>`| ${label} | ${value} |`).join('\n')}\n`;
    return hbfm.render(tableMd).replace(/ id="[^"]*"/g,'').replace(/<th align=left>/g,'<th align=left scope="col">');
  });
  if(regionImages[id]) {
    const image=regionImages[id];
    const bytes=fs.readFileSync(path.join(src,image.file));
    // Native edge mask: only the sky/background meets the text. The foreground,
    // original decorative border and signatures remain intact at the page edge.
    const settings={eltabbar:[740,0,510],delhumide:[600,-80,566],pyarados:[700,-60,530],thaymount:[520,-170,670]};
    const [artWidth,offset,captionTop]=settings[id]||[816,-100,580];
    const art=`<div class="imageMaskEdge1 bottom" data-page-art style="--offset:${offset}px"><p><img src="data:image/webp;base64,${bytes.toString('base64')}" alt="${escapeHtml(image.caption)}" style="width:${artWidth}px;height:auto;left:${816-artWidth}px;bottom:0"></p></div>`;
    const captionPosition=id==='eltabbar'?'top:470px;left:72px;width:320px':id==='thaymount'?'top:720px;left:72px;width:200px':`top:${captionTop}px;left:72px;width:672px`;
    const caption=`<div class="artist" style="${captionPosition}"><p>${escapeHtml(image.caption)}<br>Illustration : ${escapeHtml(image.credit)}</p></div>`;
    composed=composed.replace(/^(<h1>.*?<\/h1>)/,`<div class="wide">$1</div>${art}${caption}`);
  }
  if(id==='eltabbar') composed=composed.replace('<h2>Marchés, ateliers et vie quotidienne</h2>', '<div data-page-break></div>'+figureFor('eltabbar-map',false)+'<h2>Marchés, ateliers et vie quotidienne</h2>');
  // Regional subjects are compact subsections (native PHB ruled h3), not
  // chapter-sized h2s. A spanning title aligns both column starts, art or not.
  composed=composed.replace(/<(\/?)h2>/g,'<$1h3>');
  if(!regionImages[id]) composed=composed.replace(/^(<h1>.*?<\/h1>)/,'<div class="wide">$1</div>');
  tharchs[id]=composed;
}
const practiceMd=fs.readFileSync(path.join(src,'pratique.md'),'utf8');
const practiceErrors=hbfm.validate(practiceMd);
if (practiceErrors.length) throw Error(JSON.stringify(practiceErrors));
const practice=hbfm.render(practiceMd).replace(/ id="[^"]*"/g,'');
if (!practice.startsWith('<h1>En pratique</h1>') || (practice.match(/PRACTICE_IMAGE/g)||[]).length!==1 || /<script|<iframe|https?:\/\/|\.\.\//i.test(practice)) throw Error('Page pratique invalide');
for (const situation of data.situations) if (!practice.includes(situation.body)) throw Error('Situation manquante : '+situation.id);
const out={renderer:'Homebrewery V3 — marked-hbfm 1.0.1',fiches,tharchs,practice};
fs.writeFileSync(path.join(src,'fiches-data.json'),JSON.stringify(out,null,1)+'\n');
execFileSync('uv',['run','--with','playwright','python',path.join(root,'tools/paginate_politics.py')],{cwd:root,stdio:'inherit'});
console.log(`${council.length} fiches zulkirs et ${data.provinces.length} fiches tharchs et une page En pratique Homebrewery validées et converties dans fiches-data.json.`);
