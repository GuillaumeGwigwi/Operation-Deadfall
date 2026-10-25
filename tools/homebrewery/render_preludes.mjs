import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {hbfm} from 'marked-hbfm/src/index.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const specs=[
 {id:'cavernes',title:'Les Cavernes du Chaos',region:'Gauros · Montagnes du Levant',level:'Niveau 3 proposé',source:'01-les-cavernes-du-chaos.homebrewery.md',file:'prelude-cavernes-du-chaos-mj.html'},
 {id:'alaor',title:'Le Dragon d’Alaor',region:'Alaor Minor · Port d’Ala',level:'Niveau 7 proposé',source:'02-le-dragon-d-alaor.homebrewery.md',file:'prelude-dragon-d-alaor-mj.html'}
];
const out=specs.map(spec=>{const md=fs.readFileSync(path.join(root,'sources/propositions/preludes-thay',spec.source),'utf8');const errors=hbfm.validate(md);if(errors.length)throw Error(JSON.stringify(errors));return {...spec,html:hbfm.render(md)};});
fs.mkdirSync(path.join(root,'sources/site/preludes'),{recursive:true});
fs.writeFileSync(path.join(root,'sources/site/preludes/rendered.json'),JSON.stringify(out));
console.log('Deux sources converties avec marked-hbfm, sans erreur.');
