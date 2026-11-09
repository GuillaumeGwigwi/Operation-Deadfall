# Le pouvoir écarlate — sources du site joueurs

Livrable : `site/politique-thay.html`. Partager uniquement ce HTML autonome. CSS, JavaScript, fiches, données publiques et images sont intégrés, sans réseau ni fichiers voisins.

## Sources

- `public-data.json` : quatre rôles, huit zulkirs, onze provinces et cinq situations.
- `fiches/*.md` : huit fiches joueurs en Markdown Homebrewery V3.
- `tharchs/*.md` : onze fiches provinciales joueurs en Markdown Homebrewery V3.
- `pratique.md` : une seule page Homebrewery reprenant les cinq situations existantes et les deux rubriques sur l’argent et les habitants.
- `assets/pratique.png` : dérivé sans métadonnées de `01-004.tax-station.png`, illustration du poste fiscal du chapitre 1.
- `homebrewery-officiel/` : CSS officiel V3 5ePHB, ressources embarquées, provenance et empreintes.
- `fiches-data.json` : HTML généré par `marked-hbfm` 1.0.1 ; ne pas modifier à la main.
- `index.template.html` : interface, galerie, lecteur modal et navigation.
- `assets/embleme.png` : dérivé sans métadonnées de l’illustration récupérée `sources/chapters/chapter-01-thay/assets/illustrations/01-002.symbol-of-the-red-wizards.png`.

L’emblème du livre remplace les illustrations d’ambiance créées par école. Il est embarqué une fois, puis réutilisé en en-tête et dans la section du Conseil. Deux portraits individuels identifiés sont également intégrés dans la galerie et le lecteur : Xelnene Thrul (`assets/evocation.png`) et Szass Tam (`assets/necromancie.png`), dérivés sans métadonnées des illustrations `09-005.xelnene-thrul.png` et `09-004.szass-tam.png` de l’appendice B. Le MJ a explicitement autorisé la divulgation aux joueurs de l’apparence de mort-vivant de Szass Tam. Cette autorisation ne s’étend pas aux autres informations privées du personnage. Les six autres zulkirs disposent désormais de portraits générés à partir des descriptions disponibles et validés par le MJ pour les joueurs : Yazir Nym, Nevron, Lethnar, Delraz, Mythrellaa et Nzas. Les images sont préparées dans `assets/<ecole>.png`, sans métadonnées. La validation porte sur les apparences visuelles, pas sur les histoires ou pouvoirs. Les notes et briefs restent dans `sources/propositions/portraits-zulkirs-mj/`, hors HTML livré. Les anciens JPG ne sont plus utilisés par la génération ni transmis dans le HTML.

Priorité aux assets récupérés, puis au web si aucun asset pertinent ne convient, puis à la création d’image en dernier recours. Les deux portraits individuels disponibles dans le livre sont conservés. Les six portraits manquants ont été générés avec GPT Image 2 à partir des éléments textuels, avec l’illustration collective comme référence d’ambiance, puis validés par le MJ. Leur incorporation ne déclenche aucune nouvelle génération.

## Génération

Depuis la racine du projet :

    uv run --with pillow python3 tools/prepare_politics_assets.py
    uv run --with pillow python3 tools/prepare_tharch_assets.py
    uv run --with pillow python3 tools/prepare_politics_portrait_blends.py
    node tools/homebrewery/render_politics.mjs
    python3 tools/build_politics.py

Installation des dépendances d’édition si nécessaire : `npm ci --ignore-scripts --prefix tools/homebrewery`. L’avertissement concernant `expr-eval` documenté dans le README de l’atlas reste applicable : convertir seulement les sources revues. Les dépendances ne sont pas livrées dans le HTML.

« En pratique » est affiché directement comme une seule page utilisant le même bundle officiel V3 5ePHB que les fiches provinciales. Le sélecteur de situation et les blocs séparés ont été retirés, sans suppression de leur contenu. Le bouton extérieur « 100 % / Ajuster » permet la lecture à taille native sur mobile ; le défilement reste dans le cadre. Aucun style de police, marge ou colonne de la page officielle n’est modifié.

Les huit zulkirs, les onze fiches de tharchs et la page En pratique utilisent désormais le même véritable thème officiel V3 5ePHB. L’imitation CSS historique des zulkirs a été supprimée. Les documents isolés restent en mémoire entre les sélections : styles et fontes ne sont plus réinterprétés à chaque région. Le shell adapte uniquement l’échelle et le défilement. Les pages régionales sont composées avec les classes natives `wide`, `block`, `columnSplit`, `imageMaskEdge1` et `artist`, sans modification des fontes ni des marges. Les panoramas rejoignent le bord inférieur ; les autres illustrations sont placées selon leur sujet. Les listes de gouvernement et les charges des zulkirs deviennent des tableaux natifs, sans suppression de valeurs. La carte conserve son cadre et tous ses repères.

