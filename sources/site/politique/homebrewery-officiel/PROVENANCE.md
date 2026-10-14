# Homebrewery V3 — thème officiel 5e PHB, autonome

## Livraison

`/home/gwi/Operation-Deadfall/sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css`

Bundle CSS : 18 931 773 octets ; SHA-256 `3f001e220c7c10385d65ab9b741077e15f9dd624162814d0b8897aeee1156e5e`.

Le manifeste `provenance.json` donne chaque URL téléchargée, sa taille, son MIME, son SHA-256, les replis et les vérifications. 132 ressources distinctes, 154 occurrences URL en data URI, 43 déclarations @font-face. Aucune URL de ressource externe, aucun @import. Les règles et couleurs officielles sont conservées ; aucune imitation, aucun CSS maison, aucune modification de palette. Seuls les URL sont remplacés par les données téléchargées et des commentaires de provenance ajoutés. L'égalité des CSS originaux après inversion des substitutions a été vérifiée en mémoire.

## Sources officielles et ordre

1. https://homebrewery.naturalcrit.com/brewRenderer/brewRenderer.css
2. https://homebrewery.naturalcrit.com/themes/V3/Blank/style.css
3. https://homebrewery.naturalcrit.com/themes/V3/5ePHB/style.css

Le thème 5ePHB hérite de Blank. Le renderer contient le reset et les styles globaux nécessaires. Tous ces CSS sont de vrais fichiers distribués `text/css`, téléchargés avec succès. Les ressources principales sont celles distribuées par Homebrewery, pas des substituts visuels.

Dépôt technique : https://github.com/naturalcrit/homebrewery
Référence consultée : `01a14c2b00957ff4883193f8b7a3bd0e06346e0b`.
Version annoncée par le site : `3.24.1`. Le commit consulté n'est pas une preuve du commit déployé ; les empreintes des fichiers effectivement distribués sont l'autorité pour ce bundle.

Fichiers de référence : `themes/V3/5ePHB/settings.json`, `themes/V3/5ePHB/style.less`, `themes/V3/Blank/style.less`, `client/homebrew/brewRenderer/brewRenderer.jsx`, `client/homebrew/brewRenderer/brewRenderer.less`, `vitePlugins/generateAssetsPlugin.js`.

`phb.standalone.css` à la racine du dépôt et `scripts/phb.js` ne sont pas la livraison V3 choisie ici. L'ancienne URL `/homebrew/bundle.css` retourne actuellement une page HTML, même avec statut HTTP 200 : elle n'a pas été incorporée.

## Intégration HTML

Pour un véritable fichier HTML autonome, incorporer le contenu complet du bundle dans un `<style>` ; un `<link>` vers ce fichier reste hors ligne mais crée une dépendance à un second fichier.

Structure minimale recommandée, conforme aux classes officielles :

```html
<div class="brewRenderer">
  <div class="pages" lang="fr">
    <div class="page" id="p1">
      <h1>Province</h1>
      <p>Présentation.</p>
      <h2>Territoire</h2>
      <p>Texte.</p>
      <div class="note"><h5>Repère</h5><p>Texte.</p></div>
      <div class="pageNumber">1</div>
      <div class="footnote">PROVINCE</div>
    </div>
  </div>
</div>
```

`.page` remplace les classes maison `.hb-page`/`.hb-body`. Chaque page doit être enfant direct de `.pages` pour le dimensionnement et l'ombre du renderer. Aucun conteneur `.hb-body` nécessaire. Utiliser les éléments HTML attendus et les classes V3 officielles (`note`, `descriptive`, `monster`, `wide`, `columnSplit`, `columnWrapper`, `pageNumber`, `footnote`, etc.), sans wrappers décoratifs inventés. La parité du pied de page repose sur `.page:nth-child(even)` : ne pas intercaler d'autres enfants dans `.pages`.

