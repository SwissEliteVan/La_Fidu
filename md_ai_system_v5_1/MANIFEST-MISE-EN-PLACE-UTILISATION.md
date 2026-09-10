# MANIFESTE — MISE EN PLACE ET UTILISATION

Guide humain du système. Écrit pour quelqu'un qui ne code pas.
`MANIFEST.json` reste le manifeste machine.

Index des documents : `README.md`. Rôle de chaque fichier : `SYSTEM-MAP.md`.
Vocabulaire et statuts : `GLOSSARY.md`.

---

## 0. En une page

Tu ouvres ton projet dans VS Code. Tu envoies **un message** à l'IA, une seule
fois. Ensuite, à chaque étape, l'IA travaille puis te donne une ligne
`NEXT_PROMPT_TO_SEND`. Tu lui renvoies cette ligne. C'est tout.

L'IA fait le reste : elle lit les fichiers, exécute les commandes, met à jour
l'état, calcule l'étape suivante. Elle ne te demande une décision que lorsque le
système en a réellement besoin.

Ton rôle, en entier :

1. ouvrir le bon dossier dans VS Code ;
2. choisir `POLICY_PROFILE` (PRODUCTION, STAGING ou POC) quand on te le demande ;
3. confirmer l'hébergement quand on te le demande ;
4. **utiliser deux IA différentes** : l'une produit, l'autre vérifie (section 2) ;
5. répondre aux décisions humaines réellement nécessaires ;
6. renvoyer `NEXT_PROMPT_TO_SEND` à l'IA indiquée par `NEXT_PROMPT_AI`.

Tu n'as jamais à ouvrir un prompt, ni à modifier un fichier JSON, ni à taper une
commande Git.

---

## 1. Ce que fait le système

Le travail est découpé en **54 catégories** (stack, architecture, design, médias,
SEO, sécurité, tests, déploiement, clôture…). Chaque catégorie passe par quatre
étapes tenues par quatre IA :

| Étape | Qui | Ce qu'elle fait | Touche au projet |
|---|---|---|---|
| 1 | IA1 | analyse ce qui est demandé et ce qui existe vraiment | non |
| 2 | IA2 | refait le constat de son côté et vérifie IA1 | non |
| 3 | IA3 | exécute, uniquement dans le périmètre autorisé | oui |
| 4 | IA4 | contrôle le résultat réel et valide ou refuse | non |

IA1 et IA2 ne font pas double emploi : IA2 repart des sources sans faire confiance
à IA1. C'est ce qui empêche une erreur d'analyse d'être exécutée.

Tout l'état est écrit dans des fichiers. Conséquence pratique : **tu peux changer
d'IA, fermer VS Code, revenir dans trois semaines** — le travail reprend où il en
était, sans avoir besoin de l'ancienne conversation.

### Ton projet n'est pas fait que de fichiers `.md`

C'est une confusion fréquente. Le système **pilote** avec des `.md`, mais ton
projet contient de vrais fichiers :

| Dans ton projet | Exemples | Qui les écrit |
|---|---|---|
| le produit réel | HTML, CSS, JavaScript, PHP, templates, configuration, base de données | IA3 |
| les médias réels | images, vidéos, poster, icônes, favicons | IA3 |
| les documents de pilotage | SOURCE OF TRUTH, `MEDIA-MANIFEST.md`, `CTA-MAP.md`… | IA1 et IA3 |
| l'état du workflow | `md_ai_system_v5_1/.md-ai-system/*.json` | les outils |

Les `.md` sont les **règles et la mémoire** du projet. Le site, l'application ou
l'API, ce sont des fichiers de code et de médias, produits par IA3 et contrôlés
par IA4.

## 2. Deux IA différentes, obligatoirement

Une IA ne se vérifie pas elle-même. Le système impose donc :

- **IA2 doit être une autre IA qu'IA1** ;
- **IA4 doit être une autre IA qu'IA3**.

Deux IA suffisent. Exemple de répartition :

