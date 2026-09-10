# COOKIES / CONSENTEMENT / PRIVACY UX

ÉTAPE: `3-IA3-EXECUTION.md`
CATÉGORIE: `27-COOKIE-CONSENT-PRIVACY`

PÉRIMÈTRE
Traiter le Consent Management comme une catégorie complète. Aucun tracker non essentiel avant consentement lorsque la réglementation applicable l'exige. Premier niveau : Accepter / Refuser / Personnaliser avec refus aussi simple que l'acceptation. Catégories séparées : nécessaires, analytics, marketing, personnalisation si applicable. Aucune case précochée pour consentement requis. Consentement explicite, modification/révocation ultérieure, lien permanent “Gérer mes cookies”, conservation de l'état, version du texte, date si nécessaire, intégration analytics/ads, chargement conditionnel des scripts, fonctionnement sans JS tiers, clavier, responsive, CLS maîtrisé, aucun dark pattern.

Créer/maintenir : `COOKIE-CONSENT-RULES.md`, `PRIVACY-MANIFEST.md`, `TRACKING-MANIFEST.md`, `CONSENT-STATE.md`.
Relier explicitement : consentement → scripts autorisés → analytics → marketing → événements commerciaux → preuve du choix.
Le détail juridique dépend des services réellement installés et de la juridiction applicable ; ne jamais inventer la juridiction.

DÉPENDANCES RÉELLES
23-INTEGRATIONS

PROJECT_PROFILES CONCERNÉS
all

LECTURES SYSTÈME OBLIGATOIRES — à lire directement dans le workspace VS Code
- `TEMPLATES/STAGES/3-IA3-EXECUTION.md`
- `COMMON-RULES.md`
- `TEMPLATES/GIT-INJECTION-TEMPLATE.md`
- `WORKFLOW-RULES.md`
- `SOURCE-OF-TRUTH-RULES.md`
- `POLICY-PROFILES.md`
- `NEXT-PROMPT-RULES.md`
- `.md-ai-system/state/27-COOKIE-CONSENT-PRIVACY.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
