# Conventions du projet Operation Deadfall

## Sites à partager

Tous les sites demandés pour ce projet doivent être livrés en fichiers HTML autonomes dans `site/`.

Chaque HTML livré doit embarquer son CSS, son JavaScript, ses données, ses images et, si nécessaire, ses polices. Il doit rester utilisable après copie du seul fichier dans un dossier vide, sans serveur, installation ni connexion Internet. Aucun CDN, fichier voisin, import JavaScript, feuille CSS externe ou image externe ne peut être nécessaire à son fonctionnement.

Les sources d’édition peuvent être séparées, mais elles restent dans `sources/site/`, et les outils de génération dans `tools/`. Ne pas présenter un ensemble HTML + JS + CSS + assets comme le livrable final.

Vérifier dans un navigateur une copie isolée du HTML : images, interactions, mobile et absence de requêtes vers des fichiers voisins ou Internet. Signaler la taille du fichier si les images rendent le partage volumineux.

## Public joueurs

« Pour les joueurs » signifie sans spoilers, y compris dans les données, images, noms de fichiers, métadonnées et code embarqués. Ne pas embarquer les sources MJ, même masquées dans l’interface. Une exception de divulgation validée par le MJ doit rester limitée à son périmètre et être consignée dans les notes de campagne, hors du livrable.

## Illustrations et rédaction

Utiliser d’abord les assets récupérés du projet, puis chercher sur le web si aucun asset pertinent ne convient. Créer une image seulement en dernier recours. Vérifier la confidentialité et la pertinence d’une image avant de l’embarquer ; ne pas présenter une illustration générique comme un portrait identifié. Embarquer les images dans le HTML sans métadonnées superflues.

Supprimer les phrases de remplissage et les répétitions éditoriales ; conserver les faits utiles et les libellés nécessaires aux interactions.
