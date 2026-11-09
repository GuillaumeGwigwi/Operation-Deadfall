# Livres D&D 2014 / 2024 et Homebrewery : recherche visuelle et règles de composition proposées

**Statut : recherche sourcée et proposition, pas nouvelle charte approuvée.** Consultation le 26 octobre 2026. Public : MJ, document privé. Aucun skill, thème, manuscrit ou livrable existant n’a été modifié par ce sous-agent. Les captures et échantillons de recherche sont dans `recherche-style/` ; ils ne constituent pas des assets autorisés à republier. Le [manifeste des échantillons](recherche-style/manifest.json) donne leurs sources, tailles et empreintes SHA-256. La p. 12 des Basic Rules est conservée comme échantillon complémentaire examiné par le parent selon son message, sans lui attribuer ici une observation propre au sous-agent.

## 1. Décision directement applicable

**Conserver intégralement le thème officiel de Homebrewery V3 `5ePHB`, éventuellement avec une palette validée, et améliorer l’édition et la composition du contenu. Ne pas fabriquer une CSS « PHB 2024 ».**

Trois choses différentes doivent rester nommées séparément :

1. **Les règles D&D 2024** : version mécanique du texte. Elles peuvent parfaitement être présentées avec le thème HB choisi.
2. **La direction artistique des livres WotC** : elle varie entre 2014, 2024 et les ouvrages ultérieurs ; les compositions imprimées ne sont pas le rendu web D&D Beyond.
3. **Le thème officiel de l’outil Homebrewery** : `5ePHB` est une interprétation de la famille graphique du PHB de la génération 2014, pas une feuille de style publiée par Wizards. « V3 » désigne le moteur Homebrewery, pas une édition de D&D et surtout pas « 2024 ».

**Résultat de la vérification de disponibilité : aucun thème natif distinct explicitement PHB 2024 n’a été trouvé dans les sources officielles HB examinées.** Le dépôt contient `5ePHB`, `5eDMG`, `Blank`, `Journal`, `UnearthedArcana` sous `themes/V3`. Les métadonnées de `5eDMG` indiquent qu’il hérite de `5ePHB`, non qu’il serait un thème 2024. L’accueil effectivement servi annonce V3, utilise `theme: "5ePHB"` et annonce la version applicative `3.24.2`. Cette conclusion est bornée à l’état vérifié, pas une affirmation qu’aucun auteur communautaire n’a jamais réalisé un thème 2024. Une publication hébergée sur Homebrewery n’est pas automatiquement un thème officiel de l’outil. [H1–H5]

Le nom officiel est **« 5e PHB »**, sans millésime dans `settings.json`. L’expression « famille 2014 » ci-dessus est une **attribution visuelle et historique**, étayée par les formes observées et la vocation déclarée du projet, non un libellé de métadonnées « 2014 » qui n’existe pas dans ce fichier.

**Le gain le plus important à reprendre de 2024 n’est pas une bordure ni une police : c’est la fonction structurante de l’image, placée selon une logique répétable près de son sujet.** On peut reprendre cette logique avec les composants HB natifs, sans imiter les cadres 2024.

## 2. Méthode, périmètre et niveau de preuve

Compétence lue : `campaign-art-direction`, ainsi que ses trois références `source-led-theme-workflow.md`, `illustrated-adventure-books.md` et `sourced-character-portraits.md`. Consignes locales lues dans `AGENTS.md`. Provenance du bundle existant lue dans `sources/site/politique/homebrewery-officiel/PROVENANCE.md`.

Les paragraphes suivants distinguent :

- **VU** : image effectivement chargée et examinée en vision native.
- **SOURCE** : texte, métadonnées ou CSS réellement lus ; ce n’est pas une observation visuelle.
- **PROPOSITION** : règle de composition recommandée pour le projet ; aucune prétention de norme interne WotC.

### Corpus effectivement examiné

| Corpus | Support effectivement vu | Ce qu’il permet d’affirmer | Limite essentielle |
|---|---|---|---|
| WotC 2014 | PDF public **Player’s Basic Rules v0.2**, pages 3, 4, 6, 10, 25, rendues en PNG | Grille, hiérarchie, tableaux, densité, continuité et blancs d’une publication WotC contemporaine | **Ce n’est pas un fac-similé du PHB commercial** ; on ne peut en déduire sa fréquence d’illustrations |
| PHB 2024 | Deux photographies de doubles pages, publiées par GamesRadar dans un entretien avec le directeur artistique Josh Herman | Composition réelle des historiques et sous-classes, articulation texte/image | Source journalistique et photographies créditées Benjamin Abbott, **pas previews servies par WotC** ; perspective et éclairage coloré interdisent de mesurer couleurs et marges |
| PHB 2024, officiel | Illustration de ferme par Kenny Vo publiée dans l’article D&D Beyond sur les nouveautés | Sujet, palette, cadrage et narration d’une image officielle | Visuel promotionnel autonome, pas page imprimée |
| DMG 2024, officiel | PDF public `NPC Tracker` lié depuis D&D Beyond | Séparation fonctionnelle texte/ornement et feuille de suivi | Feuille à remplir, pas page narrative ; ses grands blancs ont une fonction différente |
| Homebrewery | Captures des deux pages de la démonstration réelle sur le site officiel, plus sources `5ePHB` et `Blank` | Rendu réellement disponible, syntaxe, composants, contraintes de colonnes | La démonstration contient quelques réglages propres, détaillés plus bas |
| Source privée du projet | Illustration d’ouverture du chapitre 1 et scène des zulkirs, avec manifeste local | Bordures présentes dans l’asset, transparence, proportions et relation entre sujet et cadrage | Images autonomes extraites d’un HTML fourni par l’utilisateur, pas preuve de pagination imprimée ni autorisation publique |

