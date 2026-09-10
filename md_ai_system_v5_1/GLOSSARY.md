# GLOSSAIRE — VOCABULAIRE UNIQUE DU SYSTÈME

Ce document ne crée aucune règle. Il fige le sens des termes déjà utilisés par
`COMMON-RULES.md`, `WORKFLOW-RULES.md`, `SOURCE-OF-TRUTH-RULES.md`,
`NEXT-PROMPT-RULES.md`, `POLICY-PROFILES.md` et les templates d'étape.

En cas de doute sur un mot, ce fichier fait référence.
En cas de conflit sur une règle, les fichiers de règles font référence.

## 1. Les quatre IA

| IA | Rôle | Modifie le produit | Écrit dans l'état |
|---|---|---|---|
| IA1 | ANALYSE : exigences réelles + état réel | non | `current_cycle.ia1` |
| IA2 | VÉRIFICATION INDÉPENDANTE d'IA1, en repartant des documents et du réel | non | `current_cycle.ia2` |
| IA3 | EXÉCUTION du périmètre autorisé | oui | `current_cycle.ia3` |
| IA4 | CONTRÔLE final à partir du réel | non | `current_cycle.ia4` + `status` + `last_validation` |

IA1 et IA2 ne sont pas redondantes : IA2 ne vérifie pas le texte d'IA1, elle
refait le constat depuis les sources et compare. Cette double lecture est
volontaire et ne doit jamais être fusionnée.

**IA2 doit être une IA différente d'IA1, et IA4 une IA différente d'IA3.**
Deux IA suffisent : A tient IA1 et IA3, B tient IA2 et IA4. Le nom de l'IA
utilisée est enregistré à chaque étape dans `current_cycle.iaN.provider` et dans
le journal d'audit. Règles complètes : `AI-ROLES-RULES.md`.

## 2. Applicabilité (catégorie)

Champ `applicability` dans `.md-ai-system/state/<CATEGORY>.json`.

- `ACTIVE` — la catégorie s'applique au projet ; elle exécute IA1→IA4.
- `N/A` — la catégorie ne s'applique pas ; elle n'exécute pas IA1→IA4.
- `TO_DEFINE` — l'applicabilité n'a pas encore été décidée par
  `01-PROJECT-PROFILE-APPLICABILITY`.

`N/A` est une applicabilité, jamais un statut.
`TO_DEFINE` n'autorise aucune exécution : une catégorie non décidée n'est pas
exécutable et ne peut pas être considérée comme terminée.

## 3. Statut de catégorie

Champ `status` dans `.md-ai-system/state/<CATEGORY>.json`.
C'est le statut lu par le DAG, les gates et le résolveur de prochain prompt.

| Statut | Sens | Qui peut l'écrire |
|---|---|---|
| `null` | aucun cycle terminé pour cette catégorie | initial |
| `VALIDÉ` | tous les contrôles exigés passent et les preuves obligatoires existent | IA4 uniquement |
| `REFUSÉ` | un écart vérifiable subsiste, ou une preuve obligatoire manque | IA2 ou IA4 |
| `BLOQUÉ` | un obstacle réel empêche d'avancer sur cette catégorie | IA1, IA2, IA3 ou IA4 |
| `EN_ATTENTE_DE_DÉCISION` | une décision humaine/documentaire indispensable manque | IA1, IA2, IA3 ou IA4 |
| `À_RÉÉVALUER` | catégorie déjà validée, un changement pertinent impose un nouveau cycle | IA1..IA4 |
| `EN_REVALIDATION` | le nouveau cycle sur le delta est en cours | IA1..IA4 |
| `TERMINÉ` | statut global de projet, pas de catégorie (voir §4) | `53-FINAL-CLOSURE` |

Règle d'écriture (interprétation unique) :
- seul IA4 peut porter une catégorie à `VALIDÉ` ;
- `VALIDÉ` renvoyé par IA2 est un verdict d'étape, pas une validation de
  catégorie : il signifie « l'analyse d'IA1 est confirmée, IA3 peut être
  autorisée » ;
- `EXÉCUTÉ` renvoyé par IA3 et `ANALYSE` renvoyé par IA1 sont des verdicts
  d'étape et ne sont jamais recopiés dans `status`.

## 4. Statut d'étape (sortie IA)

Champ `STATUT:` du bloc de sortie obligatoire d'une IA. Il décrit le résultat de
l'étape courante, pas l'état durable de la catégorie.

| Étape | Valeurs autorisées | Effet sur `status` de la catégorie |
|---|---|---|
| IA1 | `ANALYSE` | aucun |
| IA2 | `VALIDÉ` | aucun (autorise IA3) |
| IA2 | `REFUSÉ` | `status = REFUSÉ` |
| IA3 | `EXÉCUTÉ` | aucun |
| IA4 | `VALIDÉ` | `status = VALIDÉ` + `last_validation` mis à jour |
| IA4 | `REFUSÉ` | `status = REFUSÉ` |
| toutes | `BLOQUÉ`, `EN_ATTENTE_DE_DÉCISION`, `À_RÉÉVALUER`, `EN_REVALIDATION` | recopié dans `status` |

