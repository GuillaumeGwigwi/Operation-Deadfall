# Portraits des six zulkirs — propositions visuelles MJ

Statut : les six portraits et leur divulgation visuelle aux joueurs ont été validés par le MJ (« je suis d accord »), après présentation des apparences et de la demande d’intégration. Les détails non explicités par les sources restent des interprétations artistiques validées, pas des citations du livre. Ce dossier éditorial reste interne au MJ ; seules les copies d’images sélectionnées sont intégrées au site joueurs.

## Sources examinées

Source principale : `sources/chapters/chapter-01-thay/sections/03-CouncilOfZulkirs.md`. Les références ci-dessous sont les lignes physiques de ce fichier, pas des numéros de pages du livre.

- Yazir Nym : lignes 186–200. Elfe ; pronoms masculins ; caractère agressif. Pas de description précise du visage, des cheveux, des yeux ou du costume.
- Nevron : lignes 129–143. Tieffelin ; pronoms masculins ; caractère méprisant. Forme des cornes et couleur de peau non précisées. Ne pas illustrer son histoire ou les pactes mentionnés dans les notes MJ.
- Lethnar : lignes 72–86. Gnome ; le texte ne fixe pas un genre masculin ou féminin ; tempérament pratique et impitoyable. Portrait androgyne proposé, sans prétendre déterminer son genre.
- Delraz : lignes 53–67. Humain ; pronoms masculins ; caractère manipulateur. La morphologie et l’âge apparent sont des interprétations artistiques.
- Mythrellaa : lignes 91–105. Humaine ; pronoms féminins ; caractère calculateur. Son histoire ne fixe pas son âge apparent. Aucun élément de ses intrigues ne doit figurer dans le portrait.
- Nzas : lignes 110–124. Humaine ; pronoms féminins ; visage dissimulé par des ombres. Cette dissimulation est une description explicite. Les transformations de membres ne sont pas représentées : elles ne constituent pas une apparence permanente et révéleraient des capacités non approuvées.

Une recherche complémentaire dans les chapitres importés retrouve surtout les mêmes notices sous leurs variantes chapitre/section/entrée/entité ; aucun autre détail physique indépendant n’a été retenu.

## Référence visuelle récupérée

`sources/chapters/chapter-01-thay/assets/illustrations/01-003.zulkir.png` : scène collective des huit zulkirs. Sa légende nominative est dans la source principale, ligne 30. Elle est fournie au générateur comme référence de langage pictural, de robes rouges et d’ambiance chromatique, sans attribuer un visage incertain à un personnage.

Les deux portraits individuels existants, Xelnene Thrul et Szass Tam, ne sont ni remplacés ni régénérés.

## Limite entre source et interprétation

Les espèces, pronoms et le visage dissimulé de Nzas viennent du texte. Les expressions traduisent les traits de caractère. Les traits précis, âges apparents, poses, tatouages, coupes des robes et, pour Nevron, couleur de peau et forme des cornes sont des choix artistiques. Les crânes rasés et tatouages sont un parti visuel cohérent avec les signes courants des Magiciens Rouges, pas une description personnelle attestée pour chacun.

Aucun élément de biographie, ambition, combat, prophétie, pacte, allié ou intrigue n’est ajouté aux images.

## Génération et fichiers

- `briefs.json` : les six briefs, références de sources et choix artistiques.
- `generation-results.json` : résultats réels du générateur et chemins des fichiers produits.
- `originaux/` : sorties originales de génération conservées pour l’édition.
- `portraits/` : copies redimensionnées sans métadonnées, destinées à la revue MJ.
- `planche-contact.jpg` : vue d’ensemble des six propositions.

Génération par le fournisseur Hermes OpenAI Codex avec GPT Image 2, qualité moyenne, format portrait, référence visuelle collective. Le modèle hôte interne par défaut `gpt-5.5` a été refusé par le service ; le script utilise `gpt-6.1-sol`, modèle de la session, uniquement dans son processus. Le modèle qui produit effectivement les images reste GPT Image 2. L’essai refusé est conservé dans `essai-refuse-gpt-5.5.json`. L’authentification existante est utilisée par le fournisseur ; aucun secret n’est copié dans ce dossier. Aucune configuration Hermes ni donnée d’un autre profil n’est modifiée.

## Vérification des résultats

Six portraits distincts ont été effectivement générés puis examinés individuellement, ainsi que sur la planche contact. Les robes écarlates et fonds sombres forment une série cohérente. Yazir Nym possède des oreilles elfiques ; Nevron des cornes ; Lethnar une présentation androgyne ; Delraz et Mythrellaa des apparences humaines ; le visage de Nzas reste entièrement dissimulé. Aucun texte, compagnon, scène d’intrigue ou transformation de membre n’est visible.

Les six copies de revue sont des PNG de 800 × 1200 pixels, intégralement décodés et sans métadonnées ni EXIF. Leurs empreintes sont toutes distinctes. Le total des six PNG est de 7 260 230 octets. Après validation, les six nouveaux portraits rejoignent les images déjà embarquées : les huit zulkirs, l’emblème et le poste fiscal sont désormais présents. Les textes publics et le template ont été comparés à l’état précédent et sont inchangés. Les briefs, résultats de génération, références, originaux et notes internes ne sont pas embarqués.

Le script reproductible est `tools/generate_zulkir_portraits.py`. Il conserve les résultats réussis pour éviter de générer et facturer de nouveau les mêmes portraits. Les briefs restent éditables dans ce dossier ; supprimer explicitement une entrée réussie du manifeste avant de demander sa régénération. Exécution avec l’environnement Python Hermes disponible sur cette machine : `/home/gwi/.hermes/hermes-agent/venv/bin/python tools/generate_zulkir_portraits.py`.

## Publication

Le MJ a validé l’intégration des six portraits présentés et la divulgation de leurs apparences, notamment Nevron, Lethnar, Yazir Nym et Nzas. L’autorisation est limitée aux images examinées : elle ne permet pas de publier les histoires, pouvoirs, transformations, ambitions ou intrigues des personnages. Les fichiers publics sont nommés par école, sans métadonnées et sans notes internes. Les portraits récupérés de Xelnene Thrul et Szass Tam sont conservés.