**Limite importante : la recherche n’a pas obtenu de corpus représentatif de pages illustrées du PHB commercial 2014 via des previews primaires encore accessibles.** Les recherches ont souvent remonté des copies intégrales de provenance non autorisée ; elles n’ont pas été utilisées. La page D&D Beyond `phb-images` n’a pas fourni les illustrations recherchées dans sa réponse accessible. Le comparatif 2014 reste donc fondé visuellement sur les Basic Rules, et historiquement complété par l’entretien consacré au changement 2014 → 2024. Il ne faut pas présenter ce rapport comme une revue complète des six livres de base.

Aucune photographie ne permet de conclure « toujours », « jamais » ou de calculer un taux global d’occupation. Aucun ratio texte/image, nombre de mots par page ou corps typographique WotC n’a été inventé.

## 3. Ce que montrent réellement les pages 2014

Source primaire [W14]. Échantillons locaux : [p. 3](recherche-style/basic2014-p3.png), [p. 4](recherche-style/basic2014-p4.png), [p. 6](recherche-style/basic2014-p6.png), [p. 10](recherche-style/basic2014-p10.png), [p. 25](recherche-style/basic2014-p25.png).

### 3.1 La page est un flux de lecture, pas une succession de cartes

**VU, p. 3–4 :** deux colonnes continues, corps à empattements noir, titres brun-rouge, papier clair légèrement texturé. Plusieurs niveaux se distinguent par taille, petites capitales et présence ou absence de filet doré. Les paragraphes successifs emploient le retrait plutôt que de grands espaces verticaux. Des mots ou débuts de propositions en gras fournissent des prises de lecture à l’intérieur d’un texte assez dense.

La p. 3 commence par une continuation : elle ne se sent pas obligée de réinstaller un titre de rubrique en haut. La procédure numérotée commence en bas de la colonne gauche et continue en haut de la droite. À la fin de la p. 4, le texte se poursuit : la page matérielle ne remplace pas l’organisation du chapitre.

**Conséquence :** rendre chaque PNJ, quartier ou sous-section indépendant sur une nouvelle page produit un catalogue de fiches, pas nécessairement un livre. Une rupture de page se justifie par un chapitre, une ouverture visuelle ou un regroupement éditorial, non par chaque `h2`.

### 3.2 Une hiérarchie sobre supporte une forte densité

**VU, p. 25 :** « Fighting Style », les styles individuels, les capacités et « The Fighter » ne sont pas traités comme des panneaux identiques. Les petits intitulés signalent des unités courtes ; les titres à filet marquent les ruptures plus fortes. La table de progression tient dans la colonne droite sous le texte, sans cadre massif ni cellule rectangulaire fortement délimitée à chaque intersection.

**Conséquence :** pour un dossier MJ, titre de territoire, sous-parties politiques, entrées de personnes et libellés de faits doivent avoir des rôles différents. Mettre tous les textes en encadrés `note` ou tous les noms au niveau `h2` efface ces différences.

### 3.3 Les tableaux ne sont pas des paragraphes comprimés

**VU, p. 25 :** trois colonnes utiles, en-têtes compacts, fond alterné vert clair, présentation plus utilitaire que le corps narratif. Les intitulés de capacités restent les éléments dominants ; l’alternance aide à suivre la ligne.

**VU, p. 10 :** la table « Character Advancement » utilise des groupes de lignes teintées, et le texte explicite que l’ombrage distingue des paliers de jeu. **Ce n’est donc pas partout un simple zébrage une ligne sur deux.** Reproduire automatiquement l’apparence HB ne reproduirait pas cette sémantique.

**Conséquence :** employer des mots de groupe explicites quand une table doit signifier une catégorie. Dans notre cadre « palette seule », ne pas introduire un nouveau système de coloration par cellules pour simuler cet exemple WotC.

### 3.4 Le blanc n’est pas systématiquement une erreur

**VU, p. 10 :** la colonne gauche descend près du bas ; la droite s’arrête après la table, laissant un espace notable sous elle. Cela clôt un ensemble identifiable. Le blanc n’est pas rempli par une image sans rapport.

**VU, p. 6 :** l’ouverture de partie et de chapitre emploie un grand bandeau de titres sur la largeur et reprend immédiatement le texte en colonnes. **Pas de lettrine décorative géante sur cet échantillon**, malgré la présence de petites capitales au démarrage. Il serait faux d’attribuer la lettrine HB visible plus loin à toutes les ouvertures WotC 2014.

**Conséquence :** distinguer un blanc de fin d’unité et une colonne vide créée par un mauvais saut. Ne pas imposer une densité uniforme, mais exiger une raison compréhensible pour une page presque vide.

