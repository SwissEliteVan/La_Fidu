# APPLICATION INTERNE / GOUVERNANCE

ÉTAPE: `3-IA3-EXECUTION.md`
CATÉGORIE: `08-INTERNAL-APP-GOVERNANCE`

PÉRIMÈTRE
Pour application interne : RBAC, permissions métier, audit log, administration, import/export et séparation stricte des privilèges.

DÉPENDANCES RÉELLES
05-DATA-BACKEND-AUTH

PROJECT_PROFILES CONCERNÉS
internal_app

LECTURES SYSTÈME OBLIGATOIRES — à lire directement dans le workspace VS Code
- `TEMPLATES/STAGES/3-IA3-EXECUTION.md`
- `COMMON-RULES.md`
- `TEMPLATES/GIT-INJECTION-TEMPLATE.md`
- `WORKFLOW-RULES.md`
- `SOURCE-OF-TRUTH-RULES.md`
- `POLICY-PROFILES.md`
- `NEXT-PROMPT-RULES.md`
- `.md-ai-system/state/08-INTERNAL-APP-GOVERNANCE.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
