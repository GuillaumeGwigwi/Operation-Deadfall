# Livres des préludes — MJ uniquement

## Livraisons actives

- `/home/gwi/Operation-Deadfall/site/prelude-cavernes-du-chaos-mj.html` — Les Cavernes du Chaos, 22 pages, 15 illustrations, 64 lieux.
- `/home/gwi/Operation-Deadfall/site/prelude-dragon-d-alaor-mj.html` — Le Dragon d’Alaor, 19 pages, 14 illustrations, 39 lieux.
- `/home/gwi/Operation-Deadfall/site/prelude-cavernes-du-chaos-mj.pdf`
- `/home/gwi/Operation-Deadfall/site/prelude-dragon-d-alaor-mj.pdf`

Les HTML fonctionnent chacun seuls, hors connexion. Les PDF contiennent les livres entiers, pas une impression du shell. Tous ces fichiers contiennent des secrets MJ et des adaptations proposées ; ne pas les envoyer aux joueurs.

## Livre continu

### Version avec chronologie et présages

Chaque livre contient désormais « Mener le prélude », le contexte du pouvoir thayen, les étapes de préparation et de conduite, les présages et leurs rappels conditionnels, ainsi qu’une introduction encadrée à lire aux joueurs en page 3. Les Cavernes commencent le 12 Mirtul 1483 CV ; Alaor le 8 Eleasis 1491 CV. Ces dates sont proposées pour la campagne. La source situe le présent en 1501 CV et l’ouverture d’Operation Deadfall au 1er Tarsakh, après le rétablissement du Conseil en 1478 CV. Les références et réserves de datation sont dans les annexes des livres eux-mêmes.

Szass Tam est annoncé chez Yelena, par le brouillon non envoyé d’Ivlis et par une conversation d’Orso. Il n’est pas le commanditaire des antagonistes locaux. À Alaor, une rencontre commerciale avec Wynston Wrynn prépare des retrouvailles sans révéler son métier d’espion ni antidater une opération de Thrul. La rencontre ancienne et ses circonstances sont des ajouts explicites, pas des faits de la source.

Les livraisons de cette version ont été reconstruites et contrôlées : texte rendu sans perte, 103 repères conservés, CSS officiel inchangé, HTML isolés hors connexion, mobile 390/650 px, titres non isolés, positions du texte des PDF sans débordement. Les planches des 41 pages ont été examinées ; après correction, le titre et l’encadré de chaque introduction restent ensemble. Rendus de revue : `verification/presages/`. Les comptes de pages et empreintes actuels figurent dans les rapports de build, de PDF et de contrôle final ; les revues d’illustration plus anciennes décrivent leurs versions historiques.

Une seule séquence de pages est composée pour chaque aventure. Chapitres et salles partagent sa pagination. Toutes les pages restent dans le même document du lecteur : le sommaire et les résultats de recherche conduisent au passage concerné, sans remplacer le livre par une fiche indépendante. Le lecteur permet le défilement continu, la page précédente/suivante, le zoom ajusté/100 %, les liens profonds et l’impression de tout le livre.

La recherche porte sur les titres et le corps des passages, indépendamment de la casse et des accents. Les filtres distinguent chapitres et repères de salles ; ils ne suppriment pas les pages du livre. Sur mobile, seul le sommaire se replie, pas la recherche.

## Sources et rendu

Sources actives, choisies explicitement par le convertisseur :

- `sources/propositions/preludes-thay/01-les-cavernes-du-chaos.homebrewery.md`
- `sources/propositions/preludes-thay/02-le-dragon-d-alaor.homebrewery.md`

Le convertisseur utilise `marked-hbfm`. La pagination est mesurée dans Chromium avec les vraies polices chargées et le CSS officiel Homebrewery V3/PHB intégral. Plusieurs rencontres peuvent partager une page ; les titres ne déclenchent pas de nouvelle fiche.

Le style officiel est isolé dans un iframe, sans CSS documentaire personnalisé. Le bundle embarqué décomprimé est comparé octet par octet au fichier officiel local. Aucun changement des polices, marges, colonnes ou ornements pour faire tenir le texte. Le shell de navigation est distinct. Les PDF utilisent exactement ce même CSS et ces mêmes pages, au format natif du thème.

