# Ressources locales — Operation Deadfall

Ressources de travail du MJ pour D&D 5e 2024. Les textes sources restent en anglais. Aucun événement de campagne n'est déduit de ces textes : ce sont les informations du livre, pas le journal de votre table.

## Chapitre importé

[Chapter 1: Thay, Dominion of Red Wizards](chapters/chapter-01-thay/README.md)

- `raw/chapter-01-thay.html` : HTML exact fourni dans la conversation, sans la phrase qui le précède.
- `chapters/chapter-01-thay/original.html` : copie de conservation du même HTML.
- `chapters/chapter-01-thay/chapter.md` : chapitre complet converti en Markdown avec ancres explicites.
- `chapters/chapter-01-thay/chapter.html` : page de lecture locale avec images locales et styles simples ; les scripts et commandes interactives du site sont supprimés.
- `sections/` : sections du chapitre, introduction comprise.
- `entities/zulkirs/`, `entities/tharchs/`, `entities/wards/` : extraits classés, non résumés et non traduits.
- `tables/` : tous les tableaux en CSV UTF-8 et JSON, également conservés dans le chapitre.
- `assets/illustrations/` : illustrations.
- `assets/maps/mj/` : cartes MJ.
- `assets/maps/players/` : fichiers explicitement présentés comme versions joueurs dans le HTML fourni. Leur présence ne rend pas le reste du dossier partageable.
- `manifest.json` : provenance, inventaire, crédits, légendes, URL originales, dimensions, tailles et empreintes SHA-256 des images.
- `links.json` : références vers les autres pages ; leur contenu n'a pas été téléchargé.

Tous les chemins ci-dessus à partir de `sections/` sont relatifs à `chapters/chapter-01-thay/`.

## Confidentialité et Git

Le chapitre et les fiches contiennent des secrets de MJ. La séparation MJ/joueurs est une convention de rangement, pas un contrôle d'accès.
Ces ressources protégées sont destinées à votre travail local : ne pas les publier sur un dépôt public ni les redistribuer. Aucun commit ni push n'a été effectué par l'importeur. `.venv` et les caches Python sont ignorés ; les contenus du livre ne sont pas automatiquement ignorés par Git. Vérifier attentivement les fichiers avant tout commit ou push.

## Import de tout le dossier (usage habituel)

Déposer les fichiers `.html` ou `.htm` directement dans :
`/home/gwi/Operation-Deadfall/sources/raw/`

Depuis Windows :
`\\wsl$\Ubuntu\home\gwi\Operation-Deadfall\sources\raw`

Accepte un fragment contenant `.p-article-content` ou une page HTML complète contenant cet élément. Lors d'un enregistrement « Page web complète », conserver le dossier d'images associé à côté du HTML : les images référencées par des chemins relatifs sont copiées et validées. Les références locales ne peuvent pas sortir du dossier du fichier HTML. Les fichiers vides sont signalés et ignorés ; les fichiers non conformes sont signalés en erreur, sans interrompre les autres imports.

```sh
cd /home/gwi/Operation-Deadfall

# Tout classer et récupérer les images explicitement liées au CDN
sources/.venv/bin/python sources/tools/import_all.py --download-images

# Mode sans réseau : copier les images locales et réutiliser celles déjà téléchargées
sources/.venv/bin/python sources/tools/import_all.py

# Tests
sources/.venv/bin/python -m unittest discover -s sources/tools -p 'test_*.py' -v
```

Le script fonctionne aussi depuis un autre dossier : ses chemins par défaut sont calculés à partir de son propre emplacement.

Résultats :
- `index.html` : point d'entrée de lecture locale, chapitres puis annexes ;
- `INDEX.md` : index général ;
- `catalog.json` : catalogue des rubriques avec titre, chapitre, ancre et fichier local ;
- `import-report.json` : un résultat par fichier, erreurs, fichiers vides, provenance des URL et contrôle de conservation du texte ;
- `chapters/<nom>/entries/` : extraits par rubrique h1 à h6 directement présente dans le conteneur de l'article, en complément du texte intégral et du découpage en sections.

Les liens entre pages importées sont réécrits vers leurs versions locales lorsqu'on connaît la page et que l'ancre cible est présente. Les liens vers des fiches externes ou pages non fournies restent en ligne, sans être téléchargés.

Les URL de référence viennent du lien canonical du HTML ou sont inférées à partir des titres/noms des fichiers (cela ne signifie pas qu'elles ont été vérifiées sur le site). Pour fournir des URL exactes, créer un JSON comme `{"nom-du-fichier.html": "https://www.dndbeyond.com/sources/dnd/aud/chemin-exact"}` puis ajouter `--source-map chemin/vers/ce-fichier.json`.

Ne pas renommer inutilement un fichier déjà importé. Les numéros des noms commençant par `chapter-` sont classés avec deux chiffres dans les dossiers de sortie, sans modifier les originaux. Si le contenu d'une source change, l'ancienne copie est conservée et une nouvelle sortie `-rev-<empreinte>` est créée. Les notes personnelles doivent rester hors des dossiers générés.

Un import sans `--download-images` peut laisser des images distantes non téléchargées : leurs statuts restent `not_downloaded` dans les manifestes. Ajouter l'option pour les récupérer. Le script n'utilise ni compte ni cookie et ne récupère jamais le texte des pages web.

## Importeur d'une seule page

`tools/import_source.py` lit exclusivement un fichier HTML local fourni par l'utilisateur. Il ne visite pas la page source, ne parcourt pas les chapitres, ne récupère pas les fiches de monstres ou de sorts et n'utilise ni cookie ni identifiant. Avec `--download-images`, seuls les fichiers image explicitement liés au domaine HTTPS `media.dndbeyond.com` sont téléchargés. Les redirections vers d'autres domaines sont refusées. Une image déjà présente et valide est réutilisée. Un échec est enregistré dans le manifeste et entraîne un code de sortie non nul.

Le classement zulkirs/provinces/quartiers reconnaît les ancres propres à ce chapitre. Pour un autre chapitre, le texte complet, le découpage en h2, les tableaux et les images fonctionnent ; un classement métier supplémentaire peut nécessiter une adaptation.

Depuis `/home/gwi/Operation-Deadfall` :

```sh
# Réinstaller l'environnement si nécessaire (uv est requis)
uv venv sources/.venv
uv pip install --python sources/.venv/bin/python -r sources/requirements.txt

# Réimporter ce chapitre ; les images déjà présentes sont réutilisées
sources/.venv/bin/python sources/tools/import_source.py \
  sources/raw/chapter-01-thay.html \
  --output sources/chapters/chapter-01-thay \
  --source-url https://www.dndbeyond.com/sources/dnd/aud/chapter-1-thay-dominion-of-red-wizards \
  --download-images

# Tests locaux sans réseau
sources/.venv/bin/python -m unittest discover -s sources/tools -p 'test_*.py' -v
```

Pour un nouveau texte, enregistrer son HTML dans `raw/`, choisir un nouveau répertoire de sortie et fournir son URL uniquement comme référence. L'importeur refuse de remplacer un original différent dans le même répertoire. Les documents dérivés sont régénérés : écrire les notes personnelles dans un autre dossier.

## Limites

La couverture est celle du HTML fourni, pas une vérification que ce HTML représente tout le livre. Les infobulles et les pages liées ne font pas partie du texte fourni. Les liens vers D&D Beyond nécessitent toujours un accès au site ; le corps du chapitre et ses images sont consultables localement après un import réussi.
