# SOURCE OF TRUTH RULES

La SOURCE OF TRUTH est la référence documentaire principale du projet.

Structure minimale par décision verrouillée :
- décision ;
- périmètre ;
- état ;
- tests associés ;
- commit de validation si applicable ;
- limitations connues.

Ne pas imposer dans cette structure :
- version/date de décision ;
- liste des fichiers concernés ;
- dépendances entre décisions.

Règles :
- Vérifier automatiquement la cohérence code ↔ SOURCE OF TRUTH lorsqu'une catégorie est contrôlée.
- Détecter les modifications non documentées.
- Toute modification d'une décision verrouillée suit : règle actuelle → justification → validation → modification → tests → mise à jour `.md` → IA1→IA4 → commit/push.
- Les fichiers critiques explicitement déclarés peuvent être protégés par hash.

## Registre machine des décisions

`.md-ai-system/DECISIONS.json` est la forme machine des décisions verrouillées.
Chaque entrée de `locked_decisions` porte exactement ces champs :

| Champ | Contenu |
|---|---|
| `id` | identifiant stable, unique, non réutilisé |
| `decision` | la décision, en une phrase non ambiguë |
| `scope` | périmètre couvert |
| `state` | `VALIDÉ`, `REFUSÉ`, `BLOQUÉ` ou `EN_ATTENTE_DE_DÉCISION` |
| `tests` | tests associés réellement exécutés |
| `validation_commit` | commit de validation, ou `null` si non applicable |
| `known_limitations` | limitations connues |
| `locked_by` | `IA4` ou `HUMAIN` |
| `locked_at` | horodatage UTC `YYYY-MM-DDTHH:MM:SSZ` |

Ces champs sont la projection machine de la structure minimale ci-dessus : ils
n'ajoutent aucune exigence documentaire (ni version, ni liste de fichiers, ni
dépendances entre décisions). Le registre et la SOURCE OF TRUTH disent la même
chose ; une divergence entre les deux est une contradiction à signaler.
