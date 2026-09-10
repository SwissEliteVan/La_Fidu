# POLICY PROFILES

`PROJECT_PROFILE` décrit ce qu'est le projet.
`POLICY_PROFILE` décrit le niveau de rigueur opérationnelle.
Ils sont indépendants.

## PRODUCTION
- Git strict selon `TEMPLATES/GIT-INJECTION-TEMPLATE.md`.
- Validations renforcées.
- Tous les checks applicables.
- Contrôles de risque renforcés.
- Déploiement/rollback applicables contrôlés.

## STAGING
- Git strict selon `TEMPLATES/GIT-INJECTION-TEMPLATE.md`.
- Validations normales.
- Checks applicables au staging.
- Les contrôles exclusivement production peuvent rester explicitement en attente de la phase production.

## POC — PROTOTYPE
Objectif : valider une idée vite, **sans créer de dette invisible**.
Un POC n'est pas un projet bâclé : c'est un projet dont le périmètre contrôlé est
volontairement réduit, et dont chaque réduction est écrite.

### Ce qui reste obligatoire, sans exception
- Git réduit en verbosité, mais les protections dangereuses restent obligatoires.
- Working tree clean obligatoire.
- Contrôle distant conservé.
- Détection des modifications humaines conservée.
- Staging explicite conservé.
- Interdiction des opérations Git destructives conservée.
- Protections secrets, destruction de données et opérations irréversibles conservées.
- Double contrôle par deux IA différentes (`AI-ROLES-RULES.md`).
- Contraintes d'hébergement et de services externes (`DEPLOYMENT-CONSTRAINTS.md`).
- Tests réels des chemins critiques du prototype ; aucun test annoncé sans être exécuté.
- SOURCE OF TRUTH tenue à jour pour les décisions réellement prises.
- Applicabilité justifiée : aucune catégorie n'est ignorée en silence.

### Ce qui peut être différé
Les catégories qui ne servent pas à démontrer l'idée peuvent être enregistrées
`N/A` **liées au profil courant**, avec justification :

```text
python TOOLS/mdai.py set --category 39-VISUAL-REGRESSION --applicability N/A     --reason "hors périmètre du prototype" --policy-scoped
```

`--policy-scoped` inscrit que ce `N/A` ne vaut **que pour le POC**. C'est la dette
de prototype, rendue visible et récupérable.

Sont typiquement différables en POC, si le prototype n'en dépend pas :
régression visuelle, cross-browser, SEO opérationnel, release/changelog,
gestion des incidents, parité d'environnements, support client, attribution.

Ne sont jamais différables, même en POC : sécurité, secrets, sauvegarde des
données réelles, consentement si des données personnelles sont collectées,
licences des médias utilisés.

### Passage du prototype au projet réel
```text
python TOOLS/mdai.py promote --to STAGING      # ou PRODUCTION
```

La promotion :
- remet en `TO_DEFINE` toutes les catégories mises `N/A` au titre du POC ;
- remet en `À_RÉÉVALUER` toutes les catégories validées sous POC, avec un delta
  pertinent et l'autorisation de revalidation ;
- **conserve chaque dernière validation** : rien n'est effacé, tout est recontrôlé
  au niveau de rigueur du nouveau profil ;
- journalise la promotion dans l'audit.

Un prototype promu n'est donc jamais confondu avec un projet validé en production.

Aucun POLICY_PROFILE n'est deviné. Il doit être configuré explicitement dans `.md-ai-system/CONFIG.json`.