| Étape | IA |
|---|---|
| IA1 analyse | IA **A** |
| IA2 vérifie | IA **B** |
| IA3 exécute | IA **A** |
| IA4 contrôle | IA **B** |

Tu déclares les deux au démarrage :

```text
python md_ai_system_v5_1/TOOLS/mdai.py init --ia1 claude --ia2 chatgpt --ia3 claude --ia4 chatgpt
```

Ensuite, à chaque étape, le système te dit quelle IA doit travailler
(`NEXT_PROMPT_AI`) et **refuse** d'enregistrer une vérification faite par l'IA qui
a produit. Les noms sont libres : `claude`, `chatgpt`, `deepseek`, `gemini`, `qwen`…

En pratique : tu gardes deux onglets ouverts, un par IA, et tu envoies
`NEXT_PROMPT_TO_SEND` dans l'onglet indiqué.

Règles complètes : `AI-ROLES-RULES.md`.

---

## 3. Prérequis

- VS Code (ou un environnement équivalent où l'IA lit tes fichiers) ;
- Python 3.8 ou plus ;
- Git, avec une branche `main` ;
- une IA ayant accès au workspace, et si possible au terminal.

Tu n'as pas à vérifier ces éléments toi-même : demande-le à l'IA. Si un prérequis
manque, elle doit te le dire clairement et s'arrêter. Elle ne doit jamais
contourner un contrôle en silence.

---

## 4. Où placer le système

Le système vit dans son propre dossier, **à l'intérieur** du dossier de ton projet.

```text
MON-PROJET/                  ← c'est CE dossier que tu ouvres dans VS Code
├── index.html, styles.css, app.js, …   ← ton produit réel
├── assets/  (images, vidéos, icônes)   ← tes médias réels
├── docs/    (SOURCE OF TRUTH, MEDIA-MANIFEST.md, …)
├── README.md                ← le README de TON projet
└── md_ai_system_v5_1/       ← le système
    ├── PROMPTS/
    ├── TEMPLATES/
    ├── TOOLS/
    ├── .md-ai-system/       ← l'état de ton projet
    └── ...
```

Le projet cible est donc le **dossier parent** de `md_ai_system_v5_1`.

Ne confonds pas le `README.md` du système avec celui de ton projet.
Ne déplace pas les fichiers internes du système une fois le projet démarré.

---

## 5. Installation, pas à pas

1. Crée ou ouvre le dossier de ton projet.
2. Place `md_ai_system_v5_1` dans ce dossier (décompresse le ZIP s'il y a lieu).
3. Ouvre **le dossier du projet** dans VS Code : `Fichier > Ouvrir un dossier`.
4. Vérifie dans l'explorateur que tu vois à la fois tes fichiers et le dossier
   `md_ai_system_v5_1`.
5. Envoie le message de démarrage de la section 6.

### Configurer et vérifier en deux commandes

Demande à l'IA d'exécuter, depuis `md_ai_system_v5_1` :

```text
python TOOLS/mdai.py init --policy POC --hosting hostinger \
    --ia1 claude --ia2 chatgpt --ia3 claude --ia4 chatgpt
python TOOLS/mdai.py check
```

`init` écrit tes choix dans la configuration. `check` vérifie Python, Git, la
branche, l'état du dépôt, puis les 15 contrôles de cohérence du système.
Tu dois lire `RESULTAT: PASS` à la fin.

Si un contrôle échoue, l'IA doit t'expliquer lequel et pourquoi, sans rien
modifier d'autre.

---

## 6. Les réglages que tu dois choisir

Ils sont écrits dans `.md-ai-system/CONFIG.json`. L'IA le modifie elle-même, mais
c'est **toi** qui décides.

### 6.1 POLICY_PROFILE — le niveau de rigueur

Jamais deviné par l'IA. Tu choisis un des trois :

| Profil | Pour quoi | Ce que ça change |
|---|---|---|
| `PRODUCTION` | site ou produit destiné à de vrais utilisateurs | contrôles renforcés, tous les checks applicables |
| `STAGING` | préproduction | Git strict, validations normales |
| `POC` | prototype, test d'idée | contrôles allégés **mais** protections dangereuses conservées |

Même en `POC` : jamais de `git add -A`, jamais de reset automatique, jamais
d'écrasement de ton travail, protections sur les secrets et les données.

### 6.2 PROJECT_PROFILE — le type de projet

Déduit par l'IA depuis tes documents et ton projet réel, pas inventé :
`website`, `saas`, `ecommerce`, `api_backend`, `internal_app`.
Plusieurs profils sont possibles si le réel le justifie.

Les catégories qui ne s'appliquent pas à ton projet sont marquées `N/A` et ne sont
pas exécutées.

---

## 7. Le message unique de démarrage

Copie-colle ce message à l'IA **une seule fois**, au début du projet.

```text
Lis d'abord `md_ai_system_v5_1/MANIFEST-MISE-EN-PLACE-UTILISATION.md` et applique-le.

Le projet cible est le dossier parent de `md_ai_system_v5_1`.
Je n'ai aucune connaissance en code : lorsque tu as accès au workspace et au terminal, effectue toi-même les lectures de fichiers, vérifications, commandes, mises à jour JSON et régénérations d'état nécessaires. Ne me demande pas de modifier manuellement les fichiers internes du système ni de copier le contenu des prompts que tu peux lire toi-même.

Respecte strictement les décisions verrouillées, `COMMON-RULES.md`, `WORKFLOW-RULES.md`, `SOURCE-OF-TRUTH-RULES.md`, `POLICY-PROFILES.md`, `NEXT-PROMPT-RULES.md`, `DEPLOYMENT-CONSTRAINTS.md` et `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. En cas de doute sur un terme ou un statut, consulte `GLOSSARY.md`.

Ne devine jamais `POLICY_PROFILE`. S'il n'est pas configuré, demande-moi de choisir uniquement entre PRODUCTION, STAGING ou POC, puis configure le fichier toi-même.

Le double contrôle par deux IA différentes est obligatoire : IA2 doit être une autre IA qu'IA1, IA4 une autre IA qu'IA3. Lis `AI-ROLES-RULES.md` et le bloc `ai_roles` de `.md-ai-system/CONFIG.json`. Si tu es l'IA qui a produit l'étape précédente, ne fais pas l'étape de contrôle : dis-le et arrête-toi.

Ne devine jamais l'hébergement ni les services autorisés : ils sont lus dans le bloc `deployment` de `.md-ai-system/CONFIG.json`. Aucun fournisseur externe n'est proposé lorsque la politique est `deny`. Toute capacité d'hébergement doit être constatée réellement, jamais supposée.

Commence par vérifier le système avec `md_ai_system_v5_1/TOOLS/validate_system.py`, puis les prérequis et l'état du dépôt Git, sans contourner les règles existantes. Ensuite, commence par `md_ai_system_v5_1/PROMPTS/00-START/1-IA1-ANALYSE.md` et lis toi-même tous les fichiers système qu'il référence.

À la fin de chaque étape, exécute la commande unique depuis `md_ai_system_v5_1` :

```
python TOOLS/mdai.py finish-stage --category <CATÉGORIE> --stage <1..4> --ai <ton nom déclaré> --verdict <STATUT> --summary "<résumé>" [--commit <sha>]
```

Elle met à jour l'état, journalise, régénère l'index et la vue, puis retourne `NEXT_PROMPT_PATH`, `NEXT_PROMPT_TO_SEND`, `NEXT_PROMPT_REASON` et `NEXT_PROMPT_AI`. Vérifie toi-même que le prompt retourné existe, puis restitue-moi ces quatre lignes.

N'exécute pas silencieusement le prompt suivant dans la même réponse. J'enverrai ensuite `NEXT_PROMPT_TO_SEND` pour autoriser l'étape suivante.
```

---

## 8. Utilisation quotidienne

Entre deux étapes, tu as **une seule action** :

1. lire le résultat de l'IA ;
2. répondre à une éventuelle décision demandée ;
3. repérer la ligne `NEXT_PROMPT_TO_SEND` ;
4. la renvoyer telle quelle à l'IA.

Exemple de ce que l'IA te donne :

```text
NEXT_PROMPT_TO_SEND: Exécute le prompt `PROMPTS/02-STACK/2-IA2-VERIFICATION.md` en le lisant directement dans le workspace VS Code.
```

Tu n'ouvres pas ce fichier. L'IA le lit elle-même.

Si une IA te demande de copier le contenu d'un prompt alors qu'elle a accès à tes
fichiers, elle ne respecte pas le système : rappelle-lui le message de la
section 6.

---

## 9. Ce que l'IA fait automatiquement après chaque étape

```text
mettre à jour l'état de la catégorie
→ journaliser la transition (AUDIT.jsonl)
→ régénérer STATE.json
→ régénérer STATE-OVERVIEW.md
→ calculer le prochain prompt
→ vérifier qu'il existe
→ te fournir NEXT_PROMPT_TO_SEND
```

Les outils, tous dans `md_ai_system_v5_1/TOOLS/` :

En pratique, **une seule commande fait tout cela** :

```text
python TOOLS/mdai.py finish-stage --category 02-STACK --stage 2 \
    --ai chatgpt --verdict VALIDÉ --summary "analyse confirmée"
```

Les autres commandes utiles :

```text
python TOOLS/mdai.py status                      où en est le projet
python TOOLS/mdai.py next                        prochain prompt + IA attendue
python TOOLS/mdai.py explain --category 02-STACK pourquoi c'est bloqué, en clair
python TOOLS/mdai.py unblock --category 02-STACK --reason "..."   lever un blocage
python TOOLS/mdai.py promote --to PRODUCTION     passer du prototype au réel
python TOOLS/mdai.py check                       prérequis + cohérence
```

Les outils détaillés restent disponibles : `audit_append.py`, `state_index.py`,
`state_overview.py`, `next_prompt.py`, `validate_system.py`.

Tu ne dois jamais modifier toi-même :

```text
.md-ai-system/STATE.json
.md-ai-system/state/*.json
.md-ai-system/DECISIONS.json
.md-ai-system/AUDIT.jsonl
.md-ai-system/APPLICABILITY.md
```

---

## 10. Hébergement, déploiement et médias

Le système ne choisit pas ton hébergeur et n'en suppose jamais les capacités.
Tout est dans le bloc `deployment` de `.md-ai-system/CONFIG.json` :

```json
"deployment": {
  "hosting_target": "hostinger",
  "hosting_plan": null,
  "external_services_policy": "deny",
  "allowed_external_services": [],
  "media_hosting": "self_hosted"
}
```

Ce que cela impose à l'IA :

- **aucun fournisseur externe** tant que la politique est `deny` : ni Vercel,
  Netlify, Render, Supabase, Firebase, Auth0, Cloudinary, S3, ni fonctions
  serverless ou cron tiers ;
- toute solution retenue doit tourner **telle quelle** sur ton hébergement ;
- l'IA doit **constater réellement** ce que l'hébergement offre : version de PHP
  ou Node, base de données, accès SSH ou FTP, tâches planifiées, DNS, e-mail,
  quota disque, taille d'upload. Ce qu'elle ne peut pas vérifier, elle le déclare
  manquant au lieu de le supposer ;
- les **médias** sont hébergés chez toi : images et vidéos encodées et
  redimensionnées en amont, poster obligatoire pour une vidéo, vidéo hero
  toujours muette et sans plein écran forcé, poids et vitesse mesurés sur
  l'hébergement réel, droits et licences documentés pour chaque fichier.

Pour autoriser une exception, elle doit être inscrite dans
`allowed_external_services` et justifiée comme décision verrouillée. Sans cela,
l'IA doit s'arrêter plutôt que contourner.

Règles complètes : `DEPLOYMENT-CONSTRAINTS.md`.

---

## 11. Comprendre les statuts

- `VALIDÉ` : la catégorie a passé ses contrôles.
- `REFUSÉ` : un problème réel subsiste, ou une preuve obligatoire manque.
- `BLOQUÉ` : quelque chose empêche vraiment d'avancer sur cette catégorie.
- `EN_ATTENTE_DE_DÉCISION` : on attend une réponse de ta part.
- `À_RÉÉVALUER` : la catégorie était validée, un changement impose un nouveau contrôle.
- `EN_REVALIDATION` : ce nouveau contrôle est en cours.
- `TERMINÉ` : tout est validé et les conditions finales sont remplies.
- `N/A` : la catégorie ne concerne pas ton projet. C'est une **applicabilité**, pas un statut.
- `TO_DEFINE` : on n'a pas encore décidé si la catégorie s'applique. Rien ne peut
  être clôturé tant qu'il en reste.

Point important : un `VALIDÉ` affiché par **IA2** veut seulement dire « l'analyse
est confirmée, l'exécution peut commencer ». Seule **IA4** valide réellement une
catégorie. Détail : `GLOSSARY.md`.

---

## 12. Voir où en est le projet

```text
md_ai_system_v5_1/.md-ai-system/STATE-OVERVIEW.md
```

Ce fichier est généré depuis les états JSON. Ne le modifie pas à la main.

Tu peux simplement demander :

```text
Lis STATE-OVERVIEW.md et résume-moi où en est le projet : ce qui est validé, bloqué, en attente, et la prochaine étape.
```

---

## 13. Quand ça n'avance pas

### Si une catégorie échoue

Trois cas, trois suites différentes :

- **refusée** → le cycle repart de l'analyse (IA1) en mode correction.
  Jamais d'exécution sur une analyse refusée.
- **bloquée** → la catégorie s'arrête et ne propose plus d'étape. Les autres
  branches du projet continuent. Il faut lever le blocage explicitement pour reprendre.
- **en attente de décision** → elle attend ta réponse. Les autres branches continuent.

Une catégorie en échec ne bloque que les catégories qui **dépendent réellement**
d'elle, pas tout le projet.

### Si le prochain prompt vaut NONE

```text
NEXT_PROMPT_PATH: NONE
```

L'IA doit t'indiquer la cause exacte : applicabilité encore à décider, décision
humaine en attente, blocage à lever, refus à corriger, ou projet terminé.

Ne choisis jamais un prompt au hasard pour contourner un `NONE`.

### Si l'IA détecte tes propres modifications en cours

Elle doit s'arrêter et te le dire. Elle ne doit pas supprimer tes modifications,
les mettre de côté automatiquement, réinitialiser le dépôt, ni les inclure dans
son commit.

---

## 14. Les protections Git, en clair

Tu n'exécutes aucune commande. L'IA applique ces règles :

- travail sur `main` uniquement, aucune branche créée ;
- si des modifications non enregistrées existent : **STOP** ;
- si une modification humaine est détectée : **STOP** ;
- jamais de `stash`, `reset` ou `clean` automatique pour contourner un STOP ;
- jamais `git add -A` ni `git add .` : seuls les fichiers autorisés sont ajoutés ;
- détection des fusions, rebases ou conflits en cours : **STOP** ;
- si `main` distant a bougé pendant l'intervention : **STOP** et réévaluation ;
- retour en arrière non destructif, priorité à `git revert`, jamais de force-push.

Le système ne t'impose pas de synchroniser le dépôt avant la première
vérification, ni d'être aligné sur le distant avant l'exécution.

---

## 15. Prototype d'abord, projet réel ensuite

Si tu veux d'abord tester une idée, choisis `POC`. Un prototype n'est pas un
projet bâclé : c'est un projet dont le périmètre contrôlé est réduit **et écrit**.

Restent obligatoires même en POC : protections Git, secrets, données réelles,
double contrôle par deux IA, contraintes d'hébergement, tests réels des chemins
critiques, licences des médias, consentement si tu collectes des données
personnelles.

Peuvent être mis de côté, avec justification : régression visuelle, cross-browser,
SEO opérationnel, changelog, gestion des incidents, parité d'environnements,
support client. On les enregistre ainsi :

```text
python TOOLS/mdai.py set --category 39-VISUAL-REGRESSION --applicability N/A \
    --reason "hors périmètre du prototype" --policy-scoped
```

`--policy-scoped` veut dire : « ce N/A ne vaut que pour le prototype ».
C'est ta dette, visible et récupérable.

Le jour où le prototype devient un vrai projet :

```text
python TOOLS/mdai.py promote --to PRODUCTION
```

Le système remet automatiquement en jeu tout ce qui avait été mis de côté au titre
du prototype, et remet à revalider ce qui avait été validé au niveau POC. **Aucune
validation n'est effacée** : tout est recontrôlé au nouveau niveau d'exigence.

## 16. Démarrer un nouveau projet

1. Utilise une **copie neuve** de `md_ai_system_v5_1`.
2. Place-la dans le nouveau dossier projet.
3. N'importe **jamais** les JSON d'état d'un ancien projet.
4. Ouvre le nouveau dossier projet dans VS Code.
5. Renvoie le message de la section 6.
6. Choisis le nouveau `POLICY_PROFILE` et confirme l'hébergement.

Chaque projet garde son propre état.

---

## 17. Ce que tu ne dois normalement jamais faire

- Modifier les fichiers JSON d'état.
- Choisir manuellement un prompt parmi les 216.
- Copier le contenu d'un prompt dans le chat quand l'IA a accès au workspace.
- Modifier le graphe de dépendances en cours de projet sans décision explicite.
- Éditer une décision verrouillée directement.
- Utiliser `git add -A` « pour aider » l'IA.
- Utiliser `stash` ou `reset` pour contourner un STOP du système.
- Autoriser un service externe sans l'inscrire dans `allowed_external_services`.

---

## 18. Le raccourci à retenir

```text
1. J'ouvre le dossier du projet dans VS Code.
2. J'ouvre deux IA : A et B.
3. J'envoie le message unique de démarrage à l'IA A.
4. Je choisis PRODUCTION / STAGING / POC et je confirme l'hébergement.
5. L'IA travaille sur l'étape courante.
6. Elle me donne NEXT_PROMPT_TO_SEND et NEXT_PROMPT_AI.
7. Je renvoie cette ligne à l'IA indiquée (A ou B).
8. Je réponds seulement quand le système a besoin d'une vraie décision.
```

---

## 19. Phrases utiles à envoyer à l'IA

| Ce que tu veux | Ce que tu envoies |
|---|---|
| Vérifier que le système est sain | `Exécute TOOLS/mdai.py check et donne-moi le résultat.` |
| Savoir où on en est | `Lis STATE-OVERVIEW.md et résume-moi l'avancement et la prochaine étape.` |
| Comprendre un blocage | `Exécute TOOLS/mdai.py explain --category <CATÉGORIE> et explique-moi en langage simple.` |
| Reprendre après une pause | `Reprends depuis l'état persistant. Ne te fie pas à la conversation précédente.` |
| Changer de niveau de rigueur | `Passe POLICY_PROFILE à PRODUCTION dans CONFIG.json et dis-moi ce que ça change.` |
| Vérifier l'hébergement | `Vérifie réellement ce que l'hébergement fournit et dis-moi ce que tu ne peux pas vérifier.` |
| Passer du prototype au réel | `Exécute TOOLS/mdai.py promote --to PRODUCTION et explique-moi ce qui va être recontrôlé.` |
| Savoir qui doit travailler | `Donne-moi NEXT_PROMPT_AI : quelle IA doit faire l'étape suivante ?` |
| Contrôler les médias | `Lis MEDIA-MANIFEST.md et dis-moi quelles pages n'ont pas de média conforme.` |
