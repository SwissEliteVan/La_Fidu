# STAGING / DÉPLOIEMENT

ÉTAPE: `1-IA1-ANALYSE.md`
CATÉGORIE: `47-STAGING-DEPLOY`

PÉRIMÈTRE
Préparer staging puis production selon les `.md`. Contrôler env/secrets, build, HTTPS/SSL, domaine, cache, headers, redirections, robots/sitemap, staging noindex si requis, smoke tests, Lighthouse si prévu, rollback et vérification post-déploiement. Vérifier que la production est indexable si elle doit l'être.

DÉPENDANCES RÉELLES
44-TESTING, 46-ENV-PARITY

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
- `.md-ai-system/state/47-STAGING-DEPLOY.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
