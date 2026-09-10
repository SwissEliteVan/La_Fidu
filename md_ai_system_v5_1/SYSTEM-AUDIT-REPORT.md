# AUDIT DU SYSTÈME MARKDOWN — RAPPORT ET PLAN

Portée : les 237 fichiers `.md` du système (216 prompts + 21 documents), plus les
JSON et outils dont ils dépendent.
Méthode : 7 passes — inventaire, contradictions, architecture, optimisation,
automatisation, validation, test par scénarios.
Principe appliqué : la structure existante est intentionnelle. Aucune catégorie,
aucune IA, aucun contrôle n'a été supprimé ni fusionné.

Rapport de contrôle exécutable : `python TOOLS/validate_system.py`.

## 1. Carte des Markdown

La carte complète est un document à part, destiné à être relu :
**`SYSTEM-MAP.md`** — rôle, lu par, écrit par, autorité, dépendances,
modifiable ou verrouillé, pour chaque fichier, plus la hiérarchie de lecture.

Résumé de la structure réelle :

| Famille | Fichiers | Autorité |
|---|---|---|
| Règles système | `COMMON-RULES`, `WORKFLOW-RULES`, `SOURCE-OF-TRUTH-RULES`, `NEXT-PROMPT-RULES`, `POLICY-PROFILES`, `PROJECT-PROFILES`, `DEPLOYMENT-CONSTRAINTS`, `GLOSSARY`, `TEMPLATES/GIT-INJECTION-TEMPLATE`, `TEMPLATES/STAGES/*` | N0 |
| Prompts | `PROMPTS/<54 catégories>/<4 étapes>.md` | N0 |
| Structure machine | `MANIFEST.json`, `DEPENDENCY-GRAPH.json`, `EXECUTION-MATRIX.md`, `READING-ORDER.md`, `ORDER.md`, `SNAPSHOTS.json` | N0 |
| État projet | `.md-ai-system/**` | N1/N2 |
| Documents produits | SOURCE OF TRUTH, `MEDIA-MANIFEST.md`, `CTA-MAP.md`, … | N3 |
| Guides et rapports | `README`, `MANIFEST-MISE-EN-PLACE-UTILISATION`, `SYSTEM-MAP`, ce rapport, `STRUCTURAL-VALIDATION`, `FUNCTIONAL-VALIDATION` | N4 |

Les 216 prompts sont structurellement homogènes : même squelette, seuls le titre,
le périmètre métier, les dépendances, les profils et l'état lu varient. Cette
homogénéité est un atout : elle rend le système parsable et vérifiable.

## 2. Contradictions et ambiguïtés trouvées

Gravité : **A** = casse le workflow, **B** = fait diverger deux IA, **C** = coût ou confusion.

