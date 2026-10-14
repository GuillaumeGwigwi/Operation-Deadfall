import fs from 'node:fs';
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
for (const {id,name,ruler,capital} of data.provinces) {
  if (!/^[a-z0-9-]+$/.test(id)) throw Error('Identifiant provincial invalide');
  const md=fs.readFileSync(path.join(src,'tharchs',id+'.md'),'utf8');
  const errors=hbfm.validate(md);
  if (errors.length) throw Error(`${id}: ${JSON.stringify(errors)}`);
  const html=hbfm.render(md).replace(/ id="[^"]*"/g,'');
  if (!html.startsWith(`<h1>${name}</h1>`) || !html.includes(ruler) || !html.includes(capital)) throw Error(`${id}: province, gouverneur ou capitale manquants`);
  if (!html.includes('class="block note"') || /<script|<iframe|<img|style=|https?:\/\/|\.\.\/|sources\//i.test(html)) throw Error(`${id}: fiche non valide ou non portable`);
  tharchs[id]=html;
}
const practiceMd=fs.readFileSync(path.join(src,'pratique.md'),'utf8');
const practiceErrors=hbfm.validate(practiceMd);
if (practiceErrors.length) throw Error(JSON.stringify(practiceErrors));
const practice=hbfm.render(practiceMd).replace(/ id="[^"]*"/g,'');
if (!practice.startsWith('<h1>En pratique</h1>') || (practice.match(/PRACTICE_IMAGE/g)||[]).length!==1 || /<script|<iframe|https?:\/\/|\.\.\//i.test(practice)) throw Error('Page pratique invalide');
for (const situation of data.situations) if (!practice.includes(situation.body)) throw Error('Situation manquante : '+situation.id);
const out={renderer:'Homebrewery V3 — marked-hbfm 1.0.1',fiches,tharchs,practice};
fs.writeFileSync(path.join(src,'fiches-data.json'),JSON.stringify(out,null,1)+'\n');
console.log(`${council.length} fiches zulkirs et ${data.provinces.length} fiches tharchs et une page En pratique Homebrewery validées et converties dans fiches-data.json.`);
