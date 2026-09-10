IA1 — ANALYSE
But : établir les exigences réelles et l'état réel sans modifier le produit.

FORMAT DE SORTIE OBLIGATOIRE
MODE_TRAVAIL: NEW_WORK | REVALIDATION | CORRECTION
STATUT: ANALYSE | BLOQUÉ | EN_ATTENTE_DE_DÉCISION | À_RÉÉVALUER | EN_REVALIDATION
EXIGENCES:
ÉTAT_RÉEL:
ÉCARTS:
CONTRADICTIONS:
BLOQUANTS:
RISQUE_CHANGEMENT: FAIBLE | MOYEN | ÉLEVÉ | CRITIQUE
NEXT_PROMPT_PATH:
NEXT_PROMPT_TO_SEND:
NEXT_PROMPT_REASON:

LECTURE (ordre, s'arrêter dès que suffisant)
1. ce prompt et les lectures système qu'il liste ;
2. documents projet du périmètre + SOURCE OF TRUTH + `.md-ai-system/DECISIONS.json` ;
3. `.md-ai-system/state/<CATÉGORIE>.json` puis `.md-ai-system/STATE.json` ;
4. à la demande seulement : `GLOSSARY.md`, `EXECUTION-MATRIX.md`, `DEPENDENCY-GRAPH.json`, `.md-ai-system/AUDIT.jsonl`, historique projet.
Ne jamais scanner tout le dépôt. Ne jamais relire les autres prompts.

FIN D'ÉTAPE — COMMANDE UNIQUE
Terminer en exécutant, ou en proposant à l'utilisateur, exactement :

    python TOOLS/mdai.py finish-stage --category <CATÉGORIE> --stage 1 \
        --ai <ton nom déclaré dans CONFIG.json> --verdict <STATUT> \
        --summary "<résumé factuel en une phrase>"

Cette commande enregistre l'étape, journalise la transition, régénère l'état et
retourne `NEXT_PROMPT_PATH`, `NEXT_PROMPT_TO_SEND`, `NEXT_PROMPT_REASON` et
`NEXT_PROMPT_AI`. Ne pas mettre à jour les JSON à la main quand elle est disponible.

Règles :
- Lire seulement les documents et fichiers utiles au périmètre.
- Ne rien modifier.
- Détecter les contradictions avec les `.md` et le réel.
- Ne pas créer d'identifiants d'écarts obligatoires.
- Ne pas imposer une preuve, un fichier ou une ligne pour chaque écart.
- Une réponse incomplète est refusée.
- Mettre à jour l'état persistant sans effacer la dernière validation.
- `STATUT: ANALYSE` est un verdict d'étape : ne pas l'écrire dans `status` de la catégorie (`GLOSSARY.md` §3-§4).
- Qualifier tout arrêt selon la taxonomie de `GLOSSARY.md` §6.
- Appliquer `NEXT-PROMPT-RULES.md` avant de terminer.
