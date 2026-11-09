# Dossier politique — revue interne MJ

Livraison : `site/politique-thay.html`, deuxième site distinct de l’atlas. Ne transmettre que ce HTML. Les données publiques sont sélectionnées explicitement, jamais obtenues en embarquant un chapitre brut.

Références du chapitre 1, lignes physiques des sources, sans numéros de pages :
- `sections/03-CouncilOfZulkirs.md`, lignes 8, 12, 19 et 39–48 : rôle du Conseil, vote de remplacement, résidences et huit associations nom/école. Ne garder de 12 et 19 que les fonctions et faits publics.
- `sections/04-ThayDetails.md`, lignes 15–31 : bureaucratie, nomination et attributions des tharchions et autharchs. Les raisons privées du remplacement des fonctionnaires sont exclues.
- `sections/10-TharchDescriptions.md`, lignes 28–40 : noms et provinces des gouverneurs uniquement. Capitales recoupées avec les descriptions des provinces et les notices publiques de l’atlas. Profils de jeu, espèces cachées, alignements et activités clandestines exclus.
- `sections/07-LifeInThay.md`, lignes 15–23 et 37 : lois, recours, sanctions et hiérarchie sociale.
- `sections/05-ThayanWealth.md`, lignes 15–17 et 30–48 : péages, documents, guilde et assouplissements dans les enclaves ; aucune ambition personnelle.
- `sections/06-MagicalMilitary.md`, lignes 21 et 28 : forces non unifiées et armées privées ; aucune tactique, faiblesse ou projet de conquête.
- `sections/11-EltabbarThaysCapital.md`, lignes 50–54 et 131–133 : compétence du guet, amendes et fonction publique de Renatta Vott uniquement.

Fonctions supplémentaires du Conseil : Lethnar et tribunal (03, ligne 86), fiscalité publique de Delraz (03, ligne 67), cantonnement de Nzas (03, ligne 124), double mandat de Xelnene Thrul et Szass Tam (10, lignes 37–39), service institutionnel de Mazradash auprès de Mythrellaa (11, ligne 50). Ces lignes mélangent parfois fonctions publiques et éléments privés : seule la proposition publique est retenue.

La présentation en organigramme est une synthèse pédagogique des nominations, pas un organigramme officiel reproduit du livre. L’autorité des Magiciens Rouges est montrée séparément pour éviter une fausse chaîne « autharch > Magicien Rouge ». Les orientations pratiques reformulent les compétences et règles décrites, sans garantir de permis, d’exemption ou de procédure d’appel.

Historique de la première présentation, désormais remplacée : aucun portrait ni illustration du livre n’était embarqué, pour éviter toute divulgation de nature cachée. Décision art initiale : les huit fiches utilisent la planche générée validée par le MJ (`/home/gwi/.hermes/cache/images/openai_codex_gpt-image-2-medium_20261012_194945_f1a22177.png`, 4 × 2), découpée en huit JPEG sans métadonnées nommées par école. Ce sont des symboles d’école, ni portraits ni lieux canoniques ; légende affichée « Illustration évocatrice de l’école, pas un portrait. » Aucune intrigue, motivation privée, profil de combat, mission ou référence aux chapitres d’aventure n’alimente le HTML. L’année de référence reste celle de la source, 1501 CV.

## Validation des portraits pour le site joueurs

Le MJ a explicitement choisi « Ajouter les deux portraits : l’apparence de Szass Tam peut être révélée aux joueurs ». Portraits retenus : `09-005.xelnene-thrul.png` et `09-004.szass-tam.png` dans l’appendice B, associés respectivement à Xelnene Thrul et Szass Tam. Dérivés redimensionnés sans métadonnées, intégrés une seule fois par image, réutilisés dans galerie et lecteur. Aucune donnée de bestiaire ni motivation, intrigue ou caractéristique de combat n’est ajoutée. La scène collective `01-003.zulkir.png` n’est pas utilisée pour fabriquer des portraits individuels non identifiés. L’emblème récupéré reste en en-tête ; les anciennes images d’école générées ne sont pas livrées.

## Validation complémentaire des six portraits générés

Le MJ a validé les six portraits présentés et leur intégration au site joueurs (« je suis d accord »). Cette validation autorise uniquement la divulgation visuelle des apparences proposées : Yazir Nym, Nevron, Lethnar, Delraz, Mythrellaa et Nzas. Elle ne divulgue pas leurs biographies, capacités ou ambitions. Les traits non décrits par les sources sont des interprétations artistiques. Références et revue détaillées : `sources/propositions/portraits-zulkirs-mj/revue.md`, hors livraison. Les textes des fiches restent inchangés.

