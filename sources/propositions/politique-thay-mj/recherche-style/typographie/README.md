# Comparaison typographique — tableaux et titres

Revue interne de composition ; ce document n'est pas embarqué dans le HTML joueur.

## Références réellement récupérées et examinées

- Wizards, *Player's Basic Rules* v0.2, 2014 : https://media.wizards.com/2014/downloads/dnd/PlayerDnDBasicRules_v0.2.pdf . Pages PDF 10, 43 et 53 examinées en image. Exemples : Character Advancement, Starting Wealth by Class, Standard Exchange Rates, Lifestyle Expenses. Ce sont les Basic Rules, pas une prétendue inspection de tous les livres reliés.
- NaturalCrit, composants natifs : https://github.com/naturalcrit/homebrewery/blob/master/themes/V3/Blank/snippets.js ; section Tables, snippet Table. Le snippet est rendu réellement avec le moteur installé et le CSS officiel embarqué, dans `homebrewery-composants.html`.
- NaturalCrit, variantes PHB : https://github.com/naturalcrit/homebrewery/blob/master/themes/V3/5ePHB/snippets.js . Les tableaux de classe avec cadre sont un autre composant ; leur ornementation n'est pas automatiquement appropriée à une courte table de gouvernement.

## Constats et décisions

1. Un titre de tableau et des en-têtes de colonnes ne sont pas interchangeables. Le livre montre un titre noir en petites capitales, puis des libellés plus petits et gras. Le composant Homebrewery emploie un `h5` avant le tableau. Dans la version précédente, Gouvernement devenait le nom de la seconde colonne et les titres des tableaux de zulkirs étaient des cellules fusionnées : mauvaise structure, malgré un CSS officiel.
2. Les libellés textuels s'alignent sur les valeurs. Le centrage est utile pour certaines colonnes numériques, pas une règle universelle. Deux colonnes textuelles adoptent l'alignement gauche natif proposé par la syntaxe Markdown `:---`.
3. Les espacements dépendent de la structure : `h5 + *`, `table + *`, `p + *` et `h3 + *` sont des règles du thème. Les enveloppes introduites par le paginateur peuvent rompre ces voisinages. La correction doit donc porter sur le DOM et la pagination, sans surcharger les marges CSS du thème.
4. La planche `comparaison-tableaux.png` rapproche un extrait de la page 43, le composant natif rendu et un tableau corrigé du guide. Les fontes de NaturalCrit imitent une famille graphique ; elles ne sont pas présentées comme les fichiers typographiques de Wizards.
5. Conserver les illustrations validées, les données et les proportions. Cette passe est typographique ; aucune nouvelle illustration ni nouveau fait de campagne n'est requis.

## Preuves

- `wotc-basic2014-p10.png`, `wotc-basic2014-p43.png`, `wotc-basic2014-p53.png` : références.
- `homebrewery-composants.png` : moteur réel, titre de tableau, H2 et H3.
- `comparaison-tableaux.png` : comparaison rapprochée.
- `sources.json` : URLs et empreinte du CSS.
- Avant : `sources/site/politique/verification/typography-before/`.
- Après : `sources/site/politique/verification/typography/` pour les régions ; `verification/council-composition/` pour les portraits.

Les captures servent à examiner le résultat ; les tests de géométrie et de conservation du texte ne remplacent pas cette comparaison.