## 4. Ce que 2024 apporte au raisonnement de composition

### 4.1 Les historiques : l’image est un élément d’identification récurrent

**VU, photographie [P24-A] :** la double page des historiques alterne larges scènes horizontales et bandes claires de texte. « Hermit » et « Noble » sont lisibles. Sous chaque scène, les informations mécaniques et la description occupent des zones distinctes. D’autres scènes apparaissent plus bas, indiquant une répétition du dispositif au sein de la double page.

Ce n’est ni une galerie séparée ni une série d’images décoratives entre des paragraphes indifférenciés : **image + nom + informations constituent une entrée reconnaissable**. L’illustration ne remplace pas les informations, elle donne une identité immédiatement mémorisable à l’entrée.

**PROPOSITION pour les tharchs :** placer un paysage pertinent près du nom et du passage qui définit son identité, puis conserver l’ordre des rubriques. L’élément répétable est la fonction de l’image, pas nécessairement sa hauteur exacte. Ne pas fabriquer une grille CSS de cartes pour reproduire cette photographie.

### 4.2 Les sous-classes : deux masses visuelles latérales, texte dense au centre

**VU, photographie [P24-B] :** les illustrations verticales occupent les côtés extérieurs de la double page ; les colonnes de texte se rapprochent de la reliure. Les personnages ont un environnement et un cadre fin, pas un fondu aquarellé uniforme. Le chevalier sombre à droite occupe une grande hauteur ; une petite légende se trouve dans le bas de l’image. La table des sorts reste insérée au-dessus du texte de règles, dans une colonne, avec bandes claires.

**Ce que cela réfute :** « faire moderne » ne signifie pas forcément agrandir les marges, passer tout le livre en une colonne ou supprimer la densité. Une image forte et un texte compact peuvent cohabiter si leurs emplacements sont prévus ensemble.

**SOURCE, entretien [P24] :** Josh Herman explique que les doubles pages de classes ont été conçues dès le départ, avec une image emblématique de classe et des images verticales latérales pour les sous-classes. L’objectif déclaré est l’orientation du lecteur autant que l’illustration. Le journaliste décrit aussi davantage d’images dans les sorts ; c’est une appréciation sourcée, non un comptage de notre part.

**PROPOSITION pour les PNJ :** les portraits peuvent devenir des repères de sections. Prévoir image et notice ensemble avant de paginer. Ne pas ajouter les portraits après coup en acceptant qu’ils chassent le texte utile sur la page suivante. Une scène de groupe horizontale n’est pas interchangeable avec un portrait vertical.

### 4.3 L’image raconte une situation, pas seulement un emblème

**VU, image officielle [W24-A] :** moulin et maison couverts de végétation, chemin au premier plan, parcelles en eau et lumière de fin de journée. Les bâtiments ancrent la gauche ; le regard suit le chemin et les lignes du paysage vers la droite. Les teintes chaudes du ciel s’opposent aux ombres plus froides. Le cadrage large contient une action possible et un milieu de vie, sans texte superposé.

**SOURCE [W24] :** D&D Beyond annonce des illustrations pour chaque classe et sous-classe, ainsi que pour les historiques et espèces ; l’article insiste également sur les exemples de jeu, les explications, l’index et le glossaire.

**PROPOSITION :** associer un panorama à une fonction du lieu — commerce, passage, surveillance, richesse, isolement — plutôt qu’à son seul nom. Cela reste une illustration, pas une carte exacte. Les portes, passages et moyens d’accès ne doivent pas contredire les sources du scénario.

### 4.4 Le décor ne doit pas envahir la zone fonctionnelle

**VU, feuille officielle NPC Tracker [W24-T] :** surface centrale très claire, rubriques de formulaire, lignes et zones à compléter ; feuillages et lavis se concentrent aux bords. Une petite créature illustrée occupe le coin inférieur droit. Le titre possède un encadrement fin à courbes. Ce n’est pas le parchemin brun-jaune de la démonstration HB.

**Limite :** ces grands blancs sont des espaces d’écriture. Ils ne justifient pas des pages de livre à moitié vides. Le transfert pertinent est la séparation des zones, pas la densité du formulaire.

### 4.5 Ce qu’on ne doit pas déduire

- L’éclairage vert et rose des photos [P24-A/B] n’est pas la palette imprimée.
- Un cadre aperçu sur une sous-classe ne démontre pas un cadre universel sur toutes les images 2024.
- Un fichier image D&D Beyond ne décrit pas la gouttière, les marges ni les sauts du livre papier.
- L’article officiel décrit les intentions ; seul le corpus vu étaye nos observations précises de placement.
- Ces sources ne démontrent aucune règle WotC chiffrée sur veuves, orphelins, longueur des légendes ou taux d’illustration.

## 5. Le cas des images privées déjà disponibles dans le projet

Source locale [L1], manifestée comme **HTML fourni directement par l’utilisateur**, et non comme récupération publique autorisant une diffusion. L’utilisateur rattache cette référence visuelle à une source « 2025 » ; le manifeste consulté n’atteste pas lui-même ce millésime. L’analyse ci-dessous porte sur les pixels et la provenance locale, **sans utiliser cette date pour identifier un thème PHB 2024**.

### 5.1 Ouverture du chapitre 1 : cadre doré intégré et vrai problème d’alpha