## Reconstruction

Depuis `/home/gwi/Operation-Deadfall` :

    uv run --with playwright --with beautifulsoup4 python3 tools/build_preludes.py
    sources/.venv/bin/python tools/verify_prelude_content.py
    uv run --with playwright --with beautifulsoup4 --with pypdf python3 tools/export_prelude_pdfs.py

Prérequis du build : Node, `marked-hbfm` dans `tools/homebrewery/node_modules`, Chromium Playwright dans le cache local. Rien de cela n’est nécessaire pour lire les HTML livrés ; un navigateur récent prenant en charge `DecompressionStream` suffit.

## Vérifications

- `tests/test_prelude_sites.py` : fichiers autonomes, style officiel inchangé, références des 64 et 39 salles, empreinte des sources courantes.
- `tests/test_prelude_continuous.py` : un livre par fichier, pagination globale, absence de pages de rubrique quasi vides.
- `tests/test_prelude_semantic_pagination.py` : titres non isolés et non fragmentés entre colonnes, introductions liées aux titres, sections courtes conservées, utilisation des deux colonnes.
- `tests/test_prelude_pdf_layout.py` : contrôle des positions des caractères dans les vrais PDF imprimés ; pas de texte passant dans une troisième colonne. Les lettrines décoratives officielles peuvent déborder légèrement à gauche.
- `tests/test_prelude_all_pages.py` : toutes les pages sont présentes dans le même lecteur.
- `tests/test_prelude_cached_reader.py` et `test_prelude_links.py` : réutilisation du document, liens et retour à l’ouverture après un fragment inconnu.
- `tests/test_prelude_browser.py` : copie de chaque HTML seule dans un répertoire temporaire, réseau désactivé, navigation de toutes les salles, toutes les pages inspectées pour les débordements, recherche, filtres, absence de résultat, zoom, clavier, mobile 390/650 px, captures.
- `tests/test_prelude_final.py` : nouveau contrôle des octets finaux après corrections éditoriales et typographiques ; navigation des 103 repères via leurs boutons, ancrages, document conservé, toutes les colonnes, mobile et réseau. Le rapport garde les empreintes des versions testées.
- `tools/verify_prelude_content.py` : correspondance avec les deux HTML originaux et comparaison intégrale du texte rendu avant/après pagination, sans perte.
- Export PDF : compte des pages comparé au livre HTML et extraction du texte de chaque page ; aucune page vide. Les fins d’annexes peuvent naturellement ne pas remplir les deux colonnes.
- Régression du site politique : `tests/test_politics_tharchs.py`.

Rapports : `build-report.json`, `verification/browser-report.json`, `verification/final-report.json`, `verification/pdf-report.json`, et `sources/propositions/preludes-thay/verification.json`. Captures navigateur et rendus de contrôle PDF dans `verification/`.

## Limites et historique

Les cartes et illustrations liées dans les éditions originales sont encore absentes du dossier raw des Cavernes lors du dernier contrôle. Quinze illustrations générées spécialement pour les Cavernes sont maintenant intégrées : les cinq images initiales, conservées à l’identique, et les dix compléments du programme validé par le MJ. Elles ne remplacent pas les plans exacts. Certains profils et l’annexe A des récompenses des Cavernes ne sont pas inclus dans les extraits fournis. Le récit et le rendu ne remplacent pas ces ressources : les annexes des livres disent précisément ce que le MJ doit préparer.

## Illustrations des Cavernes

Les panoramas occupent la largeur de page avec la classe officielle `wide` ; les portraits sont des vignettes de colonne avec la classe officielle `block`. Les bords picturaux sont estompés dans les fichiers WebP eux-mêmes, avec une vraie transparence. Seules les dimensions d’images sont déclarées dans le manuscrit ; le thème, les colonnes et les polices ne changent pas. Les images sont intégrées en URI `data:` dans le HTML et dans le rendu PDF.

Génération réelle : GPT Image 2, qualité haute, fournisseur OpenAI Codex déjà disponible. Références locales : illustration régionale de Gauros et illustration des Mages Rouges. Les visages et détails non décrits sont des interprétations artistiques, pas des portraits officiels ni une nouvelle carte canonique.