| # | Constat | Gravité | Traitement |
|---|---|---|---|
| C-01 | `VALIDÉ` renvoyé par IA2 et `VALIDÉ` de catégorie sont le même mot. Lu littéralement, un `VALIDÉ` d'IA2 écrit dans `status` valide la catégorie avant toute exécution et arrête le cycle avant IA3/IA4. | A | Corrigé (documentation) : `GLOSSARY.md` §3-§4, `WORKFLOW-RULES.md`, templates d'étape |
| C-02 | Le guide humain donnait en exemple le chemin PROMPTS/01-STACK/2-IA2-VERIFICATION.md, inexistant. | B | Corrigé → `02-STACK` |
| C-03 | `TERMINÉ` est défini comme statut mais n'est produit par aucune étape ni aucun outil ; un projet fini retourne seulement `NONE`. | C | Corrigé : `next_prompt.py` énonce la clôture et la cause exacte de `NONE` |
| C-04 | `TO_DEFINE` est la valeur initiale de 52 catégories sur 54 et n'était définie nulle part. | A | Corrigé : défini dans `GLOSSARY.md`, `COMMON-RULES.md`, `NEXT-PROMPT-RULES.md` |
| C-05 | `.md-ai-system/STATE.json` (index global lu par tous les prompts) n'avait aucun générateur : deux sources de vérité pour l'applicabilité. | A | Corrigé : `TOOLS/state_index.py` + contrôle 7 du validateur |
| C-06 | `.md-ai-system/APPLICABILITY.md` est produit par `01` mais absent de l'inventaire d'état persistant. | B | Corrigé dans `WORKFLOW-RULES.md` |
| C-07 | `AUDIT.jsonl` n'a ni schéma, ni écrivain défini : chaque IA inventerait son format. | B | Corrigé : schéma dans `WORKFLOW-RULES.md` §Audit + `TOOLS/audit_append.py` + contrôle 13 |
| C-08 | `DECISIONS.json` n'a pas de schéma d'entrée, alors que la structure côté SOURCE OF TRUTH est spécifiée. | B | Corrigé : schéma dans `SOURCE-OF-TRUTH-RULES.md` + contrôle 14 |
| C-09 | `MANIFEST.file_hashes` mélange fichiers système immuables et état runtime mutable : l'invariant est invérifiable en l'état. | C | Corrigé : `file_hashes` (248 fichiers système) séparé de `runtime_files` (59 fichiers d'exécution) |
| C-10 | `STRUCTURAL-VALIDATION.md` et `FUNCTIONAL-VALIDATION.md` affichent `PASS` figé et peuvent être lus comme des règles. | C | Corrigé : bandeau « rapport de build, non normatif » |
| C-11 | La priorité documentaire tenait en une phrase avec des `>` : rang de `DECISIONS.json` et égalité de rang non tranchés. | B | Corrigé : liste ordonnée + règles de départage dans `COMMON-RULES.md` |
| C-12 | « workspace VS Code » apparaît dans les 216 prompts et les règles : dépendance apparente à un éditeur. | B | Corrigé sans toucher aux prompts : clause d'équivalence générique (`GLOSSARY.md` §9, `NEXT-PROMPT-RULES.md`) |
| C-13 | `STATUT` désigne à la fois un verdict d'étape et un champ métier (audit média par page). | C | Corrigé : `GLOSSARY.md` §8 |
| C-14 | « MANIFEST » désigne trois objets différents (manifeste machine, guide humain, manifestes métier). | C | Corrigé : `GLOSSARY.md` §8 |
| C-15 | L'emplacement des documents produits (`MEDIA-MANIFEST.md`, `CTA-MAP.md`, …) n'est spécifié nulle part : deux IA les créeront à deux endroits. | B | Corrigé : règle unique dans `COMMON-RULES.md` |
| C-16 | Le template Git impose d'enregistrer le SHA distant initial sans dire où : l'information est perdue à la reprise. | B | Corrigé : `current_cycle.git` dans l'état de catégorie |
| C-17 | **Routage** : après un refus d'IA2, le résolveur propose IA3. | A | Corrigé : `REFUSÉ` repart d'IA1 (§7, S3) |
| C-18 | **Routage** : une catégorie `BLOQUÉ` continue d'avancer d'étape et capte la priorité au lieu de laisser passer une branche indépendante. | A | Corrigé : `BLOQUÉ` ne propose plus d'étape (§7, S4 et S9) |
| C-19 | **Gate** : `gate_ready` n'examine que les catégories `ACTIVE` ; `52` et `53` peuvent donc passer avec 50 catégories encore `TO_DEFINE`. | A | Corrigé : `TO_DEFINE` bloque les gates (§7, S11) |
| C-20 | Le graphe de dépendances existe en quatre exemplaires sans aucun contrôle de cohérence. | B | Corrigé : contrôles 3, 4, 5, 6 de `TOOLS/validate_system.py` |
| C-21 | Aucune contrainte d'hébergement ni d'interdiction de fournisseurs externes n'existait, alors que le projet impose Hostinger et l'auto-hébergement. | A | Ajouté sur demande : `DEPLOYMENT-CONSTRAINTS.md` + bloc `deployment` dans `CONFIG.json` |

## 3. Doublons réellement inutiles

**Aucun doublon n'a été supprimé.** Les redondances examinées sont volontaires ou
utiles :

| Redondance | Verdict |
|---|---|
| Les 9 lectures système répétées dans les 216 prompts | **Conserver.** Chaque prompt doit être autoportant : une IA qui n'a que ce fichier doit savoir quoi lire. Le texte des règles n'est pas dupliqué, seulement la liste. |
| IA1 et IA2 refont le même constat | **Conserver.** C'est le mécanisme de vérification indépendante, pas une redondance. |
| `ORDER.md` (3 lignes) pointant vers `READING-ORDER` et `EXECUTION-MATRIX` | **Conserver.** Aiguillage à coût nul contre une confusion fréquente. |
| Titres des catégories dans `READING-ORDER.md` et `MANIFEST.json` | **Conserver.** Vue humaine + vue machine, désormais vérifiées identiques (contrôle 5). |
| Statuts expliqués dans `WORKFLOW-RULES.md` et dans le guide humain §9 | **Conserver.** Public différent ; les deux versions ont été alignées. |
| Dépendances présentes dans manifeste, graphe, matrice et états | **Conserver.** Redondance de sûreté, désormais vérifiée automatiquement. |

Le seul texte réellement supprimé est la phrase de priorité documentaire de
`COMMON-RULES.md`, remplacée par la liste ordonnée équivalente.

## 4. À conserver absolument (vérifié après optimisation)

- Les 54 entrées de workflow et leurs noms exacts.
- Les 4 IA, leurs rôles distincts et l'indépendance d'IA2 vis-à-vis d'IA1.
- Les 216 prompts, leurs chemins et leur contenu (empreintes `SNAPSHOTS.json` inchangées).
- Les statuts, l'applicabilité `N/A`, les modes `NEW_WORK` / `REVALIDATION` / `CORRECTION`, `DRY_RUN` / `EXECUTION`.
- Le DAG, `execution_priority`, les gates `52` et `53`.
- La révalidation par delta, la préservation de `last_validation`, l'autorisation IA4.
- La SOURCE OF TRUTH, les décisions verrouillées, la procédure de modification.
- L'état persistant par catégorie, l'index, la vue générée, l'audit.
- Toutes les règles Git : `main` seulement, arrêt sur working tree non clean,
  arrêt sur modification humaine, interdiction de `git add -A` / `git add .`,
  staging explicite, contrôle du SHA distant, rollback non destructif, pas de force-push.
- Les profils projet et les profils de rigueur, jamais devinés.
- L'intervention humaine limitée aux décisions réellement nécessaires.
- Le protocole `NEXT_PROMPT_PATH` / `NEXT_PROMPT_TO_SEND` / `NEXT_PROMPT_REASON`.

## 5. Optimisations sans changement de comportement — APPLIQUÉES

| Fichier | Modification |
|---|---|
| `GLOSSARY.md` *(nouveau)* | Sens unique de chaque terme ; distinction statut d'étape / statut de catégorie ; taxonomie des 5 formes d'arrêt ; désambiguïsation des termes surchargés ; clause d'indépendance vis-à-vis du fournisseur d'IA. |
| `SYSTEM-MAP.md` *(nouveau)* | Carte de tous les documents : rôle, lecteur, auteur, autorité N0→N4, dépendances, modifiable ou verrouillé ; hiérarchie de lecture en 4 niveaux. |
| `SYSTEM-AUDIT-REPORT.md` *(nouveau)* | Ce rapport. |
| `TOOLS/validate_system.py` *(nouveau)* | 11 contrôles de cohérence : comptes, prompts, graphe, matrice, ordre de lecture, états, index, empreintes prompts, empreintes système, références de chemins, configuration. |
| `TOOLS/state_index.py` *(nouveau)* | Régénère `STATE.json` depuis les états par catégorie. Supprime la seconde source de vérité (C-05). |
| `COMMON-RULES.md` | Priorité documentaire en liste ordonnée + règles de départage ; `TO_DEFINE` défini ; renvois vers `GLOSSARY`, `SYSTEM-MAP`, `DEPLOYMENT-CONSTRAINTS` ; interdiction de supposer une capacité, une commande ou un test. |
| `WORKFLOW-RULES.md` | Titre « Statuts de catégorie » ; `TERMINÉ` précisé ; règle d'écriture de `VALIDÉ` par IA4 ; inventaire d'état complété (`APPLICABILITY.md`, `CONFIG.json`) ; hiérarchie `state/*.json` → projections ; ordre de reprise. |
| `NEXT-PROMPT-RULES.md` | Séquence de fin d'étape incluant `state_index.py` ; formulation indépendante de l'éditeur ; `TO_DEFINE` ne satisfait pas une dépendance ; causes de `NONE` énumérées. |
| `TEMPLATES/STAGES/1..4` | Bloc « LECTURE » (hiérarchie, arrêt anticipé, interdiction de scan) ; rappel du statut d'étape propre à chaque IA ; rappel des contraintes de déploiement pour IA3/IA4. **Aucun champ ni valeur du format de sortie n'a été modifié.** |
| `MANIFEST-MISE-EN-PLACE-UTILISATION.md` | Chemin `01-STACK` corrigé ; séquence de fin d'étape à 6 points ; outils listés ; statuts précisés ; section 14 bis sur l'hébergement et les médias ; renvois d'index. |
| `README.md` | Devient l'index d'entrée : tableau « par où entrer selon le besoin », outils, contraintes d'hébergement. |
| `STRUCTURAL-VALIDATION.md`, `FUNCTIONAL-VALIDATION.md` | Bandeau « rapport de build, non normatif » + renvoi vers le validateur exécutable. |
| `TEMPLATES/CONFIG-TEMPLATE.json`, `.md-ai-system/CONFIG.json` | Bloc `deployment` ajouté. Les clés existantes sont inchangées. |
| `MANIFEST.json` | `file_hashes` mis à jour pour les fichiers modifiés, entrées ajoutées pour les nouveaux fichiers, champs `revision` / `revision_date_utc`. `version`, `build_id`, `builder_sha256`, catégories, priorités, gates, profils : inchangés. |

Ajout hors périmètre d'optimisation, demandé explicitement :
`DEPLOYMENT-CONSTRAINTS.md` (hébergement Hostinger, interdiction des fournisseurs
externes, médias auto-hébergés) — voir §6, CH-00.

Les changements de comportement du §6 ont ensuite été **validés et appliqués**, à
l'exception de CH-07.

Ce qui n'a **pas** été touché : les 216 prompts, `MANIFEST.json` (structure),
`DEPENDENCY-GRAPH.json`, `EXECUTION-MATRIX.md`, `READING-ORDER.md`, `ORDER.md`,
`SNAPSHOTS.json`, `POLICY-PROFILES.md`, `PROJECT-PROFILES.md`,
`SOURCE-OF-TRUTH-RULES.md`, `TEMPLATES/GIT-INJECTION-TEMPLATE.md`,
`TOOLS/next_prompt.py`, `TOOLS/state_overview.py`, `TESTS/`, les états JSON.

## 6. Optimisations qui MODIFIENT le comportement

**CHANGEMENT DE COMPORTEMENT — validés et appliqués**, sauf CH-07.
Chaque élément reste indépendant et réversible.

### CH-00 — contraintes d'hébergement et de médias *(déjà appliqué, sur ta demande)*
Ajoute une contrainte réelle : l'IA doit refuser tout fournisseur externe quand
`external_services_policy = "deny"`, et refuser de supposer une capacité
d'hébergement. Signalé ici parce que c'est un changement de comportement assumé,
demandé explicitement. Réversible en passant la politique à `allow_listed`.

### CH-01 — un refus d'IA2 ne doit pas mener à IA3 *(gravité A)* *(appliqué)*
Aujourd'hui, `status = REFUSÉ` après IA2 fait proposer IA3 (§7, S3).
Correction dans `TOOLS/next_prompt.py`, fonction `next_stage_for` :

```python
    if status in ("REFUSÉ",):
        return STAGES[0]          # avant le calcul par étape
```

Effet : un refus repart toujours en IA1, mode `CORRECTION`.
Rien d'autre ne change. C'est la correction la plus importante du lot.

### CH-02 — une catégorie BLOQUÉE ne doit pas avancer *(gravité A)* *(appliqué)*
Aujourd'hui, `BLOQUÉ` après IA3 propose IA4, et une catégorie bloquée capte la
priorité au lieu de laisser passer une branche indépendante (§7, S4 et S9).

```python
    if status == "BLOQUÉ":
        return None               # comme EN_ATTENTE_DE_DÉCISION
```

Effet : le résolveur passe à la branche exécutable suivante, conformément à
« une catégorie REFUSÉE/BLOQUÉE bloque uniquement ses descendants réels ».
Contrepartie à valider : il faudra lever explicitement le blocage
(`status` remis à `null` ou `À_RÉÉVALUER`) pour reprendre la catégorie.

### CH-02b — `TO_DEFINE` doit bloquer les gates globaux *(gravité A)* *(appliqué)*
`gate_ready` n'examine que les catégories `ACTIVE` : `52` et `53` peuvent passer
avec 50 catégories non décidées (§7, S11).

```python
        if other.get("applicability") == "TO_DEFINE":
            return False
        if other.get("applicability") == "ACTIVE" and other.get("status") != "VALIDÉ":
            return False
```

Effet : impossible de verrouiller la SOURCE OF TRUTH ou de clôturer tant qu'une
applicabilité n'a pas été décidée. C'est ce que dit déjà `WORKFLOW-RULES.md`.

### CH-02c — émettre `TERMINÉ` *(appliqué)*
Quand toutes les catégories `ACTIVE` sont `VALIDÉ`, que rien n'est `TO_DEFINE` et
que `53-FINAL-CLOSURE` est validée, `next_prompt.py` renvoie `NONE` avec la raison
« projet TERMINÉ » au lieu d'une raison générique.

### CH-03 — mémoriser l'état Git du début de cycle *(appliqué)*
Ajouter à `current_cycle` :

```json
"git": { "head_at_start": null, "remote_sha_at_start": null, "checked_at": null }
```

Effet : la comparaison du SHA distant avant push survit à une interruption.
Aujourd'hui l'information n'existe que dans la réponse de l'IA.
Impact : `schema_version` des états à passer à `2.1`.

### CH-04 — schéma de `AUDIT.jsonl` *(appliqué)*
Une ligne JSON par transition, champs obligatoires :
`ts`, `category`, `stage`, `mode`, `from_status`, `to_status`, `actor`,
`commit`, `summary`.
Effet : l'audit devient exploitable et la reprise devient déterministe.
Aujourd'hui le fichier est vide et sans format.

### CH-05 — emplacement des documents produits *(appliqué)*
Fixer une règle unique, par exemple : les documents de catégorie sont créés dans
`docs/` du projet cible s'il existe, sinon à la racine du projet cible ;
l'emplacement retenu est enregistré une fois comme décision verrouillée.
Effet : deux IA successives cessent de créer `MEDIA-MANIFEST.md` à deux endroits.

### CH-06 — séparer les empreintes système et runtime *(appliqué)*
Dans `MANIFEST.json`, scinder `file_hashes` en `file_hashes` (fichiers système
immuables) et `runtime_files` (liste sans empreinte, pour `.md-ai-system/**`).
Effet : l'intégrité devient vérifiable sans exception codée dans l'outil.

### CH-07 — alléger les lectures obligatoires d'IA1 et IA2 *(NON appliqué)*
IA1 et IA2 ne modifient rien mais lisent `TEMPLATES/GIT-INJECTION-TEMPLATE.md` à
chaque étape. Le retirer de leurs lectures obligatoires (en le gardant pour IA3 et
IA4, et en conservant pour IA1/IA2 le contrôle « working tree non clean : STOP »)
économise environ 15 % du contexte d'entrée sur la moitié des étapes.
**Non appliqué.** Ce n'est pas une incohérence mais le retrait d'un contrôle : cela
touche 108 prompts, modifie leurs empreintes `SNAPSHOTS.json` et supprime une
lecture que tu as peut-être imposée volontairement. Il faut une décision explicite
« applique CH-07 » pour le faire.

### CH-08 — schéma de `DECISIONS.json` *(appliqué)*
Aligner les entrées sur `SOURCE-OF-TRUTH-RULES.md` :
`id`, `decision`, `scope`, `state`, `tests`, `validation_commit`,
`known_limitations`, `locked_by`, `locked_at`.

## 7. Passe 7 — scénarios simulés

Simulation réelle sur une copie du système, résolveur `next_prompt.py` exécuté à
chaque fois.

| # | Scénario | Résultat | Verdict |
|---|---|---|---|
| S1 | Nouveau projet | `00-START/1-IA1-ANALYSE` | conforme |
| S2 | IA1 terminée | `00-START/2-IA2-VERIFICATION` | conforme |
| S3 | IA2 refuse | `00-START/1-IA1-ANALYSE` (CORRECTION) | corrigé — CH-01 |
| S4 | IA3 bloquée | `NONE` + cause « blocage réel à lever (00-START) » | corrigé — CH-02 |
| S5 | Test échoué, IA4 refuse | `00-START/1-IA1-ANALYSE` | conforme |
| S6 | Revalidation autorisée par IA4 | `00-START/1-IA1-ANALYSE` | conforme |
| S6b | Delta pertinent sans autorisation IA4 | catégorie suivante, pas de relance | conforme |
| S7 | Décision humaine en attente | `NONE` + cause « décision humaine en attente » | conforme |
| S8 | Interruption puis reprise | état relu depuis les JSON, `current_cycle.git` préservé | conforme |
| S9 | Catégorie bloquée + branche indépendante | `11-MARKETING-BRAND-DIFFERENTIATION/1-IA1-ANALYSE` | corrigé — CH-02 |
| S10 | Dépendance `N/A` | dépendance considérée satisfaite | conforme |
| S11 | Gate `52` avec 50 catégories `TO_DEFINE` | `NONE` + cause « applicabilité TO_DEFINE à décider » | corrigé — CH-02b |
| S12 | Toutes catégories validées | `NONE` + « Projet TERMINÉ » | corrigé — CH-02c |
| S12b | Toutes catégories `N/A` sauf `00-START` validée | `NONE` + « Projet TERMINÉ » | conforme |
| S13 | Deux IA différentes, sans chat commun | reprise depuis `state/*.json`, `STATE.json`, `AUDIT.jsonl` | conforme |
| S14 | Changement de stack en cours de projet | `À_RÉÉVALUER` + delta, `last_validation` préservée | conforme |

Les quatre défauts étaient dans le résolveur, pas dans les Markdown. Le résolveur
applique désormais la règle que les Markdown énonçaient déjà. Simulation rejouée
après correction : aucun écart restant.

## 8. Plan de modification, fichier par fichier

Statut : **[F]** fait, **[V]** en attente de ta validation.

| Fichier | Action | Statut |
|---|---|---|
| `GLOSSARY.md` | Créer : vocabulaire unique, statuts, taxonomie des arrêts | [F] |
| `SYSTEM-MAP.md` | Créer : carte + hiérarchie de lecture | [F] |
| `SYSTEM-AUDIT-REPORT.md` | Créer : ce rapport | [F] |
| `DEPLOYMENT-CONSTRAINTS.md` | Créer : hébergement, services externes, médias | [F] |
| `TOOLS/validate_system.py` | Créer : 11 contrôles de cohérence | [F] |
| `TOOLS/state_index.py` | Créer : régénération de `STATE.json` | [F] |
| `COMMON-RULES.md` | Priorité ordonnée, `TO_DEFINE`, renvois | [F] |
| `WORKFLOW-RULES.md` | Statuts précisés, inventaire d'état, reprise | [F] |
| `NEXT-PROMPT-RULES.md` | Séquence, neutralité fournisseur, `TO_DEFINE`, causes de `NONE` | [F] |
| `TEMPLATES/STAGES/1..4` | Bloc LECTURE + rappel de statut d'étape | [F] |
| `MANIFEST-MISE-EN-PLACE-UTILISATION.md` | Chemin corrigé, outils, statuts, §14 bis | [F] |
| `README.md` | Index d'entrée | [F] |
| `STRUCTURAL-VALIDATION.md`, `FUNCTIONAL-VALIDATION.md` | Bandeau non normatif | [F] |
| `CONFIG` (template + projet) | Bloc `deployment` | [F] |
| `MANIFEST.json` | Empreintes + `revision` | [F] |
| `TOOLS/next_prompt.py` | CH-01, CH-02, CH-02b, CH-02c | [F] |
| `.md-ai-system/state/*.json` + `WORKFLOW-RULES.md` | CH-03 (bloc `git`), `schema_version` 2.1 | [F] |
| `WORKFLOW-RULES.md` + `TOOLS/audit_append.py` | CH-04 (schéma `AUDIT.jsonl`) | [F] |
| `COMMON-RULES.md` | CH-05 (emplacement des documents produits) | [F] |
| `MANIFEST.json` + validateur | CH-06 (séparation des empreintes) | [F] |
| 108 prompts IA1/IA2 | CH-07 (allègement des lectures) | [V] — seul point restant |
| `SOURCE-OF-TRUTH-RULES.md` | CH-08 (schéma `DECISIONS.json`) | [F] |

## 9. Compatibilité V5.1

Inchangés : noms et nombre de catégories, chemins des prompts, contenu des 216
prompts, noms des étapes, catégories/priorités/dépendances/gates/profils du
manifeste, `DEPENDENCY-GRAPH.json`, `EXECUTION-MATRIX.md`, `READING-ORDER.md`,
vocabulaire des statuts, applicabilités, modes, format de sortie des IA,
protocole `NEXT_PROMPT_*`, noms et chemins des scripts existants.

Ajouté : 4 documents, 3 outils, 1 bloc `deployment` dans la configuration,
1 bloc `git` dans `current_cycle`, `runtime_files` dans le manifeste,
`decision_fields` dans le registre des décisions.

Migration d'un projet déjà commencé sous la V5.1 d'origine — deux points :
1. `schema_version` passe de `2.0` à `2.1` dans les JSON ;
2. chaque `state/<CATEGORY>.json` reçoit
   `current_cycle.git = {head_at_start, remote_sha_at_start, checked_at}` à `null`.

Aucun champ n'est supprimé ni renommé, aucune valeur existante n'est perdue.
`python TOOLS/validate_system.py` signale précisément ce qui manque.

Changements de comportement effectifs, à connaître :
- une catégorie `BLOQUÉ` ne propose plus d'étape : sa reprise demande une levée
  explicite (`status` remis à `null` ou `À_RÉÉVALUER`) ;
- un refus repart toujours d'IA1 ;
- `52` et `53` ne passent plus tant qu'une applicabilité reste `TO_DEFINE` ;
- l'IA doit refuser tout fournisseur externe sous politique `deny`.

---

## 10. Second tour — double contrôle, automatisation, prototype

Trois manques apparus à l'usage, corrigés après validation.

| # | Constat | Gravité | Traitement |
|---|---|---|---|
| C-22 | Rien n'imposait que la vérification soit faite par une **autre IA**. La même IA pouvait tenir IA1 et IA2, ce qui annule la vérification indépendante — le cœur du système. | A | Corrigé : `AI-ROLES-RULES.md`, bloc `ai_roles`, refus à l'enregistrement, contrôle 15 du validateur |
| C-23 | Le profil `POC` disait « checks essentiels » sans dire lesquels, et rien ne permettait de repasser proprement d'un prototype à un projet réel : la dette de prototype était invisible. | A | Corrigé : `POLICY-PROFILES.md` réécrit, applicabilité liée au profil (`--policy-scoped`), commande `promote` |
| C-24 | La fin d'étape demandait 5 opérations manuelles sur des JSON. Chaque oubli créait une incohérence, et l'écriture manuelle d'un statut est une porte ouverte à l'erreur. | B | Corrigé : `TOOLS/mdai.py finish-stage` fait tout en une commande, avec vérification des verdicts autorisés par étape |
| C-25 | Le guide laissait croire que le projet ne contenait que des `.md`. | C | Corrigé : `MANIFEST-MISE-EN-PLACE-UTILISATION.md` §1, `README.md` |

### Ce qui a été ajouté

- **`AI-ROLES-RULES.md`** — IA2 ≠ IA1, IA4 ≠ IA3 ; le fournisseur d'IA est
  enregistré par étape dans `current_cycle.iaN.provider` et dans l'audit ; le mode
  `degraded` existe mais exige une décision verrouillée.
- **`TOOLS/mdai.py`** — commande unique : `init`, `check`, `status`, `next`,
  `git-snapshot`, `finish-stage`, `set`, `promote`, `explain`, `unblock`.
- **Profil prototype** — ce qui reste obligatoire en POC, ce qui peut être différé,
  et la promotion `promote --to STAGING|PRODUCTION` qui rouvre les catégories
  différées et remet à revalider ce qui l'avait été au niveau POC, sans effacer
  aucune validation.
- **`NEXT_PROMPT_AI`** — quatrième ligne de sortie du résolveur : quelle IA doit
  faire l'étape suivante. Additive : les trois lignes existantes sont inchangées.
- `schema_version` `2.1` → `2.2` ; `applicability_scope` ajouté aux états ;
  `provider` ajouté au journal d'audit ; `ai_roles` ajouté à la configuration.

### Garde-fous vérifiés

`mdai finish-stage` refuse : un verdict impossible pour l'étape (`VALIDÉ` pour
IA1, par exemple), une étape sur une catégorie non `ACTIVE`, une vérification par
l'IA qui a produit, une vérification sans étape produite enregistrée, un `VALIDÉ`
d'IA4 sans commit hors profil POC. `--force` permet de changer d'IA déclarée,
**jamais** de contourner l'indépendance.