**VU :** `01-001.ch-1-splash.png`, Joshua Raphael selon le manifeste. Composition presque verticale : grandes figures en robes rouges en partie haute, éclairs bleus, petites figures humaines au sol. Un cadre doré irrégulier épouse l’image : courbes rentrantes, pointes et détails ornementaux. Ce cadre fait partie de l’asset, ce n’est pas une bordure CSS HB.

Sur le premier affichage, l’extérieur apparaissait noir. **Vérification technique effectuée : PNG en mode palette `P`, transparence portée par les métadonnées de palette ; après conversion RGBA, alpha de 0 à 255 et pixel du coin `(0, 0, 0, 0)`.** Il serait donc erroné de décrire ce noir extérieur comme un aplat opaque imposé par l’artiste.

Un dérivé de contrôle a été composé sur `#EEE5CE` : [simulation sur fond uni](recherche-style/source-privee-splash-sur-parchemin.jpg). **VU :** le fond clair remplace bien les zones noires extérieures ; la bordure dorée reste intacte. Ce test est une simulation d’alpha sur une couleur HB, pas une page finale ni une preuve de rendu sur la texture complète.

### 5.2 Scène des zulkirs : un autre traitement, dans le même chapitre

**VU :** `01-003.zulkir.png`, Bubble Cat Studio selon le manifeste. C’est une scène collective horizontale, pas un portrait individuel. Les robes rouges et une lumière surnaturelle chaude se détachent d’une architecture sombre bleutée. **Pas de cadre doré courbe semblable à l’ouverture** ; le bord inférieur est pictural et irrégulier.

Le fichier possède lui aussi une transparence de palette, alpha converti de 0 à 255. Son coin supérieur gauche est partiellement transparent `(50, 46, 54, 191)`. La transition doit donc être examinée sur le véritable fond, pas jugée depuis un aperçu noir.

**Conclusion de composition :** même une source récente n’impose pas un seul mode de bordure. Ne pas appliquer un masque aquarelle identique à tous les assets. Conserver un cadre déjà dessiné ; préserver l’alpha d’un bord pictural ; réserver un nouveau fondu aux images qui en ont réellement besoin. La règle durable ne doit pas être « tout fondre », mais **choisir et vérifier le raccord de chaque type d’image**.

**Compatibilité avec la contrainte utilisateur :** utiliser une illustration qui contient déjà un cadre ne modifie pas le thème HB. En revanche, reconstruire ce cadre sur toutes les pages, importer les styles du site source ou en faire de nouveaux encadrés CSS serait une réinterprétation graphique interdite. Ne pas ajouter un second cadre HB autour d’un cadre intégré, ni découper automatiquement l’ornement pour « uniformiser ».

Le PNG original doit rester intact. Tout dérivé de placement est distinct, tracé et vérifié ; aucune publication des sources MJ ou du dérivé privé de cette recherche n’est autorisée par la présente analyse.

## 6. Homebrewery officiel : ce qui existe vraiment

### 6.1 Rendu vu et identité

Captures réellement prises dans Chromium sur l’accueil officiel : [page 1](recherche-style/homebrewery-officiel-page1.png), [page 2](recherche-style/homebrewery-officiel-page2.png).

**VU, page 1 :** parchemin clair jaune-beige, corps serif noir, grands titres brun foncé, filet sous plusieurs sous-titres, grande lettrine décorative dorée au début, deux colonnes, note vert pâle avec bordure et ombre, illustration de chope sur tache picturale près du bas de la colonne gauche, crédit à proximité, filet et pied de page dorés. **Ce sont les formes qu’il faut garder**, pas seulement une palette ressemblante.

**VU, page 2 :** même grille, tableau contenu dans une seule colonne, petit exemple d’image, textes et hiérarchie. Le titre violet et le fond violet pâle sont des exemples d’injection de style de la documentation, **pas des valeurs à reproduire dans notre livre**. Le bouton orange « Create your own » appartient à l’interface de démonstration, pas au langage éditorial du livre.

**Attention méthodologique :** le champ `brew.style` de cette démonstration ajoute des pointillés au tableau exemple et un `padding-bottom: 1.1cm`. Ce n’est donc pas un étalon de marges « strictement par défaut ». La géométrie de référence vient des fichiers officiels de thème et du bundle local figé, pas de la mesure naïve de cette capture.

### 6.2 Paramètres effectivement lus dans le code officiel

Dans `themes/V3/5ePHB/style.less` et `Blank/style.less` [H2–H4] :

- Deux colonnes ; largeur de colonne déclarée `8cm`, gouttière `0.9cm`, remplissage `auto`.
- Corps `BookInsanityRemake`, `0.34cm` ; paragraphes à `1.25em` d’interligne.
- Titres principaux `MrEavesRemake`, lettrine `SolberaImitationRemake`, tables et notes `ScalySansRemake` ; ce sont **des noms de familles du thème HB**, pas une certification des fichiers typographiques WotC.
- `h1` porte un `column-span: all`. Les titres `h3` portent le filet de couleur `--HB_Color_HeaderUnderline`.
- `.wide` traverse les colonnes. `.block` est un bloc non fragmentable (`inline-block`, largeur complète, `break-inside: avoid`) dans le thème de base.
- Les tables et blockquotes ont des protections de fragmentation, mais un bloc plus grand que la place disponible ne devient pas magiquement paginable.
- `.columnSplit` correspond au saut de colonne ; `\page` et `\column` appartiennent au balisage et à sa compilation, non à une CSS qui répartirait seule un manuscrit sur un nombre illimité de pages.
- Les notes, descriptions, tables de classe, fiches de monstre, couvertures et crédits d’artiste ont déjà leurs styles natifs.

