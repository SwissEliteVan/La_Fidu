# SÉCURITÉ / LÉGAL

ÉTAPE: `4-IA4-CONTROLE.md`
CATÉGORIE: `32-SECURITY-LEGAL`

PÉRIMÈTRE
Toujours : secrets hors Git, .env.example, validation serveur si applicable, dépendances, headers et exposition minimale. Selon besoin : CSP, CORS, CSRF, rate limiting, sessions/auth, webhooks, anti-spam, conservation/suppression des données et obligations légales. La conformité consentement reste pilotée par sa catégorie dédiée.

DÉPENDANCES RÉELLES
05-DATA-BACKEND-AUTH, 27-COOKIE-CONSENT-PRIVACY

PROJECT_PROFILES CONCERNÉS
all

LECTURES SYSTÈME OBLIGATOIRES — à lire directement dans le workspace VS Code
- `TEMPLATES/STAGES/4-IA4-CONTROLE.md`
- `COMMON-RULES.md`
- `TEMPLATES/GIT-INJECTION-TEMPLATE.md`
- `WORKFLOW-RULES.md`
- `SOURCE-OF-TRUTH-RULES.md`
- `POLICY-PROFILES.md`
- `NEXT-PROMPT-RULES.md`
- `.md-ai-system/state/32-SECURITY-LEGAL.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
