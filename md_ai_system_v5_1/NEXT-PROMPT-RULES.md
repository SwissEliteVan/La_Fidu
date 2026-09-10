# NEXT PROMPT RULES

Objectif : à la fin de chaque IA, proposer le prochain prompt logique à envoyer.

1. Exécuter la commande unique de fin d'étape :

   ```text
   python TOOLS/mdai.py finish-stage --category <CATEGORY> --stage <1..4> \
       --ai <IA ayant réalisé l'étape> --verdict <STATUT> --summary "<résumé>" [--commit <sha>]
   ```

   Elle contrôle le double contrôle, met à jour l'état, journalise la transition,
   régénère `STATE.json` et `STATE-OVERVIEW.md`, puis calcule le prochain prompt.
2. Si cette commande n'est pas disponible, faire la même chose à la main, dans cet ordre :
   état de la catégorie → `TOOLS/audit_append.py` → `TOOLS/state_index.py` →
   `TOOLS/state_overview.py` → `TOOLS/next_prompt.py`.
3. Utiliser exactement le chemin retourné, sans le reconstruire de mémoire.
4. Si l'IA dispose d'un accès direct aux fichiers du projet (workspace VS Code ou environnement équivalent, quel que soit le fournisseur d'IA), elle doit lire elle-même le fichier retourné. Ne jamais demander à l'utilisateur de copier/coller le contenu du prompt. Si elle n'a pas cet accès, elle le déclare explicitement au lieu de reconstituer le prompt de mémoire.
5. Dans la réponse courante, fournir :
   - `NEXT_PROMPT_PATH: <chemin>`
   - `NEXT_PROMPT_TO_SEND: Exécute le prompt <chemin> en le lisant directement dans le workspace VS Code.`
   - `NEXT_PROMPT_REASON: <raison courte>`
   - `NEXT_PROMPT_AI: <IA attendue pour cette étape, ou NON_DÉCLARÉ>`
6. Ne pas exécuter silencieusement l'étape suivante dans la même réponse ; proposer le prompt logique suivant.
7. Si aucun prompt n'est exécutable : `NEXT_PROMPT_PATH: NONE` et expliquer la cause exacte : décision en attente, blocage réel, applicabilité `TO_DEFINE` à décider, aucune branche exécutable, ou clôture.

Sélection :
- Continuer d'abord le cycle courant d'une catégorie déjà engagée si elle est exécutable.
- Sinon choisir la catégorie ACTIVE prête dont les dépendances ACTIVE sont VALIDÉES, selon `execution_priority`.
- Une dépendance N/A est considérée satisfaite pour le graphe.
- Une dépendance `TO_DEFINE` n'est pas satisfaite : elle bloque ses descendants jusqu'à décision d'applicabilité.
- Ignorer les catégories EN_ATTENTE_DE_DÉCISION jusqu'à résolution ; continuer les branches indépendantes si possible.
- Une catégorie VALIDÉE n'est relancée que si son état est À_RÉÉVALUER/EN_REVALIDATION ou si un delta pertinent a été explicitement enregistré et autorisé par IA4.
- Une catégorie REFUSÉE repart d'IA1 en mode CORRECTION, jamais d'IA3.
- Une catégorie BLOQUÉE ou EN_ATTENTE_DE_DÉCISION ne propose aucune étape ; les branches indépendantes continuent. La levée est explicite.
- SOURCE OF TRUTH / VERROUILLAGE et FINAL-CLOSURE appliquent leurs gates globaux du manifest.
- L'étape suivante est annoncée avec l'IA attendue : une étape de contrôle ne doit pas être confiée à l'IA qui a produit (`AI-ROLES-RULES.md`).