Couleurs par défaut réellement présentes dans `5ePHB` : fond `#EEE5CE`, accent `#E0E5C1`, titres `#58180D`, filet de titre `#C0AD6A`, légendes/crédits `#766649`, pied `#C9AD6A`, tache aquarelle `#BBAD82`, fond de monstre `#F2E5B5`. **Ce relevé n’est pas une proposition de recoloration.** Certaines couleurs de décor sont codées dans les assets ou dans des déclarations non paramétrées ; changer quelques variables ne recolore pas nécessairement tout. Ne pas remplacer textures et ornements sous prétexte de changer la palette.

### 6.3 Ce que « thème intégral, palette seule » permet et interdit

| Autorisé dans le travail de composition | À ne pas faire sous cette consigne |
|---|---|
| Choisir le niveau de titre sémantiquement juste | Redéfinir police, corps ou interligne des titres et paragraphes |
| Utiliser les classes et snippets natifs du thème choisi | Inventer des composants décoratifs « presque officiels » |
| Choisir, recadrer prudemment, redimensionner et placer une illustration | Modifier les colonnes, marges ou largeur utile pour la faire entrer |
| Regrouper une courte unité dans `block`, employer `wide` lorsque pertinent | Enfermer tout un chapitre dans un bloc non fragmentable |
| Déplacer un saut de page ou de colonne, réordonner un bloc autonome sans casser le sens | Réduire la typographie ou masquer le débordement |
| Adapter les variables de couleur explicitement validées | Remplacer le papier, les filets, les ombres ou les cadres pour imiter 2024 |
| Conserver un cadre déjà inclus dans une image source | Transformer ce cadre en système CSS généralisé |

La permission générale de personnalisation offerte par HB est plus large que celle donnée pour ce projet. **Le fait que le site propose un éditeur CSS n’autorise pas à l’utiliser pour réinterpréter le thème demandé.**

## 7. Recommandations concrètes pour composer le livre

Toutes les règles de cette section sont des **propositions éditoriales**, fondées sur les observations ci-dessus ; elles ne sont pas présentées comme un manuel de fabrication interne WotC.

### 7.1 Organiser avant de paginer

Créer pour chaque section une unité de composition : titre, introduction, faits utiles, illustration éventuelle, légende/crédit et renvois. Puis distinguer quatre fonctions de pages :

- **Ouverture de chapitre** : signal fort, titre et image pertinente ; le chapitre commence réellement, sans couverture répétée pour chaque rubrique.
- **Page de développement** : flux de deux colonnes, sous-parties courtes, illustrations ponctuelles.
- **Page de référence** : tables et informations à retrouver rapidement, contenu suffisamment stable pour être consulté en partie.
- **Fin d’unité** : blanc résiduel admis, mais expliqué par la clôture du contenu plutôt que par une rupture accidentelle.

Ce sont des fonctions, pas quatre nouveaux thèmes ni quatre gabarits CSS.

### 7.2 Prévoir le format d’image selon son sujet

- **Scène collective ou géographie** : préférer la largeur de page native `wide` lorsqu’une réduction en colonne rendrait les personnages ou détails illisibles.
- **Portrait véritable** : un placement en colonne permet la proximité de sa notice et laisse le texte poursuivre son flux.
- **Objet ou symbole** : petit format, rattaché à son paragraphe ; éviter de lui consacrer une page par défaut.
- **Ouverture cadrée presque verticale** : adapter son rôle à ses proportions. Ne pas comprimer verticalement ni transformer systématiquement en bandeau par recadrage destructeur.
- **Visuel avec alpha existant** : conserver et tester l’alpha. Ne jamais déduire qu’une zone noire dans une visionneuse est un fond opaque.

Le recadrage doit conserver les traits utiles : visage, mains, attributs, interaction et sens de la scène. Une découpe d’une scène collective peut supprimer une relation importante ; ne pas la pratiquer uniquement pour remplir un rectangle.

### 7.3 Équilibrer les colonnes sans imposer un pavé uniforme

Le but est une lecture gauche → droite sans hésitation. Un panorama transversal peut interrompre ce flux : le placer de préférence à une frontière compréhensible, avec son titre et son texte introductif correctement associés. Après insertion d’un `wide`, revérifier **les colonnes qui précèdent**, pas seulement ce qui suit.

Un déséquilibre est acceptable à la fin d’une section. Il devient suspect si une colonne reste largement vide tandis que le contenu voisin est rejeté sur une nouvelle page. Chercher d’abord un bloc indivisible trop grand, un saut prématuré, une image trop haute ou un groupement qui englobe trop de texte.

