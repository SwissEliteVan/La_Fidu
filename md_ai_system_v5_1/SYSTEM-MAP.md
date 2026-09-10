# CARTE DU SYSTÈME MARKDOWN

Inventaire de tous les documents du système, de leur rôle, de qui les lit, de qui
les écrit et de leur autorité. Cette carte est descriptive : elle ne remplace
aucune règle.

Vocabulaire : `GLOSSARY.md`.

## 1. Niveaux d'autorité

| Niveau | Signification | Modifiable pendant un projet |
|---|---|---|
| N0 | Règle système normative. Toute IA doit s'y conformer. | Non, sauf décision explicite de l'utilisateur |
| N1 | Décision projet verrouillée (SOURCE OF TRUTH, `DECISIONS.json`). | Uniquement via la procédure de modification de décision verrouillée |
| N2 | État machine du workflow. | Oui, par les IA, via les champs prévus |
| N3 | Document produit dans le projet cible. | Oui, par IA3 dans le périmètre autorisé |
| N4 | Guide humain / rapport généré. Non normatif. | Régénéré ou édité hors workflow |

L'autorité N0→N4 arbitre les documents **du système**.
La priorité documentaire de `COMMON-RULES.md` arbitre les documents **du projet
cible**. Les deux ne se contredisent pas : elles portent sur des objets
différents.

## 2. Règles système (N0)

