# DÉPENDANCES / VULNÉRABILITÉS

ÉTAPE: `1-IA1-ANALYSE.md`
CATÉGORIE: `33-DEPENDENCY-AUDIT`

PÉRIMÈTRE
Vérifier versions, lockfile, dépendances inutiles, vulnérabilités connues et compatibilités. Corriger sans upgrade majeur non validé.

DÉPENDANCES RÉELLES
02-STACK

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
- `.md-ai-system/state/33-DEPENDENCY-AUDIT.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
