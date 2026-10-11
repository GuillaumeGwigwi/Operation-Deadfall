# Homebrewery pour Operation Deadfall — étude et éléments de rédaction

## Conclusion

Une chaîne locale « fichiers Homebrewery V3 → HTML statique + CSS » est possible sans serveur Homebrewery permanent. Elle a été vérifiée sur les deux gabarits du dossier templates avec marked-hbfm 1.0.1. Le test ne reproduit pas encore l'intégralité de la pagination ni les thèmes officiels du site.

## Trois options

1. Le service Homebrewery en ligne : éditeur avec aperçu. Ne pas y déposer automatiquement les sources protégées ou secrets MJ.
2. L'application complète auto-hébergée : le README documente Node, MongoDB et un serveur local. La branche consultée annonce Node >=26.4.0 dans package.json, tandis que le README parle encore de Node 16 : pour une installation il faut choisir une version précise et suivre ses exigences réelles.[2][6]
3. Le moteur seul : marked-hbfm est le module de NaturalCrit qui rend le Markdown Homebrewery en HTML ; l'application V3 appelle hbfm.render. C'est l'option recommandée pour générer les fiches d'un site statique sans installer tout l'éditeur.[4][7]

## Architecture proposée, non implémentée

- Sources de vérité : notes et fiches de campagne, avec provenance et public MJ/joueurs.
- Documents d'édition : fichiers Homebrewery V3 et feuille CSS Dossier écarlate.
- Compilation locale : validation, découpage des pages, conversion en HTML, ajout du CSS et des ressources autorisées.
- Sortie : fichiers HTML consultables localement ou intégrables dans le futur site ; PDF éventuellement obtenu par impression navigateur.
- Pour du rendu responsive, adapter les colonnes et dimensions fixes à l'écran. Pour de l'impression, garder une mise en page dédiée. Le même HTML brut ne garantit pas les deux résultats.
- Si du contenu non fiable est admis, ajouter une sanitation HTML et des politiques de ressources ; le parseur seul ne suffit pas à sécuriser la publication.
- Séparer les sorties MJ et joueurs au build. Aucun secret MJ dans les fichiers transmis au navigateur joueur.

## Syntaxe vérifiée

V3 ajoute les blocs {{note}}, {{descriptive}}, {{monster,frame}}, le modificateur wide, les listes de définition « **Champ** :: valeur », les ruptures de colonnes et pages, et les tableaux étendus. Les snippets officiels et le document d'accueil décrivent ces formes.[5][8]

hbfm.render traite le Markdown ; pour obtenir une publication fidèle, notre chaîne doit aussi gérer les conteneurs .page, les feuilles de style, les ressources et les ruptures de pages. L'application officielle effectue des opérations supplémentaires avant et autour du rendu.[4]

## Éléments livrés

- templates/stat-block-v3.md : structure vide, champs à compléter, provenance et public.
- templates/fiche-et-tableau-v3.md : description à lire, notes MJ, informations et tableau vide.
- preuve-rendu.html : résultat statique issu du véritable moteur. CSS minimal original de démonstration, pas un thème officiel ni une maquette finale.

Les deux modèles ont passé hbfm.validate sans erreur. Le test vérifie des tableaux HTML et encadrés, ainsi que les classes monster frame et descriptive. Aucun serveur ou MongoDB n'a été démarré ; les dépendances expérimentales sont dans /tmp, pas installées dans le projet. Aucun contrôle visuel de la preuve HTML n'est revendiqué. La compilation de production n'est pas encore installée.

## Règles de rédaction

D&D 5e 2024 reste la version de la campagne. « V3 » est la version de syntaxe Homebrewery, pas l'édition des règles D&D. Le snippet de monstre officiel consulté contient des données aléatoires d'exemple et une structure historique ; il n'est pas une source de statistiques ni une garantie de format D&D 2024.

- Une fiche tirée des sources conserve les nombres, unités, portée, sauvegardes, dégâts, usages et restrictions. Signaler les données manquantes et divergences.
- Séparer mise en forme, traduction, adaptation et création maison.
- Un tableau présent dans les sources est repris fidèlement, sans ajout silencieux de lignes.
- Un tableau absent n'est pas inventé automatiquement : le signaler ; proposer une table maison seulement sur demande, étiquetée et soumise au MJ.
- Ne pas créer ni rendre jouable un monstre pour remplir un gabarit.
- Ne pas supposer que la licence MIT du logiciel couvre les textes, images ou polices tierces ; vérifier les droits des ressources utilisées.[2]

## Suite recommandée

Créer un skill personnel ciblé de rédaction Homebrewery V3, avec ces procédures et modèles, en suivant le guide Hermes officiel ; puis réaliser un petit compilateur testé, avant toute intégration au site. Cette étude livre déjà les éléments de rédaction, mais ne crée pas encore un skill ni ne choisit la technologie du site.

## Sources

[2] https://github.com/naturalcrit/homebrewery/blob/master/README.md
[4] https://github.com/naturalcrit/homebrewery/blob/master/client/homebrew/brewRenderer/brewRenderer.jsx
[5] https://github.com/naturalcrit/homebrewery/blob/master/themes/V3/5ePHB/snippets.js
[6] https://github.com/naturalcrit/homebrewery/blob/master/package.json
[7] https://github.com/naturalcrit/marked-hbfm
[8] https://github.com/naturalcrit/homebrewery/blob/master/client/homebrew/pages/homePage/welcome_msg.md