## 11. Optimisations recommandées pour un débutant — non appliquées

Elles ne corrigent aucune incohérence : ce sont des ajouts de confort. À décider.

| # | Proposition | Apport | Coût |
|---|---|---|---|
| N-01 | `mdai doctor` : diagnostic en français qui liste, dans l'ordre, les 3 prochaines actions concrètes | supprime le « je fais quoi maintenant ? » | faible |
| N-02 | Journal lisible `HISTORIQUE.md` généré depuis `AUDIT.jsonl` | l'utilisateur voit ce qui s'est passé sans lire du JSON | faible |
| N-03 | `mdai finish-stage --dry-run` : montre l'effet sur l'état sans écrire | rassure avant une action | faible |
| N-04 | Rappel automatique du `git-snapshot` manquant avant toute étape IA3 | empêche un push sans contrôle de concurrence | faible |
| N-05 | Modèle de projet minimal (`docs/` + SOURCE OF TRUTH vide) créé par `mdai init` | évite le démarrage sur une page blanche | moyen |
| N-06 | Budget de fichiers par catégorie activé par défaut en POC | empêche un prototype de déraper en refonte | moyen |
| N-07 | `mdai report` : synthèse PDF/HTML de l'état du projet pour un tiers | utile pour montrer l'avancement | moyen |
| N-08 | Vérification automatique des médias (poids, dimensions, ALT, droits) contre `MEDIA-MANIFEST.md` | rend le contrôle média mesurable, pas déclaratif | élevé |
