# WORKFLOW / DAG / REVALIDATION / STATE

Définitions et correspondance statut d'étape ↔ statut de catégorie : `GLOSSARY.md`.

## Statuts de catégorie
- VALIDÉ : tous les contrôles exigés passent et les preuves obligatoires au niveau du contrôle existent.
- REFUSÉ : au moins un écart validé subsiste ou une preuve obligatoire manque. Le cycle repart d'IA1 en mode CORRECTION, quelle que soit l'étape refusante.
- BLOQUÉ : l'exécution ne peut pas continuer pour cette catégorie tant qu'un blocage réel subsiste. Aucune étape suivante n'est proposée ; les branches indépendantes continuent. La levée du blocage est explicite : `status` remis à `null` (reprise du cycle) ou à `À_RÉÉVALUER`.
- EN_ATTENTE_DE_DÉCISION : une décision humaine/documentaire indispensable manque.
- À_RÉÉVALUER : un changement pertinent impose de refaire le cycle sans effacer la dernière validation.
- EN_REVALIDATION : IA1→IA4 est en cours sur un delta pertinent.
- TERMINÉ : toutes les catégories ACTIVE sont VALIDÉES, aucune catégorie ne reste TO_DEFINE, aucune décision n'est en attente, tests/build/Git sont conformes. TERMINÉ décrit le projet, pas une catégorie isolée.
- `N/A` n'est pas un statut : c'est une applicabilité.
- `VALIDÉ` au niveau de la catégorie n'est écrit que par IA4. Les verdicts d'étape `ANALYSE` (IA1), `VALIDÉ` (IA2) et `EXÉCUTÉ` (IA3) restent dans `current_cycle`.

## DAG
- Les dépendances sont un graphe explicite, pas une chaîne implicite.
- Le builder refuse tout cycle.
- Le statut d'une catégorie est indépendant du statut des catégories non dépendantes.
- Une catégorie REFUSÉE/BLOQUÉE bloque uniquement ses descendants réels.
- Si une dépendance amont passe de REFUSÉ/BLOQUÉ à VALIDÉ, les descendants concernés redeviennent évaluables ; s'ils ont déjà une validation, utiliser À_RÉÉVALUER.
- L'ordre de lecture, la priorité d'exécution et les dépendances sont trois notions distinctes.

## Réitérabilité / delta
- Une validation existante n'est jamais effacée au démarrage d'un nouveau cycle.
- Conserver `last_validation` séparément de `current_cycle`.
- Détecter le delta depuis le commit de dernière validation lorsqu'un nouveau commit pertinent existe.
- Relancer IA1→IA4 seulement pour un changement pertinent, avec autorisation IA4 enregistrée pour la revalidation.
- Modes : NEW_WORK, REVALIDATION, CORRECTION.
- REVALIDATION = contrôle d'un delta depuis une validation existante.
- NEW_WORK = nouveau périmètre sans validation précédente.
- CORRECTION = reprise après refus/échec sur le même périmètre.

## État persistant
- `.md-ai-system/state/<CATEGORY>.json` : état machine atomique par catégorie.
- `.md-ai-system/STATE.json` : index global machine-readable.
- `.md-ai-system/STATE-OVERVIEW.md` : vue humaine générée depuis les JSON à chaque transition.
- `.md-ai-system/DECISIONS.json` : registre global des décisions verrouillées.
- `.md-ai-system/AUDIT.jsonl` : journal d'audit append-only des transitions importantes (format §Audit).
- `.md-ai-system/APPLICABILITY.md` : matrice d'applicabilité justifiée, produite par `01-PROJECT-PROFILE-APPLICABILITY`.
- `.md-ai-system/CONFIG.json` : POLICY_PROFILE, PROJECT_PROFILES et contraintes de déploiement.
- `state/<CATEGORY>.json` fait foi ; `STATE.json` et `STATE-OVERVIEW.md` en sont des projections régénérées.
- Ne pas créer d'historique séparé des décisions ou de leurs changements.
- Ne pas imposer une traçabilité exigence → code → test → commit.

## Reprise
- Après interruption : reprendre depuis le dernier état persistant valide, sans dépendre d'un historique de conversation.
- Ordre de reprise : `state/<CATEGORY>.json` → `STATE.json` → `AUDIT.jsonl` seulement si l'état paraît incohérent.
- Après échec IA3/tests/push : conserver l'échec et reprendre seulement après résolution.

## Double contrôle
- L'étape de contrôle est réalisée par une IA différente de l'étape produite :
  IA2 ≠ IA1, IA4 ≠ IA3. Règles complètes : `AI-ROLES-RULES.md`.
- Chaque étape enregistre dans `current_cycle.iaN` :
  `provider`, `verdict`, `ts`, `summary`.
- Une catégorie validée sans trace de deux IA distinctes est un écart.

## État Git du cycle
- `current_cycle.git` conserve l'état Git constaté au début du cycle :
  `head_at_start`, `remote_sha_at_start`, `checked_at`.
- Ces valeurs sont écrites lors de la vérification Git initiale de
  `TEMPLATES/GIT-INJECTION-TEMPLATE.md` et servent au contrôle de concurrence avant push.
- Elles survivent à une interruption : après reprise, la comparaison du SHA distant
  reste possible sans relire la conversation précédente.
- Elles sont réinitialisées à `null` au démarrage d'un nouveau cycle.

## Audit
- Une transition importante = une ligne JSON ajoutée à `.md-ai-system/AUDIT.jsonl`.
- Le fichier est append-only : aucune ligne n'est modifiée ni supprimée.
- Champs obligatoires, dans cet ordre :
  `ts`, `category`, `stage`, `mode`, `actor`, `provider`, `from_status`, `to_status`, `commit`, `summary`.
- `ts` est UTC au format `YYYY-MM-DDTHH:MM:SSZ`. `actor` vaut `IA1`, `IA2`, `IA3`,
  `IA4`, `HUMAIN` ou `OUTIL`. `commit` peut être `null`. `summary` est non vide.
- `provider` nomme l'IA qui a réalisé l'étape ; `null` pour une action humaine ou outil.
- Écriture par `python TOOLS/mdai.py finish-stage` (ou `TOOLS/audit_append.py` en direct), qui valide les valeurs avant d'écrire.
- Transitions à journaliser : fin d'étape, changement de statut, changement
  d'applicabilité, décision verrouillée, blocage, levée de blocage, revalidation autorisée.

## Risque
- Le risque porte sur le changement courant, pas sur une catégorie entière.
- Niveaux : FAIBLE / MOYEN / ÉLEVÉ / CRITIQUE.
- Contrôle renforcé pour migrations destructives, auth, paiements, secrets, production et opérations irréversibles.
- Les budgets de fichiers modifiés sont configurables par catégorie ; aucune limite universelle arbitraire.