Le bundle officiel est embarqué une seule fois, compressé sans perte puis restitué à l’identique par `DecompressionStream` dans le navigateur. Utiliser un navigateur récent, par exemple Chrome ou Edge. Les marges, colonnes, ornements, fontes et couleurs des pages officielles ne sont pas personnalisés ; seule la position et l’échelle de l’aperçu extérieur sont adaptées au lecteur. Le bouton « 100 % » permet la lecture à taille native sur mobile, avec défilement ; « Ajuster » revient à la vue complète. Le HTML pèse environ 30 Mo dans cette révision. Les six portraits générés validés sont désormais livrés en WebP transparent : masque aquarellé officiel précalculé, avec protection des visages, cornes, capuche et mains. Les PNG originaux sont conservés ; les deux portraits du livre restent inchangés. Aucune nouvelle image n’a été générée.

## Rédaction et confidentialité

Les fiches contiennent exclusivement des informations sur le zulkir : siège, charges personnelles, moyens, activités, entourage et établissements qui lui sont directement associés. Aucune présentation générique des villes, provinces, lois, économie ou institutions n’y est ajoutée. Nevron reste bref, sans encadré inutile : son siège, son apparence publique et sa spécialité d’invocateur sont attestés dans les sources. Les faits généraux restent dans les sections institutionnelles du site ou dans l’atlas. Aucune biographie n’est inventée pour combler une fiche courte.

Les PJ vivent à Thay : quartiers, métiers, trajets, dangers notoires et rumeurs explicitement publiques sont développés dans les onze régions. Une rumeur demeure attribuée comme telle, jamais promue au rang de fait certain. Les révélations de scénario sont exclues par revue sémantique, pas par une interdiction de termes génériques.

La revue interne est conservée dans `sources/propositions/politique-thay-mj/revue.md`, hors livraison.

Les onze fiches provinciales ne reprennent pas une présentation générale de Thay. Chacune contient son gouverneur, sa capitale et ses propres politiques, ressources ou contraintes. Leur sélection de sources est tracée dans `sources/propositions/politique-thay-mj/tharchs-revue.json`, jamais embarquée dans le site. Ne pas partager les sources MJ ni les illustrations non revues. Les droits doivent être vérifiés avant toute publication publique des illustrations du livre ; l’usage ici est le partage privé du groupe.

## Vérification

    python3 tests/test_politics_cleanup.py
    uv run --with playwright python3 tests/test_politics_site.py
    python3 tests/test_politics_personal_fiches.py
    uv run --with playwright python3 tests/test_politics_tharchs.py
    uv run --with playwright python3 tests/test_politics_practice.py
    uv run --with playwright python3 tests/test_politics_council_official.py
    python3 tests/test_politics_public_depth.py
    uv run --with playwright --with pytest pytest -q tests/test_politics_enriched.py tests/test_politics_performance.py
    uv run --with playwright python3 tools/verify_politics_revision.py
    uv run --with playwright python3 tools/capture_politics_council.py
    uv run --with playwright python3 tests/test_politics_close_focus.py
    uv run --with playwright python3 tools/benchmark_politics_revision.py

Les sept illustrations régionales et la carte publique d’Eltabbar proviennent du chapitre 1. Le manifeste `region-images.public.json` et `tools/prepare_tharch_assets.py` gouvernent les dérivés WebP sans métadonnées. Les onze régions occupent douze pages ; Eltabbar en occupe deux avec sa carte. La pagination conserve intégralement les paragraphes et protège les débuts de sections et légendes.

Les mesures comparatives sont enregistrées dans `verification/performance-before-after.json` : version Git de référence contre fichier reconstruit, même Chromium, 11 transitions par format d’écran. Distinguer première ouverture et navigation après initialisation. Les captures et le contrôle de toutes les régions sont dans `verification/`. Une capture directe d’un élément à travers un iframe défilant peut être rognée par le viewport : pour la revue pleine page, le script rouvre le DOM exact dans une surface suffisamment haute.

L’analyse graphique détaillée et ses sources sont dans `sources/propositions/politique-thay-mj/style-livres-dnd-recherche.md`. Les recommandations durables du profil sont regroupées dans la référence `campaign-art-direction/references/dnd-book-layout-homebrewery.md` : style natif, composition selon le contenu et distinction explicite des références 2014 et 2024.

Contrôles : copie du seul HTML renommé, emblème et huit portraits chargés sans métadonnées, huit fiches, onze provinces, quatre rôles, situations, recherche, clavier, Échap, retour du focus, précédent/suivant, colonnes, vues ordinateur/mobile, absence de ressources externes et d’erreurs JavaScript. Les tests statiques contrôlent aussi les métadonnées du PNG et l’absence des anciennes images et des phrases supprimées.
