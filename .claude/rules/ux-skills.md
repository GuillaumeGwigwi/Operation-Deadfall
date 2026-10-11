# Skills UX locaux — Operation Deadfall

Les quatre skills sont installés au niveau de ce projet, dans `.claude/skills/`, et non comme plugins globaux :
- `frontend-design` : direction visuelle et interfaces.
- `web-design-guidelines` : revue d'accessibilité et d'ergonomie web.
- `vercel-composition-patterns` : architecture de composants React, si React est effectivement utilisé.
- `ui-ux-pro-max` : recherche locale de recommandations UX et de design.

Utiliser les skills pertinents selon la tâche ; leur installation ne choisit pas de framework et ne valide aucune proposition de design.

## Adaptation UI/UX Pro Max à l'installation locale WSL

Les exemples du skill mentionnent `${CLAUDE_PLUGIN_ROOT}`, variable de plugin qui n'est pas requise pour cette installation de projet. Ici, utiliser directement ce chemin et `python3` (la commande `python` n'est pas disponible) :

```sh
python3 /home/gwi/Operation-Deadfall/.claude/skills/ui-ux-pro-max/scripts/search.py "keyboard focus modal" --domain ux
```

Ne pas définir de variable globale pour contourner cela. Les recherches sont locales ; ne pas inclure de secrets de campagne dans des requêtes réseau. Ne pas persister un système de design ni modifier l'interface existante sans tâche correspondante du MJ. Préserver les sources de campagne et la séparation MJ/joueurs. Aucun commit ou push sans demande.

## Provenance

Installés depuis `anthropics/skills`, `vercel-labs/agent-skills` et `nextlevelbuilder/ui-ux-pro-max-skill` via `npx skills add`, avec sélection explicite de Claude Code et copie au niveau projet. Le fichier `skills-lock.json` à la racine contient les références enregistrées par l'installateur. `.agents/skills/` contient également les copies de référence de l'installateur, dans le même dépôt.
