# PROFIL PROJET / APPLICABILITÉ

ÉTAPE: `1-IA1-ANALYSE.md`
CATÉGORIE: `01-PROJECT-PROFILE-APPLICABILITY`

PÉRIMÈTRE
Classifier le projet à partir des documents réels : site vitrine, SaaS, e-commerce, API/backend, application interne, ou combinaison justifiée. Construire et maintenir `.md-ai-system/APPLICABILITY.md` avec chaque catégorie ACTIVE ou N/A, justification et dépendances. Une activation automatique doit être justifiée et enregistrée. Le POLICY_PROFILE (PRODUCTION, STAGING ou POC) est lu depuis `.md-ai-system/CONFIG.json` et ne doit jamais être deviné ; s'il manque, retourner EN_ATTENTE_DE_DÉCISION.

DÉPENDANCES RÉELLES
00-START

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
- `.md-ai-system/state/01-PROJECT-PROFILE-APPLICABILITY.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