**Ordre de correction recommandé :** déplacer le point de rupture → changer le regroupement court → ajuster le format ou la taille de l’image sans la déformer → déplacer une unité autonome → réviser un texte seulement si l’autorisation de rédaction le permet → ajouter une page. Ne pas toucher à la géométrie du thème.

### 7.4 Densité : examiner trois niveaux

1. **Dans une colonne** : le paragraphe se lit-il sans concurrence d’une image ou d’un cadre ?
2. **Sur une page** : titre, image et masse de texte ont-ils une relation lisible ? Les blancs sont-ils volontaires ?
3. **Dans une séquence** : plusieurs pages de texte serré sont-elles suivies de plusieurs pages presque vides ? Une image doit-elle être rapprochée de son sujet plutôt que toutes regroupées ?

Pas de quota d’image par page. Le rythme recherché doit découler des unités de contenu. Un chapitre politique n’a pas à répéter le plan iconographique d’une classe de personnage.

### 7.5 Titres, veuves et orphelins

- Ne pas laisser un titre seul en bas de colonne ; le garder avec son début d’explication, **objectif proposé : au moins deux lignes de corps lorsque la section le permet**.
- Contrôler les titres longs en français : un titre ne doit pas se fragmenter entre colonnes.
- Éviter une première ou dernière ligne de paragraphe isolée ; préférer un saut éditorial propre à des retours forcés partout.
- Utiliser `block` pour une unité réellement courte et inférieure à la place utile d’une colonne. Un chapitre entier non fragmentable crée précisément les trous que l’on cherche à éviter.
- Si titre et panorama doivent traverser les colonnes, les traiter comme une unité `wide` cohérente, puis reprendre le corps dans le flux natif.

Le seuil de deux lignes est un garde-fou de projet, pas un constat mesuré chez WotC. La protection CSS seule ne constitue pas une vérification du PDF.

### 7.6 Légendes et crédits

Distinguer **identification du sujet**, **crédit artistique** et **information de jeu**. Une petite légende ne doit pas servir de refuge à des faits indispensables pour le MJ. Les crédits peuvent utiliser les possibilités natives HB ; le code `.artist` est positionné absolument, donc il faut réellement réserver sa place et vérifier qu’il ne recouvre ni texte ni pied.

Conserver image et légende sur la même page et dans un voisinage clair. Éviter une légende ambiguë entre deux portraits. Sur une scène collective, n’identifier des personnes que si une source fournit l’association ; la légende privée du manifeste peut servir de preuve au MJ, mais pas automatiquement être exportée aux joueurs.

### 7.7 Tables

Une table doit permettre une comparaison ou une recherche, pas simplement contenir tous les paragraphes difficiles à mettre en page.

- Garder un titre court avec le tableau ; placer les explications longues avant ou après.
- Faire tenir un tableau simple dans une colonne ; employer `wide` pour une largeur réellement nécessaire, pas pour chaque table.
- Si une ligne contient une longue notice narrative, sortir cette notice du tableau plutôt que réduire sa police.
- Fractionner explicitement les très longues tables en unités compréhensibles, avec en-tête répété et mention de suite si nécessaire. Le CSS officiel consulté déclare le `thead` en `table-row-group` : ne pas supposer une répétition automatique d’en-tête à l’impression.
- Conserver les valeurs, unités, libellés et références ; vérifier après fragmentation qu’aucune ligne n’a disparu ou n’a été dupliquée.
- La couleur peut guider l’œil, mais un groupe sémantique doit être nommé, pas seulement coloré.

### 7.8 Encadrés

Utiliser `note` pour une information latérale ou un rappel réellement distinct ; `descriptive` pour un texte destiné à être présenté comme description, lorsque ce rôle existe dans le manuscrit. Une note ne devrait pas devenir le conteneur par défaut de toutes les sections. Pour un long texte MJ continu, la hiérarchie native du corps est généralement plus lisible qu’un empilement de boîtes.

### 7.9 Ouvertures et pleines pages

Une image dominante est justifiée lorsqu’elle ouvre un chapitre, installe un lieu important ou constitue un objet de consultation. Elle n’est pas justifiée seulement par un trou découvert après pagination. Employer les ouvertures natives du thème sélectionné si elles sont adaptées ; ne pas importer le cadre des livres récents ni reproduire un logo WotC qui suggérerait une édition officielle.

Le récit reste un livre continu avec repères et sommaire. Une couverture pour chaque PNJ casserait le rythme ; des portraits en colonne et quelques paysages traversants sont plus souples.

## 8. Proposition de guideline durable, à intégrer par le parent après validation

