# README / DOCUMENTATION PROJET

ÉTAPE: `1-IA1-ANALYSE.md`
CATÉGORIE: `51-README-DOCUMENTATION`

PÉRIMÈTRE
Créer ou mettre à jour automatiquement le `README.md` RÉEL du projet depuis l'état réel, jamais depuis des suppositions. Les chemins, commandes et dépendances doivent être vrais.

Structure minimale :
# Nom du projet
## Objectif
## Stack
## Prérequis
## Installation
## Variables d'environnement
## Commandes
- dev
- lint
- typecheck
- test
- build
- e2e
## Architecture
## Routes / pages
## Médias
- hero vidéo
- images
- blog
- OG
- favicon
- Apple Touch Icon
## Base de données
si applicable
## Intégrations
si applicable
## Tests
## Déploiement
## Rollback
## SOURCE OF TRUTH
## État du projet
## Limitations connues

Si une section n'est pas applicable, l'indiquer explicitement sans inventer de contenu.

DÉPENDANCES RÉELLES
44-TESTING, 47-STAGING-DEPLOY, 49-RELEASE-VERSIONING-CHANGELOG

PROJECT_PROFILES CONCERNÉS
all

LECTURES SYSTÈME OBLIGATOIRES — à lire directement dans le workspace VS Code
- `TEMPLATES/STAGES/1-IA1-ANALYSE.md`
- `COMMON-RULES.md`
- `TEMPLATES/GIT-INJECTION-TEMPLATE.md`
- `WORKFLOW-RULES.md`
- `SOURCE-OF-TRUTH-RULES.md`
- `POLICY-PROFILES.md`
- `NEXT-PROMPT-RULES.md`
- `.md-ai-system/state/51-README-DOCUMENTATION.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