## Fiches joueurs des zulkirs

Sources : `sources/site/politique/fiches/*.md`, converties par `tools/homebrewery/render_politics.mjs`. Faits retenus et références, lignes physiques du chapitre 1 :
- Commun aux huit : siège et école (03, l. 39–48), rôle du Conseil, vote de remplacement (03, l. 8 et 12), résidences à Eltabbar et Thaymount, employés et soldats (03, l. 19 ; 11, l. 75), armées privées et absence de commandement unifié (06, l. 21 et 28).
- Yazir Nym : garnison à Escalant (10, l. 156). Escalant gouvernée par Keliza Vyrizek ; seule la garnison est reliée au zulkir.
- Nevron : aucun fait public propre au-delà du siège ; fiche limitée aux usages communs.
- Lethnar : tribunal pénal de Bezantur (03, l. 86), sans espèce ni motivation.
- Delraz : lourdes taxes sur les marchands thayens (03, l. 67), sans usage des recettes ni moyens d’influence.
- Xelnene Thrul : zulkir et tharchionne de Priador, palais à Bezantur, famille, assistance de Gulga Vull (10, l. 37–39 et 172), sans espèce, alignement ni aspirations.
- Mythrellaa : service de Mazradash (11, l. 50), Tour des Illusions du quartier des tours (11, l. 155), sans absence, retour ni pouvoirs privés.
- Szass Tam : zulkir et tharchion de Thaymount, Szul et Hall Rouge (03, l. 162 ; 10, l. 234, 256 et 260), sans nature, armée, forteresse, régence ni projets.
- Nzas : armée cantonnée à Bezantur (03, l. 124), sans apparence, transformations ni modifications des soldats.

Géographie reformulée depuis `sources/homebrewery/atlas-joueurs/` (escalant, lapendrar, bezantur, priador, eltabbar, thaymount, szul). Exclus : espèces non approuvées, alignements, ambitions privées, résurrections et pactes, natures cachées, intrigues, maléfices, profils de jeu, violences et tactiques. Le build et les tests refusent une liste de termes sensibles dans le HTML.

## Révision : habitants de Thay, pas visiteurs ignorants

La demande du MJ autorise un guide bien plus riche des connaissances locales, non la publication des intrigues. Les exclusions générales ci-dessus documentent l’ancien périmètre et ne sont plus une interdiction de mots tels que démon, tieffelin ou espion. La sélection est désormais proposition par proposition ; les informations géographiques, apparences connues, activités publiques et réputations explicitement décrites ne sont pas des révélations de scénario.

Enrichissement des zulkirs, source `sections/03-CouncilOfZulkirs.md` :
- Yazir Nym, l. 200 : incursions frontalières, soins et réputation de brutalité envers les prisonniers. Pas de profil ni de plans d’invasion inédits.
- Lethnar, l. 86 : volonté manifeste d’étendre les poursuites. Exclure la divination supposée à l’origine de sa cour.
- Delraz, l. 67 : défense des privilèges et justification des taxes. Exclure détournements personnels et manipulation magique des opposants.
- Xelnene, l. 181 : réputation de magie offensive et poids politique ; conserver charges, palais, famille et Gulga Vull issus du chapitre géographique. Exclure rencontres et projets de l’aventure.
- Mythrellaa, l. 105 : ancienne titulaire tenue pour morte puis revenue au Conseil. Exclure séjour en Gisombre, absorption de magie et projet de régence.
- Nevron, l. 133 et 143 : apparence tieffeline et puissance d’invocation, visibles dans sa carrière et le portrait déjà validé. Exclure pacte, circonstances de mort et objectifs de domination.
- Szass Tam, l. 162 : ambition de régence explicitement annoncée publiquement ; apparence déjà autorisée. Exclure rituel, moyens et projet opérationnel de l’aventure.
- Nzas, l. 124 : apparence voilée, transformations et violences notoires. Exclure découverte récente sur les soldats et recherche de permanence.

Institution des Magiciens Rouges : `sections/02-RedWizards.md`, « What Thayans Know », « Becoming a Red Wizard », « Training », « Hierarchy » et « Thayan Knights ». Formation, distinction des titres et service des chevaliers sont des connaissances sociales, non des règles de création de personnage ni une hiérarchie imposée aux joueurs.