> ### Composer un livre D&D avec Homebrewery officiel
> 1. Déclarer séparément la version des règles, le moteur HB et le thème exact. V3 n’est pas 2024 ; « officiel HB » n’est pas « officiel WotC ».
> 2. Employer le thème intégral choisi, avec provenance et version figées. Seule la palette explicitement validée est adaptable ; aucun remplacement de police, marge, colonne, papier, cadre ou système de titres.
> 3. Examiner des pages sources réelles et les identifier par édition et support. Ne jamais utiliser une illustration autonome ou une page web responsive comme preuve de pagination imprimée.
> 4. Définir les unités de contenu avant les sauts. Le livre est continu ; les petites rubriques n’imposent pas une nouvelle page.
> 5. Choisir une fonction pour chaque image et l’ancrer au bon passage. Employer les composants natifs, notamment `wide` et `block`, sans nouveaux gabarits décoratifs.
> 6. Respecter le traitement original des images : cadre intégré, bord pictural ou rectangle assumé. Vérifier l’alpha, y compris les PNG en palette ; ne pas ajouter un fondu systématique ni un double cadre.
> 7. Garder titres avec leur début, légendes avec images et titres de table avec tableaux. Fractionner les unités trop longues plutôt que réduire la typographie.
> 8. Traiter les blancs comme des décisions éditoriales : clôture légitime ou ouverture assumée, jamais simple effet d’un bloc surdimensionné ou d’un saut accidentel.
> 9. Après chaque changement d’image ou bloc transversal, contrôler toute la page et les pages voisines. Attendre polices et images décodées avant les mesures.
> 10. Vérifier le HTML et le PDF réellement produits : aucun texte perdu, aucune troisième colonne coupée, aucun recouvrement, aucune légende séparée, aucune ligne de table manquante.
> 11. Pour un HTML autonome, vérifier une copie isolée hors connexion ; embarquer aussi les images du contenu, pas seulement les ressources du thème.
> 12. Séparer droits, confidentialité et disponibilité technique. Un asset accessible ou fourni n’est pas automatiquement publiable ; une image montrable ne rend pas les notes MJ partageables.
>
> **Formulation de livraison recommandée :** « Contenu compatible avec les règles D&D 2024, composé avec Homebrewery V3, thème officiel de l’outil “5e PHB”, de filiation visuelle 2014 ; palette [inchangée / adaptation validée]. »

### Compléments à apporter aux références existantes, sans les modifier ici

La référence `illustrated-adventure-books.md` contient déjà des mesures utiles de pagination et de confidentialité. La compléter plutôt que la remplacer :

- qualifier les trois sens de « officiel » / « V3 » / « 2024 » ;
- remplacer l’idée implicite de fondu universel par une décision entre cadre intégré, transparence existante et fondu ajouté ;
- ajouter le piège des PNG `P` avec table de transparence ;
- distinguer page de livre, visuel de chapitre web, photographie et feuille à remplir ;
- ajouter la vérification de disponibilité du thème 2024 à chaque éventuelle migration, plutôt que figer « n’existe pas » pour toujours ;
- conserver les diagnostics déjà documentés sur blocs transversaux, découpe PDF et polices, sans les prétendre exécutés sur le livre dans la présente recherche.

## 9. Contrôle d’acceptation pour une future recomposition

Ce rapport ne réalise pas la recomposition. La passe suivante devrait produire un échantillon contenant une ouverture, une page dense, des portraits, une table et une fin de section, **avec le vrai texte**, puis vérifier :

- identité du bundle officiel inchangée hors transformations techniques d’embarquement et palette autorisée ;
- images décodées, alpha préservé, pas de déformation ;
- aucune information essentielle déplacée dans un crédit ou une légende minuscule ;
- tous les titres et tableaux sémantiquement présents ;
- rectangles du texte et des images dans la zone attendue ; exceptions limitées aux ornements natifs documentés ;
- absence de coupe à droite ou de troisième colonne cachée dans le PDF ;
- contrôle visuel de toutes les pages illustrées, des transitions et des pages signalées comme peu remplies ;
- contrôle de lecture à taille normale, pas uniquement une planche miniature ;
- vérification hors connexion du HTML autonome ;
- revue de confidentialité indépendante de la revue esthétique.

## 10. Sources et traçabilité

### Sources primaires WotC / D&D Beyond

**[W14]** *D&D Player’s Basic Rules v0.2*, PDF public de 2014, 115 pages détectées à l’ouverture ; échantillons examinés p. 3, 4, 6, 10, 25. Le pied indique autorisation de copie pour usage personnel, pas revente.  
https://media.wizards.com/2014/downloads/dnd/PlayerDnDBasicRules_v0.2.pdf

**[W24]** Michael Galvis, *What’s New in the 2024 Player’s Handbook?*, article officiel effectivement lu par requête HTTP. La réponse actuelle est une version mise à jour, pas nécessairement le texte de lancement inchangé.  
https://www.dndbeyond.com/posts/1745-whats-new-in-the-2024-players-handbook

**[W24-A]** Illustration de Kenny Vo, publiée dans [W24], effectivement vue et conservée pour la recherche :  
https://www.dndbeyond.com/attachments/11/406/phb-172_content_whatsnew_1200x628_v4.jpg

**[W24-P]** Michael Galvis, *Where to Find 2024 Player’s Handbook Previews*, liste officielle des créateurs partenaires et previews. Sert à qualifier les canaux autorisés, pas de preuve d’une page qui n’aurait pas été vue.  
https://www.dndbeyond.com/posts/1747-where-to-find-2024-players-handbook-previews

**[W24-T]** D&D Beyond, *Tracking Sheets*, page publique lue pour récupérer le lien réel au PDF ; feuille examinée : NPC Tracker.  
https://www.dndbeyond.com/sources/dnd/br-2024/tracking-sheets  
https://media.dndbeyond.com/compendium-images/br/dmg/npc-tracker-sheet.pdf

### Source journalistique, distinguée des previews officielles

