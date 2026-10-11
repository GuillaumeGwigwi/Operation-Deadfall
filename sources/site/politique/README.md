# Le pouvoir écarlate — sources du second site

Livrable : `site/politique-thay.html`. Le seul HTML est à partager. CSS, JavaScript et données publiques sont intégrés ; aucune image, police distante, bibliothèque, fichier voisin ou connexion nécessaire.

Sources d’édition :
- `public-data.json` : quatre rôles, huit zulkirs et leurs fonctions publiques, onze gouverneurs/capitales et cinq situations.
- `index.template.html` : interface Dossier écarlate, organigramme des nominations, autorité magique parallèle, annuaires, lois et lecture pratique.

Génération, depuis la racine du projet :

    python3 tools/build_politics.py

Vérification :

    uv run --with playwright python3 tests/test_politics_site.py

Le test copie seulement le HTML dans un dossier vide, le renomme et contrôle les interactions, recherches, vues mobile et ordinateur, clavier et liens internes. Toute ressource externe ou erreur JavaScript fait échouer le contrôle.

La revue des sources et décisions de confidentialité est conservée séparément dans `sources/propositions/politique-thay-mj/revue.md`, hors livraison. Le dossier ne publie ni secrets de personnages, ni portraits révélateurs, ni profils de jeu ou intrigues.

L’organigramme et les orientations pratiques sont une synthèse pédagogique des informations publiques du chapitre 1. Le titre de Magicien Rouge n’est pas présenté comme un poste administratif placé sous l’autharch. L’atlas existant n’est ni modifié ni nécessaire pour utiliser ce site.
