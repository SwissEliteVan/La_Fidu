# SOURCE OF TRUTH / VERROUILLAGE

ÉTAPE: `2-IA2-VERIFICATION.md`
CATÉGORIE: `52-SOURCE-OF-TRUTH-LOCK`

PÉRIMÈTRE
Consolider uniquement les décisions validées. Vérifier cohérence code ↔ documentation, tests associés, état Git, limitations et décisions en attente. Appliquer la procédure stricte à toute modification d'une décision verrouillée. Vérifier les hashes des fichiers critiques déclarés.

DÉPENDANCES RÉELLES
51-README-DOCUMENTATION

PROJECT_PROFILES CONCERNÉS
all

LECTURES SYSTÈME OBLIGATOIRES — à lire directement dans le workspace VS Code
- `TEMPLATES/STAGES/2-IA2-VERIFICATION.md`
- `COMMON-RULES.md`
- `TEMPLATES/GIT-INJECTION-TEMPLATE.md`
- `WORKFLOW-RULES.md`
- `SOURCE-OF-TRUTH-RULES.md`
- `POLICY-PROFILES.md`
- `NEXT-PROMPT-RULES.md`
- `.md-ai-system/state/52-SOURCE-OF-TRUTH-LOCK.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