**[P24]** Benjamin Abbott, GamesRadar+, *Forget classes, my favorite thing about the new D&D Player’s Handbook is its art*, entretien avec Josh Herman ; texte effectivement lu, photographies créditées Benjamin Abbott. Publication journalistique publique, pas scan pirate d’un livre complet ; aucune licence de republication des photos n’est présumée.  
https://www.gamesradar.com/tabletop-gaming/forget-classes-my-favorite-thing-about-the-dandd-2024-players-handbook-is-its-art/

**[P24-A]** Double page d’historiques, effectivement vue :  
https://cdn.mos.cms.futurecdn.net/C5ERz8APbfkjyCQ5o9EQLX.jpg

**[P24-B]** Double page de sous-classes de paladin, effectivement vue :  
https://cdn.mos.cms.futurecdn.net/FLtkmpU3r7DzS4yvkdz7aL.jpg

### Sources officielles Homebrewery

**[H1]** Site et démonstration réellement visités et capturés :  
https://homebrewery.naturalcrit.com/

**[H2]** Dépôt officiel et README. Déclare un outil permettant de produire du contenu à l’apparence D&D et rappelle la responsabilité de l’auteur concernant les droits des ressources.  
https://github.com/naturalcrit/homebrewery  
https://github.com/naturalcrit/homebrewery/blob/699743de1604e0fdc878e3a25cec6a647b407816/README.md

**[H3]** Métadonnées et styles de `5ePHB` ; les sources `master` ont été lues, le commit de tête relevé pour référencement reproductible :  
https://github.com/naturalcrit/homebrewery/blob/699743de1604e0fdc878e3a25cec6a647b407816/themes/V3/5ePHB/settings.json  
https://github.com/naturalcrit/homebrewery/blob/699743de1604e0fdc878e3a25cec6a647b407816/themes/V3/5ePHB/style.less

**[H4]** Styles de base et héritage DMG :  
https://github.com/naturalcrit/homebrewery/blob/699743de1604e0fdc878e3a25cec6a647b407816/themes/V3/Blank/style.less  
https://github.com/naturalcrit/homebrewery/blob/699743de1604e0fdc878e3a25cec6a647b407816/themes/V3/5eDMG/settings.json

**[H5]** Répertoire et arbre officiel interrogés pour rechercher une variante 2024 ; réponse de l’arbre complète (`truncated: false`), aucun chemin contenant `2024`, `5.5` ou `revised`. Cette recherche est croisée avec les noms des thèmes, non utilisée seule pour prouver une absence absolue.  
https://api.github.com/repos/naturalcrit/homebrewery/contents/themes/V3  
https://api.github.com/repos/naturalcrit/homebrewery/git/trees/699743de1604e0fdc878e3a25cec6a647b407816?recursive=1

Le commit GitHub relevé n’est **pas** une preuve du commit déployé sur le site. Le bundle local du projet est une autre référence figée, documentée dans son `PROVENANCE.md`, qui annonçait alors `3.24.1`. Aucune mise à jour du bundle n’a été effectuée pour cette étude.

### Sources locales privées

**[L1]** `sources/chapters/chapter-01-thay/manifest.json`, `README.md` et les fichiers :

- `sources/chapters/chapter-01-thay/assets/illustrations/01-001.ch-1-splash.png`
- `sources/chapters/chapter-01-thay/assets/illustrations/01-003.zulkir.png`

URL de provenance déclarée dans le manifeste, **pas revendiquée comme preview publique consultée** :  
https://www.dndbeyond.com/sources/dnd/aud/chapter-1-thay-dominion-of-red-wizards

**[L2]** `sources/site/politique/homebrewery-officiel/PROVENANCE.md`, contexte d’intégration du thème dans le projet. Les contrôles historiques de ce fichier ne sont pas réattribués à la présente recherche.

### Incidents, limites et mesures réellement prises

- L’outil d’extraction web était indisponible avec le backend configuré ; lecture des pages accessibles par requêtes HTTP, sans contournement d’authentification.
- Le navigateur de l’outil `browser_exec` a échoué avec `chrome-not-running`. Un Chromium headless déjà installé a permis la consultation et les captures du vrai accueil Homebrewery via Playwright. La notification d’accueil a été fermée avant les captures de référence. Aucune connexion à un compte, sauvegarde de brew ou publication n’a été effectuée.
- Les captures initiales avec notification et les échantillons non examinés ne servent pas de preuves de composition ; seuls les échantillons finaux référencés sont retenus.
- PDF publics rendus avec PyMuPDF ; absence de mesure typographique comparative WotC au point près.
- Aucun PDF intégral commercial de provenance douteuse utilisé ; aucun accès payant contourné.
- Les photos GamesRadar ont été vues et séparées des preuves officielles. Les images officielles autonomes ont été séparées des pages imprimées.
- La recherche n’a pas vérifié tous les chapitres, les trois livres de chaque génération ni les traductions françaises officielles.
- Aucune simulation de palette nouvelle ni audit de contraste global n’est revendiqué. Le fond uni de contrôle utilise la valeur HB existante uniquement pour vérifier l’alpha.
- Aucun site, livre HTML/PDF, skill, feuille CSS ou contenu narratif existant modifié. Ce rapport et ses échantillons restent une proposition de travail privée.