`TERMINÉ` n'est pas un statut d'étape. Il décrit le projet entier : toutes les
catégories `ACTIVE` sont `VALIDÉ`, aucune catégorie ne reste `TO_DEFINE`, aucune
décision n'est en attente, tests/build/Git sont conformes.

## 5. Mode de travail

Champ `MODE_TRAVAIL:` et `current_cycle.mode`.

- `NEW_WORK` — nouveau périmètre, aucune validation antérieure à préserver.
- `REVALIDATION` — contrôle d'un delta depuis une validation existante.
- `CORRECTION` — reprise du même périmètre après `REFUSÉ`, `BLOQUÉ` ou échec de test.

`MODE_IA3` est distinct : `DRY_RUN` (aucune écriture, aucun commit, aucun push)
ou `EXECUTION`.

## 6. Taxonomie des arrêts

Cinq situations différentes, souvent confondues. Elles n'ajoutent aucun statut :
elles disent quel statut existant utiliser.

| Situation | Statut à écrire | Qui débloque | Revalidation nécessaire |
|---|---|---|---|
| Blocage technique réel (commande absente, accès impossible, dépendance amont non validée) | `BLOQUÉ` | résolution technique ou validation amont | non, reprise en `CORRECTION` |
| Information manquante que l'IA ne peut pas déduire du réel | `EN_ATTENTE_DE_DÉCISION` | réponse humaine ou document | non |
| Décision humaine explicite requise (profil, arbitrage, autorisation) | `EN_ATTENTE_DE_DÉCISION` | humain | non |
| Refus de validation (écart vérifiable subsistant, preuve manquante) | `REFUSÉ` | correction puis nouveau cycle | oui, `CORRECTION` |
| Simple écart à corriger dans le périmètre déjà autorisé | pas d'arrêt, écart traité dans le cycle courant | IA3 | non |

Aucun de ces cas n'autorise à contourner un contrôle, à deviner une valeur, ou à
inventer une preuve.

Conséquences de routage :
- `BLOQUÉ` et `EN_ATTENTE_DE_DÉCISION` ne proposent aucune étape suivante pour la
  catégorie ; les branches indépendantes continuent ;
- la levée est explicite : `status` remis à `null` pour reprendre le cycle en
  cours, ou `À_RÉÉVALUER` pour repartir d'IA1 ;
- `REFUSÉ` repart toujours d'IA1 en mode `CORRECTION`, jamais d'IA3.

## 7. Delta et revalidation

- `delta.relevant = true` signifie : depuis `last_validation.commit`, un
  changement peut invalider la validation précédente.
- Un changement non pertinent (formatage, document sans portée normative,
  fichier hors périmètre de la catégorie) ne déclenche pas de revalidation.
- Une validation existante n'est jamais effacée au démarrage d'un nouveau cycle :
  `last_validation` et `current_cycle` sont deux emplacements distincts.
- La revalidation d'une catégorie déjà `VALIDÉ` exige
  `current_cycle.revalidation_authorized_by_ia4 = true`.

## 8. Termes surchargés — désambiguïsation

| Terme | Sens retenu |
|---|---|
| MANIFEST | `MANIFEST.json` = manifeste machine du système. `MANIFEST-MISE-EN-PLACE-UTILISATION.md` = guide humain. |
| manifest de catégorie | Document produit dans le projet cible (`MEDIA-MANIFEST.md`, `TRACKING-MANIFEST.md`, `PRIVACY-MANIFEST.md`). Sans rapport avec `MANIFEST.json`. |
| STATUT | Dans un bloc de sortie IA : verdict d'étape (§4). Dans un tableau de catégorie métier (ex. audit média par page) : champ métier local, sans effet sur le workflow. |
| SOURCE OF TRUTH | Document de décisions verrouillées du **projet cible**, structuré par `TEMPLATES/SOURCE-OF-TRUTH-TEMPLATE.md`. Ce n'est pas un fichier du système. |
| état | `.md-ai-system/**` = état machine du workflow. « état réel » dans un prompt = état constaté du produit. |
| priorité | `execution_priority` = ordre d'exécution. `reading_order` = ordre de lecture. Priorité documentaire = arbitrage entre documents contradictoires (`COMMON-RULES.md`). Trois notions distinctes. |
| ORDRE | `READING-ORDER.md` = lecture. `EXECUTION-MATRIX.md` + `DEPENDENCY-GRAPH.json` = exécution. Jamais une chaîne N→N+1. |

## 9. Indépendance vis-à-vis du fournisseur d'IA

Aucune règle du système ne dépend d'un modèle ou d'un éditeur particulier.
Lorsqu'un document mentionne « workspace VS Code », il désigne l'environnement de
travail donnant à l'IA un accès direct aux fichiers du projet. Toute IA disposant
d'un accès équivalent (lecture de fichiers et, si disponible, terminal) applique
la même règle sans adaptation.

Si l'IA n'a pas d'accès direct aux fichiers, elle doit le déclarer explicitement
et s'arrêter plutôt que de reconstruire de mémoire le contenu d'un document.