Originaux, briefs et manifestes privés : `sources/propositions/preludes-thay/illustrations/`. Copies PNG seules sans métadonnées : `site/illustrations-cavernes-joueurs/`. Aucun brief, fichier JSON, texte MJ ou légende révélatrice n’est placé dans ce dossier joueurs. Le MJ choisit quand montrer chaque image ; ne pas projeter les pages du livre avec leurs secrets.

Préparation reproductible, sans relancer de génération : `tools/prepare_prelude_art.py`, puis le build et l’export PDF habituels. `tests/test_prelude_art.py` contrôle les quinze images embarquées, leur transparence et les copies joueurs. `tests/test_prelude_pagination_art.py` vérifie qu’une image trop haute est refusée (exécution avec `--with playwright --with beautifulsoup4`). La vérification de débordement navigateur inclut les images. Toutes les pages illustrées ont été rendues en PNG et examinées ; emplacements dans `verification/art-placements.json`, rendus dans `verification/pdf-art/`. `tools/verify_prelude_art_complements.py` vérifie les dix ajouts, la conservation exacte du récit et les empreintes des cinq illustrations antérieures ; exécution avec `--with beautifulsoup4 --with pillow`.

## Illustrations du Dragon d’Alaor

Même traitement éditorial que les Cavernes : livre continu et thème officiel intégral, portraits en colonne et panoramas `wide`, contours transparents préparés dans les images. Quatorze illustrations : la vue fournie d’Ala Harbor, recadrée hors de son cadre éditorial, et treize créations haute qualité avec le fournisseur existant. Le port d’origine est conservé sans modification. Les apparences non attestées sont des interprétations artistiques. Mirel est recadrée pour le livre afin de partager sa page avec Orso ; l’image autonome complète reste disponible.

Les fonds d’Ashlyn, Devi, Anish, de l’atelier et des joueurs de cartes ont été corrigés pour retirer des fenêtres maritimes non décrites. Les secrets, les formes cachées et les solutions ne figurent pas dans les copies seules. Aucun accès fictif ne doit être déduit de ces illustrations, qui ne remplacent pas les plans originaux toujours absents du raw d’Alaor.

Sources et rapports privés : `sources/propositions/preludes-thay/illustrations-alaor/` ; voir `revue-mj.md` pour les emplacements et `verification-mj.json` pour les mesures. Copies PNG seules sans métadonnées : `site/illustrations-alaor-joueurs/`. Montrer chaque image lors de la découverte correspondante, pas le dossier complet à l’avance. Le livre HTML et le PDF restent MJ.

Reconstruction ciblée, sans génération et sans réécrire les livraisons des Cavernes :

    uv run --with pillow python3 tools/prepare_prelude_art.py --art-dir sources/propositions/preludes-thay/illustrations-alaor
    uv run --with playwright --with beautifulsoup4 python3 tools/build_preludes.py --only alaor
    uv run --with playwright --with beautifulsoup4 --with pypdf python3 tools/export_prelude_pdfs.py --only alaor

`tests/test_alaor_art.py` vérifie les quatorze images, leur transparence, le nettoyage des copies, la conservation exacte du récit antérieur et les empreintes inchangées des livraisons des Cavernes. `tools/render_alaor_review.py` agrège les emplacements, les tailles et les contrôles, puis rend toutes les pages et des planches dans `verification/alaor-illustre/` ; exécution avec `--with beautifulsoup4 --with pillow --with pypdfium2`. Les seize pages finales ont été examinées ; aucun titre isolé ni débordement du texte dans le PDF n’est détecté. Le lecteur final a été testé en copie isolée hors réseau, sur les trente-neuf repères et aux largeurs mobiles 390/650 px.

Les niveaux et le nombre de séances sont des cibles proposées, pas un équilibrage garanti. Les nouveaux événements n’entrent pas dans le canon avant validation et jeu.

Les premiers textes et HTML refusés ont été déplacés dans `sources/propositions/preludes-thay/archives/brouillons-refuses-v1/`. Ils ne sont plus générés ni importés par le pipeline actif. Aucune publication, aucun commit ni push n’a été effectué.