| Document | Rôle | Lu par | Écrit par | Dépend de |
|---|---|---|---|---|
| `COMMON-RULES.md` | Règles transverses, priorité documentaire projet, interdiction d'invention | IA1..IA4, à chaque étape | utilisateur | `GLOSSARY.md` |
| `WORKFLOW-RULES.md` | Statuts, DAG, delta/revalidation, état persistant, reprise, risque | IA1..IA4 | utilisateur | `GLOSSARY.md` |
| `SOURCE-OF-TRUTH-RULES.md` | Contenu minimal d'une décision verrouillée et procédure de modification | IA1..IA4 | utilisateur | `TEMPLATES/SOURCE-OF-TRUTH-TEMPLATE.md` |
| `NEXT-PROMPT-RULES.md` | Routage : sélection et format du prochain prompt | IA1..IA4 (fin d'étape) | utilisateur | `TOOLS/next_prompt.py`, `MANIFEST.json` |
| `POLICY-PROFILES.md` | Niveau de rigueur PRODUCTION / STAGING / POC | IA1..IA4 | utilisateur | `.md-ai-system/CONFIG.json` |
| `PROJECT-PROFILES.md` | Types de projet et effet sur l'applicabilité | IA1, IA2 (surtout `01`) | utilisateur | — |
| `TEMPLATES/GIT-INJECTION-TEMPLATE.md` | Règles Git uniques et centralisées | IA1..IA4 | utilisateur | `POLICY-PROFILES.md` |
| `TEMPLATES/STAGES/1-IA1-ANALYSE.md` | Format de sortie + règles d'IA1 | IA1 | utilisateur | `GLOSSARY.md`, `NEXT-PROMPT-RULES.md` |
| `TEMPLATES/STAGES/2-IA2-VERIFICATION.md` | Format de sortie + règles d'IA2 | IA2 | utilisateur | idem |
| `TEMPLATES/STAGES/3-IA3-EXECUTION.md` | Format de sortie + règles d'IA3 | IA3 | utilisateur | idem |
| `TEMPLATES/STAGES/4-IA4-CONTROLE.md` | Format de sortie + règles d'IA4 | IA4 | utilisateur | idem |
| `AI-ROLES-RULES.md` | Double contrôle : IA2 ≠ IA1, IA4 ≠ IA3, traçabilité du fournisseur | IA1..IA4 | utilisateur | `.md-ai-system/CONFIG.json` |
| `GLOSSARY.md` | Sens unique des termes et des statuts | IA1..IA4 en cas de doute | utilisateur | — |
| `PROMPTS/<CATÉGORIE>/<ÉTAPE>.md` | Périmètre métier de la catégorie + lectures obligatoires | l'IA de l'étape | générateur du système | templates d'étape, `MANIFEST.json` |

## 3. Référentiels de structure (N0, machine)

| Document | Rôle | Lu par | Écrit par |
|---|---|---|---|
| `MANIFEST.json` | Manifeste machine : 54 catégories, priorités, dépendances, gates, profils, empreintes | `TOOLS/*.py`, `TESTS/`, IA si nécessaire | générateur / maintenance validée |
| `DEPENDENCY-GRAPH.json` | Graphe machine (nœuds, arêtes, cycles) | `TESTS/`, IA | générateur |
| `EXECUTION-MATRIX.md` | Vue humaine du même graphe : priorité, dépendances, gate, profils | IA, utilisateur | générateur |
| `READING-ORDER.md` | Ordre de lecture documentaire, distinct de l'exécution | IA, utilisateur | générateur |
| `ORDER.md` | Aiguillage entre ordre de lecture, ordre d'exécution et graphe | IA, utilisateur | générateur |
| `SNAPSHOTS.json` | Empreintes SHA-256 des 216 prompts | `TOOLS/validate_system.py` | générateur |
| `TEMPLATES/CONFIG-TEMPLATE.json` | Gabarit de `.md-ai-system/CONFIG.json` | installation | générateur |
| `TEMPLATES/APPLICABILITY-TEMPLATE.md` | Gabarit de la matrice d'applicabilité | IA3 de `01` | générateur |
| `TEMPLATES/SOURCE-OF-TRUTH-TEMPLATE.md` | Gabarit de la SOURCE OF TRUTH du projet | IA3/IA4 | générateur |

**Le graphe de dépendances existe en quatre exemplaires cohérents**
(`MANIFEST.json`, `DEPENDENCY-GRAPH.json`, `EXECUTION-MATRIX.md`,
`.md-ai-system/state/*.json`). Cette redondance est volontaire — machine, humain
et état — mais elle doit être vérifiée : `python TOOLS/validate_system.py`.

## 4. État persistant du projet (N1/N2)

| Fichier | Rôle | Lu par | Écrit par | Autorité |
|---|---|---|---|---|
| `.md-ai-system/CONFIG.json` | `policy_profile` + `project_profiles` | IA1..IA4 | IA après décision humaine explicite | N1 |
| `.md-ai-system/state/<CATÉGORIE>.json` | État atomique par catégorie : applicabilité, statut, cycle courant, dernière validation, blocages | `TOOLS/*.py`, IA de l'étape | IA de l'étape | N2 — **source de vérité de l'état** |
| `.md-ai-system/STATE.json` | Index global dérivé des états par catégorie | IA, lecture rapide | `TOOLS/state_index.py` | N2 — dérivé, jamais prioritaire sur `state/*.json` |
| `.md-ai-system/STATE-OVERVIEW.md` | Vue humaine générée | utilisateur | `TOOLS/state_overview.py` | N4 — jamais édité à la main |
| `.md-ai-system/DECISIONS.json` | Registre global des décisions verrouillées (schéma : `SOURCE-OF-TRUTH-RULES.md`) | IA1..IA4 | IA4 lors du verrouillage | N1 |
| `.md-ai-system/AUDIT.jsonl` | Journal append-only des transitions importantes (format : `WORKFLOW-RULES.md` §Audit) | audit humain, reprise | `TOOLS/audit_append.py` | N2 |
| `.md-ai-system/APPLICABILITY.md` | Matrice d'applicabilité justifiée par catégorie | IA1..IA4 | IA3 de `01-PROJECT-PROFILE-APPLICABILITY` | N1 |

Reprise après interruption : lire `state/<CATÉGORIE>.json` de la catégorie
concernée, puis `STATE.json`, puis `AUDIT.jsonl` seulement si l'état paraît
incohérent. Aucune reprise ne nécessite l'historique de conversation.

## 5. Documents produits dans le projet cible (N3)

Produits et maintenus par IA3, verrouillés par IA4 dans la SOURCE OF TRUTH.
Ils appartiennent au projet, pas au système.

| Catégorie | Documents |
|---|---|
| `11-MARKETING-BRAND-DIFFERENTIATION` | `MARKETING-STRATEGY.md`, `BRAND-DIFFERENTIATION.md`, `MESSAGING.md`, `ART-DIRECTION.md` |
| `17-MEDIA-HERO-IMAGES-BLOG` | `MEDIA-MANIFEST.md`, `HERO-VIDEO-RULES.md`, `MOTION-LIBRARIES.md` |
| `19-COMMERCIAL-FUNNEL-CONVERSION` | `COMMERCIAL-STRATEGY.md`, `FUNNEL-CONVERSION.md`, `CTA-MAP.md`, `POPUP-RULES.md`, `CONVERSION-EVENTS.md` |
| `27-COOKIE-CONSENT-PRIVACY` | `COOKIE-CONSENT-RULES.md`, `PRIVACY-MANIFEST.md`, `TRACKING-MANIFEST.md`, `CONSENT-STATE.md` |
| toutes | SOURCE OF TRUTH du projet, README réel du projet (`51-README-DOCUMENTATION`) |

## 6. Guides et rapports (N4)

| Document | Rôle | Normatif |
|---|---|---|
| `README.md` | Point d'entrée et index du système | non |
| `MANIFEST-MISE-EN-PLACE-UTILISATION.md` | Guide humain d'installation et d'utilisation | non |
| `SYSTEM-MAP.md` | Ce document | non |
| `SYSTEM-AUDIT-REPORT.md` | Rapport d'audit et plan d'optimisation | non |
| `STRUCTURAL-VALIDATION.md` | Rapport de build : structure | non |
| `FUNCTIONAL-VALIDATION.md` | Rapport de build : couverture fonctionnelle | non |

Un rapport ne crée jamais une règle. Une IA qui trouve une contradiction entre un
rapport et une règle applique la règle et signale la contradiction.

## 7. Hiérarchie de lecture (économie de contexte)

Une IA ne lit jamais tout le système. Elle lit dans cet ordre et s'arrête dès
qu'elle a ce qu'il lui faut.

```text
1. OBLIGATOIRE  → le prompt de l'étape (PROMPTS/<CATÉGORIE>/<ÉTAPE>.md)
                  et les lectures système qu'il liste
2. CATÉGORIE    → les documents projet du périmètre de la catégorie
                  + SOURCE OF TRUTH + DECISIONS.json
3. ÉTAT COURANT → .md-ai-system/state/<CATÉGORIE>.json puis STATE.json
4. À LA DEMANDE → GLOSSARY.md (doute de vocabulaire),
                  EXECUTION-MATRIX.md / DEPENDENCY-GRAPH.json (routage),
                  AUDIT.jsonl (état incohérent), historique projet
                  (contradiction à trancher)
```

Ne jamais scanner l'ensemble du dépôt. Ne jamais relire les 216 prompts.
Ne jamais relire une catégorie non concernée par l'étape courante.

## 8. Outils

| Outil | Rôle | Écrit |
|---|---|---|
| `TOOLS/state_overview.py` | Régénère la vue humaine | `.md-ai-system/STATE-OVERVIEW.md` |
| `TOOLS/state_index.py` | Régénère l'index global depuis les états par catégorie | `.md-ai-system/STATE.json` |
| `TOOLS/next_prompt.py` | Calcule le prochain prompt exécutable | rien |
| `TOOLS/mdai.py` | **Commande unique** : init, check, status, next, git-snapshot, finish-stage, set, promote, explain, unblock | état, audit, index, vue |
| `TOOLS/audit_append.py` | Ajoute une transition validée au journal d'audit | `.md-ai-system/AUDIT.jsonl` |
| `TOOLS/validate_system.py` | Vérifie la cohérence interne du système (14 contrôles) | rien |
| `TESTS/test_generated_system.py` | Tests unitaires du système généré | rien |

Ordre de fin d'étape, automatisé par une seule commande :

```text
python TOOLS/mdai.py finish-stage --category <CAT> --stage <1..4> --ai <IA> \
    --verdict <VERDICT> --summary "<résumé>" [--commit <sha>]
```

Elle enchaîne : contrôle du double contrôle → mise à jour de l'état → audit →
`STATE.json` → `STATE-OVERVIEW.md` → prochain prompt et IA attendue.