Les dimensions officielles par défaut sont Letter, 215,9 × 279,4 mm ; padding 1,4 cm 1,9 cm 1,7 cm ; deux colonnes PHB de 8 cm avec intervalle 0,9 cm. `.brewRenderer` fournit un aperçu scrollable de hauteur 100vh avec padding supérieur 60px ; ce n'est pas une mise en page fluide responsive. `.pages.facing` et `.pages.flow` sont les modes officiels de présentation facultatifs ; `.facing.recto` place la première page à droite. Le bundle inclut les règles print officielles.

Les images et polices nécessaires au CSS sont déjà embarquées. Aucun moteur React ni serveur Homebrewery n'est nécessaire pour du HTML pré-rendu. En revanche ce CSS ne compile pas Markdown ni la syntaxe `{{...}}`, `\\page` ou `\\column` : le producteur doit fournir le HTML V3 et la pagination. Un saut de colonne utilise un élément `.columnSplit` ; les longues fiches doivent être réparties explicitement entre plusieurs `.page`. Le débordement est coupé par les règles officielles (`contain:strict`, `overflow:clip`).

## Limites et contrôles

- Le bundle contient tous les styles et ressources référencés, y compris masques aquarelle, icônes, polices et modes non utilisés par de simples fiches. Cela explique sa taille. Une duplication dans chaque fiche HTML autonome augmente fortement la taille totale.
- Les règles globales (`:root`, `html`, `body`, reset, `*`, classes d'icônes) sont officielles et non isolées. Éviter de mélanger avec les styles du site existant ; privilégier un document HTML distinct ou un iframe isolé, comme le renderer officiel. Un CSS maison plus spécifique ou chargé ensuite peut casser le rendu.
- La CSS PHB officielle est le thème « 5e PHB » de Homebrewery V3 ; elle ne constitue pas une preuve d'un thème graphique PHB 2024 distinct.
- Les trois fichiers TTF de fallback Font Awesome référencés par le CSS renvoient HTML sur Homebrewery. Ils ont été récupérés dans le dépôt officiel FortAwesome/Font-Awesome, tag 6.7.2, version indiquée dans les commentaires du CSS. Les WOFF2 primaires sont ceux réellement distribués par Homebrewery. Une comparaison additionnelle montre que les WOFF2 distribués ne sont pas identiques octet pour octet aux WOFF2 du tag upstream 6.7.2 : l'identité binaire/version réelle entre WOFF2 et TTF n'est donc pas prouvée. Ces TTF ne servent que de fallback ; cette limite est conservée explicitement plutôt que de prétendre à une équivalence.
- Toutes les ressources ont été réellement téléchargées ; les fausses réponses HTML rejetées ; signatures binaires vérifiées ; tous les data URI redécodés et leurs empreintes comparées au manifeste ; les SVG examinés pour références href/src externes, aucune trouvée.
- Vérification visuelle tentée mais bloquée : `browser-harness: chrome-not-running`, aucun navigateur pris en charge n'a pu être lancé. Aucun rendu navigateur ou PDF n'est prétendu vérifié. Tester dans Chrome/Chromium, notamment les colonnes, lettrines, débordements, :has(), et l'impression avec arrière-plans activés. Le site officiel recommande Chrome pour les PDF.
- Le CSS n'embarque pas les images placées dans le contenu HTML, les scripts éventuels ou les ressources de liens. Les intégrer séparément en data URI si le document doit être totalement autonome.
- Conserver les mentions de licence. MIT couvre le logiciel Homebrewery ; elle ne garantit pas les droits de tous les graphismes/polices tiers ni une autorisation commerciale de ressources D&D. Font Awesome indique Icons CC BY 4.0, Fonts SIL OFL 1.1, Code MIT. Les droits propres aux autres assets restent à contrôler avant redistribution commerciale.

## Licence du logiciel Homebrewery

Source : https://raw.githubusercontent.com/naturalcrit/homebrewery/01a14c2b00957ff4883193f8b7a3bd0e06346e0b/license

```text
MIT License

Copyright (c) 2016 Scott Tolksdorf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
