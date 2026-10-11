import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {hbfm} from 'marked-hbfm/src/index.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const file=path.join(root,'sources/site/atlas/atlas-data.js');
const data=JSON.parse(fs.readFileSync(file,'utf8').replace(/^window.THAY_ATLAS = /,'').replace(/;\s*$/,''));
const documents=[...data.landmarks,data.guide].filter(Boolean);
for (const place of documents) {
  if (!/^[a-z0-9-]+$/.test(place.id)) throw Error('Identifiant invalide');
  const md=fs.readFileSync(path.join(root,'sources/homebrewery/atlas-joueurs',place.id+'.md'),'utf8');
  const errors=hbfm.validate(md);
  if (errors.length) throw Error(`${place.id}: ${JSON.stringify(errors)}`);
  const html=hbfm.render(md);
  if (!html.includes('class="block note"')) throw Error(`${place.id}: repères du voyageur manquants`);
  if (/<script|<iframe|https?:\/\/|\.\.\/|sources\//i.test(html)) throw Error(`${place.id}: ressource ou contenu non portable`);
  place.bodyHTML=html;
}
data.renderer='Homebrewery V3 — marked-hbfm 1.0.1';
fs.writeFileSync(file,'window.THAY_ATLAS = '+JSON.stringify(data,null,2)+';\n');
console.log(`${documents.length} documents Homebrewery validés et convertis : ${data.landmarks.length} lieux et un guide.`);
