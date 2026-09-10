# COMMON RULES

- Les `.md` pilotent le projet.
- Vocabulaire et statuts : `GLOSSARY.md`. Carte des documents : `SYSTEM-MAP.md`.
## Priorité documentaire (projet cible)

Ordre déterministe, du plus fort au plus faible. Le premier document qui tranche
la question gagne ; on ne descend au rang suivant que si le rang courant est muet.

1. SOURCE OF TRUTH verrouillée ;
2. décision explicitement validée (`.md-ai-system/DECISIONS.json`) ;
3. spécification active ;
4. START / INDEX ;
5. README ;
6. document historique, obsolète ou remplacé, lorsqu'un tel état existe déjà dans le projet.

Précisions :
- une décision du rang 2 non encore reportée dans la SOURCE OF TRUTH reste applicable ;
- si les rangs 1 et 2 se contredisent, c'est un écart à signaler, pas un arbitrage à improviser ;
- deux documents de même rang qui se contredisent constituent une contradiction à signaler ;
- cette priorité arbitre les documents du projet cible. L'autorité des fichiers du
  système est décrite dans `SYSTEM-MAP.md`.

## Règles générales

- Lire uniquement les `.md` utiles à l'étape et les documents qu'ils référencent, selon la hiérarchie de lecture de `SYSTEM-MAP.md` (§7).
- Pas de scan massif initial.
- N'inventer ni exigence, ni contenu, ni preuve, ni dépendance.
- Une décision verrouillée ne peut jamais être changée silencieusement.
- Détecter les contradictions entre `.md`, entre documentation et code, et entre les sorties IA.
- Détecter toute exigence non implémentée et tout changement produit sans exigence documentaire.
- Ne pas créer un mécanisme supplémentaire de résolution des contradictions documentaires : les signaler et appliquer uniquement la priorité documentaire validée.
- Toute activation de catégorie doit être justifiée et enregistrée dans la matrice d'applicabilité.
- `N/A` est une valeur d'applicabilité/reporting, pas un statut de catégorie.
- `TO_DEFINE` est une applicabilité non encore décidée : elle n'autorise aucune exécution et n'équivaut jamais à `N/A`.
- Une catégorie N/A n'exécute pas IA1→IA4.
- Une catégorie ACTIVE exécute IA1→IA4 lors de son premier chantier, sauf blocage ou décision en attente.
- Une catégorie obligatoire ou active ne peut pas être sautée.
- Une dépendance non validée bloque seulement ses descendants réels.
- Contraintes d'hébergement, de déploiement et de médias : `DEPLOYMENT-CONSTRAINTS.md`.
- Double contrôle par deux IA différentes : `AI-ROLES-RULES.md`.
- Emplacement des documents produits : voir la section dédiée ci-dessous.
- Ne jamais supposer une capacité d'hébergement, une commande, un test ou un service : le vérifier réellement.
- Réponse courte, factuelle et opérationnelle.
- Pas de narration.

## Emplacement des documents produits

Les documents créés par les catégories (`MEDIA-MANIFEST.md`, `CTA-MAP.md`,
`COMMERCIAL-STRATEGY.md`, SOURCE OF TRUTH, etc.) appartiennent au projet cible.

Règle unique :
1. si le projet cible possède déjà un dossier `docs/`, ils y sont créés ;
2. sinon, à la racine du projet cible ;
3. l'emplacement retenu est enregistré une seule fois comme décision verrouillée,
   puis n'est plus rediscuté ;
4. ils ne sont jamais créés dans le dossier du système (`md_ai_system_v5_1/`),
   à l'exception de `.md-ai-system/APPLICABILITY.md` qui est un fichier d'état ;
5. un document déjà existant est mis à jour là où il est, jamais dupliqué ailleurs.

Avant de créer un document, chercher s'il existe déjà dans le projet cible.
Deux exemplaires du même document constituent une contradiction à signaler.
