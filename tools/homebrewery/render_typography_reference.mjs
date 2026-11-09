import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {hbfm} from 'marked-hbfm/src/index.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const out=path.join(root,'sources/propositions/politique-thay-mj/recherche-style/typographie');
fs.mkdirSync(out,{recursive:true});
// Table component from NaturalCrit themes/V3/Blank/snippets.js (first rows).
// This private specimen is not part of the player's guide.
const md=`##### Character Advancement
| Experience Points | Level | Proficiency Bonus |
|:------------------|:-----:|:-----------------:|
| 0                 | 1     | +2                |
| 300               | 2     | +2                |
| 900               | 3     | +2                |
| 2,700             | 4     | +2                |

## Titre de section — H2
Texte témoin destiné à vérifier la distance native entre un titre et son premier paragraphe.

Autre paragraphe pour observer le rythme avant la sous-section suivante.

### Sous-section — H3
Texte témoin sous un titre à filet. La comparaison porte sur la hiérarchie et les espacements, pas sur une nouvelle feuille de styles.

### Deuxième sous-section
Le même composant conserve ses distances lorsque les éléments restent des voisins directs.
`;
const css=fs.readFileSync(path.join(root,'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css'),'utf8');
fs.writeFileSync(path.join(out,'homebrewery-composants.html'),`<!doctype html><html lang="fr"><meta charset="utf-8"><title>Échantillon privé des composants Homebrewery natifs</title><style>${css}</style><body><div class="brewRenderer"><div class="pages"><div class="page">${hbfm.render(md)}</div></div></div></body></html>`);
console.log(path.join(out,'homebrewery-composants.html'));
