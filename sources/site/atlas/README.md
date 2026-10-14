# Sources d’édition de l’atlas de Thay

Le livrable joueurs est uniquement `site/atlas-de-thay.html`, à la racine du projet. Ce fichier HTML autonome contient CSS, JavaScript, 46 notices, un guide de Thay et cinq images. Il fonctionne hors connexion, sans serveur ni fichiers voisins. Ne transmettre ni ce dossier de travail ni les audits MJ.

## Édition et génération

Les 47 textes français sont conservés dans `sources/homebrewery/atlas-joueurs/`. Leur syntaxe Homebrewery V3 est validée et convertie avec le moteur réel `marked-hbfm`, version verrouillée 1.0.1. Les styles restent ceux de Dossier écarlate : ce n’est ni l’éditeur Homebrewery complet ni son système de pagination.

Depuis la racine du projet, à la première installation :

    npm ci --ignore-scripts --prefix tools/homebrewery

Après modification des notices Markdown :

    node tools/homebrewery/render_atlas.mjs
    python3 tools/build_atlas.py

Le premier script valide chaque Markdown puis régénère le HTML des 46 fiches et du guide dans `atlas-data.js`. Le second assemble le fichier autonome ; il ne reconvertit pas les Markdown à lui seul. Node est nécessaire pour l’édition, pas pour consulter le livrable.

Pour réappliquer le relevé géographique :

    python3 tools/apply_atlas_positions.py
    python3 tools/build_atlas.py

## Sources d’interface

- `index.template.html` : structure avant intégration des ressources.
- `atlas.css` : styles et mode lecture agrandi.
- `atlas.js` : carte, recherche dans les notices, filtres, navigation et sommaire.
- `atlas-data.js` : données publiques et HTML Homebrewery précalculé.
- `positions.json` : relevé des 46 ancres à la résolution originale, contrôlé par l’empreinte du fond.
- `assets/` : carte de Thay, plan joueurs d’Eltabbar et trois illustrations approuvées ; images réencodées sans EXIF ni commentaires.

Les images sont intégrées une seule fois. Le guide et les recadrages réutilisent la carte embarquée.

## Périmètre du chapitre 1

Les onze provinces, leurs capitales, les autres localités décrites, les routes et les paysages ont des notices enrichies. Les seize ajouts sont les deux îles d’Alaor, Denzar, Gauros Keep, la Citadelle et les onze autres villes nommées dans la description de Tyraturos. Les repères urbains suivent les symboles du fond ; les ancres régionales désignent des zones, pas des points d’agglomérations.

Eltabbar regroupe ses dix quartiers et leurs établissements dans une fiche longue, avec plan joueurs et accès par sommaire. Aucune position de quartier n’est inventée sur la carte nationale.

Le bouton Guide de Thay rassemble relief, climat, institutions, lois, société, cultes, commerce, péages et repères historiques. Les références à des pays voisins et aux enclaves éloignées y figurent sans faux repères hors de la carte.

L’enrichissement porte sur les informations partageables : profils de jeu, secrets, motivations cachées, tables MJ et révélations d’aventure restent exclus. L’autorisation antérieure du fond de Thay ne vaut pas autorisation des secrets du texte.

Les audits détaillés sont séparés dans `sources/propositions/atlas-chapitre1-mj/`. Ils contiennent des décisions d’exclusion et donc des secrets ; ils ne sont pas embarqués et ne doivent pas être envoyés aux joueurs. Ils indiquent les fichiers et lignes des sources utilisés, sans numéros de pages inventés. Certaines lignes mêlent contenu public et privé : seuls leurs faits publics sont reformulés.

La carte imprimée comporte encore des noms que le chapitre ne décrit pas individuellement. Les 46 notices ne prétendent pas rendre tous les noms imprimés cliquables ni inventer des informations manquantes.

## Mode lecture

Agrandir ouvre la fiche presque plein écran. Réduire ramène au panneau, Fermer le ferme. Échap réduit d’abord le mode lecture puis peut fermer le panneau. Le sommaire mène aux sections et sous-sections, notamment aux quartiers d’Eltabbar. En mode agrandi, l’arrière-plan est inerte et la navigation au clavier reste dans la fiche ; les boutons restent accessibles lors du défilement. Sur mobile, le texte passe avant l’image.

## Vérifications

    python3 tests/test_atlas_chapter1.py
    python3 tests/test_atlas_review.py
    python3 tests/test_atlas_static.py
    python3 tests/test_atlas_standalone.py
    uv run --with playwright python3 tests/test_atlas_reader.py
    uv run --with playwright python3 tests/test_atlas_browser.py

Les contrôles navigateur copient seulement le HTML dans un dossier vide et le renomment, refusent les ressources externes, ouvrent toutes les notices, vérifient les ancres après zoom/déplacement et sur mobile, puis contrôlent le mode lecture, le sommaire et la recherche dans le contenu.

## Alerte du convertisseur local

L’audit npm de cette installation signale une vulnérabilité critique d’`expr-eval`, transitive via `marked-variables` et `marked-hbfm`, sans correction proposée pour cette chaîne verrouillée. La conversion a porté uniquement sur les Markdown publics reformulés et revus dans ce projet. Ne pas utiliser ce convertisseur sur des Markdown externes non vérifiés. Ces paquets servent à la préparation locale et ne sont pas embarqués dans `site/atlas-de-thay.html` ; la consultation de l’atlas ne lance pas ce convertisseur. Cette distinction ne constitue pas une garantie de sécurité générale du paquet.

## Ressources et droits

Carte de Thay : Francesca Baerald. Plan d’Eltabbar : Gerralt Landman. Illustrations : Jeff Dee. Les crédits sont conservés dans les sources sans être affichés dans l’interface, conformément à la demande du MJ. Retirer leur affichage n’efface pas les droits. Partage privé avec le groupe ; les droits de publication ouverte sur Internet ne sont pas établis.
