# MD AI SYSTEM V5.1

Système piloté par `.md` pour projets simples à très complexes.
Quatre IA se relaient sur chaque catégorie : **IA1 analyse**, **IA2 vérifie de
façon indépendante**, **IA3 exécute**, **IA4 contrôle**. IA2 et IA4 sont tenues
par une **autre IA** que IA1 et IA3 : une IA ne se vérifie pas elle-même.
L'état vit dans des fichiers, pas dans une conversation : une nouvelle IA reprend
le travail sans le chat précédent.

Le système pilote avec des `.md`, mais le projet produit est réel : code, médias,
configuration. Les `.md` sont les règles et la mémoire.

- 53 catégories opérationnelles + `00-START` = 54 entrées de workflow.
- 216 prompts IA1→IA4 disponibles.
- Les catégories N/A n'exécutent pas IA1→IA4.
- DAG explicite avec détection de cycles.
- Ordre de lecture distinct de la priorité d'exécution.
- Révalidation par delta sans effacer la dernière validation.
- PROJECT_PROFILE : website / saas / ecommerce / api_backend / internal_app.
- POLICY_PROFILE : PRODUCTION / STAGING / POC.
- Double contrôle imposé et vérifiable : IA2 ≠ IA1, IA4 ≠ IA3.
- Contraintes d'hébergement, de déploiement et de médias paramétrées, pas devinées.
- Profil prototype avec dette explicite et promotion contrôlée vers la production.
- État : JSON par catégorie + index global + vue Markdown générée.
- Templates communs centralisés pour éviter la duplication physique.
- L'IA propose le prochain prompt logique et le lit directement dans le workspace.

## Démarrage
1. Ouvrir `PROMPTS/00-START/1-IA1-ANALYSE.md`.
2. L'IA lit elle-même les templates référencés dans le workspace.
3. Après chaque transition, mettre à jour les JSON puis exécuter
   `python TOOLS/state_index.py` et `python TOOLS/state_overview.py`.
4. Exécuter `python TOOLS/next_prompt.py` pour obtenir le prochain prompt à envoyer.
5. Ne pas suivre les numéros comme une chaîne de dépendances ; utiliser
   `DEPENDENCY-GRAPH.json` et `EXECUTION-MATRIX.md`.

Guide humain complet : `MANIFEST-MISE-EN-PLACE-UTILISATION.md`.

## Par où entrer selon le besoin

| Besoin | Document |
|---|---|
| Installer et utiliser le système | `MANIFEST-MISE-EN-PLACE-UTILISATION.md` |
| Savoir à quoi sert chaque fichier | `SYSTEM-MAP.md` |
| Lever un doute sur un terme ou un statut | `GLOSSARY.md` |
| Règles transverses et priorité documentaire | `COMMON-RULES.md` |
| Statuts, DAG, revalidation, état, reprise | `WORKFLOW-RULES.md` |
| Décisions verrouillées | `SOURCE-OF-TRUTH-RULES.md` |
| Routage vers le prochain prompt | `NEXT-PROMPT-RULES.md` |
| Règles Git | `TEMPLATES/GIT-INJECTION-TEMPLATE.md` |
| Niveau de rigueur | `POLICY-PROFILES.md` |
| Type de projet | `PROJECT-PROFILES.md` |
| Hébergement, déploiement, médias, services externes | `DEPLOYMENT-CONSTRAINTS.md` |
| Double contrôle par deux IA différentes | `AI-ROLES-RULES.md` |
| Ordre de lecture / d'exécution | `READING-ORDER.md` / `EXECUTION-MATRIX.md` |
| Audit du système et optimisations en attente | `SYSTEM-AUDIT-REPORT.md` |

## Policy profile
Configurer `.md-ai-system/CONFIG.json`. Aucun profil de rigueur n'est deviné.

## Hébergement, déploiement et médias
`.md-ai-system/CONFIG.json` porte un bloc `deployment` :
hébergeur cible, politique de services externes (`deny` par défaut), dérogations
explicitement validées, hébergement des médias. Les règles associées sont dans
`DEPLOYMENT-CONSTRAINTS.md`. Aucune capacité d'hébergement n'est supposée : elle
est constatée.

## Outils

Commande unique :

```text
python TOOLS/mdai.py init --policy POC --hosting hostinger --ia1 A --ia2 B --ia3 A --ia4 B
python TOOLS/mdai.py check                 # prérequis + 15 contrôles de cohérence
python TOOLS/mdai.py status                # avancement + prochaine étape
python TOOLS/mdai.py next                  # prochain prompt + IA attendue
python TOOLS/mdai.py git-snapshot --category <CAT>
python TOOLS/mdai.py finish-stage --category <CAT> --stage <1..4> --ai <IA> \
    --verdict <STATUT> --summary "<résumé>" [--commit <sha>]
python TOOLS/mdai.py set --category <CAT> --applicability N/A --reason "..." --policy-scoped
python TOOLS/mdai.py explain --category <CAT>
python TOOLS/mdai.py unblock --category <CAT> --reason "..."
python TOOLS/mdai.py promote --to PRODUCTION
```

`finish-stage` enchaîne à lui seul : contrôle du double contrôle → état → audit →
`STATE.json` → `STATE-OVERVIEW.md` → prochain prompt et IA attendue.

Outils détaillés, toujours disponibles :

```text
python TOOLS/audit_append.py --help
python TOOLS/state_index.py
python TOOLS/state_overview.py
python TOOLS/next_prompt.py
python TOOLS/validate_system.py
python -m unittest discover TESTS
```
