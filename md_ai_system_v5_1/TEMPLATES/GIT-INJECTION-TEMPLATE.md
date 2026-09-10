# GIT INJECTION TEMPLATE

Template unique obligatoire pour les prompts exécutables. Les prompts le référencent au lieu de recopier physiquement toutes les règles.

## Avant toute modification

```bash
git status --porcelain
git branch --show-current
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Règles validées :
- Travailler uniquement sur `main`.
- Ne jamais créer de branche.
- Ne jamais checkout/switch automatiquement.
- Working tree non clean : STOP.
- Modification humaine préexistante : STOP.
- Jamais de stash/reset/clean automatique pour contourner l'état du dépôt.
- Détecter merge, rebase, cherry-pick, revert, bisect et conflits en cours : STOP.
- Enregistrer le SHA distant de `main` au début dans `current_cycle.git.remote_sha_at_start`, avec `head_at_start` et `checked_at`, afin qu'il survive à une interruption.
- Ne pas imposer `git fetch origin main` avant cette vérification initiale.
- Ne pas imposer `HEAD == origin/main` avant IA3.

## Périmètre / staging

- Interdit : `git add -A`.
- Interdit : `git add .`.
- Utiliser uniquement `git add -- <fichiers explicitement autorisés>`.
- Fichier hors périmètre détecté : STOP.
- Exécuter `git diff`, puis `git diff --cached`, puis contrôler le diff du commit final.
- Aucun commit vide.

## Concurrence / push

Avant push, comparer le SHA distant courant à `current_cycle.git.remote_sha_at_start` avec `git ls-remote origin refs/heads/main`.
- Si `remote_sha_at_start` est absent (cycle repris sans vérification initiale) : refaire la vérification initiale avant tout push.
- Si le SHA distant a avancé : STOP ; effectuer ensuite un nouveau fetch pour réévaluation ; aucun merge/rebase automatique.

Après push :
```bash
git fetch origin main
git rev-parse HEAD
git rev-parse refs/remotes/origin/main
git status --porcelain
```

Fin Git uniquement si :
- push réussi ;
- SHA distant vérifié == HEAD ;
- working tree clean.

Rollback :
- non destructif ;
- priorité à `git revert` ;
- jamais de force-push.
