# CONTRAINTES D'HÉBERGEMENT, DE DÉPLOIEMENT ET DE MÉDIAS

Règle système (N0). Elle s'applique dès `02-STACK` et jusqu'à `53-FINAL-CLOSURE`.
Elle est paramétrée par `.md-ai-system/CONFIG.json` : le système ne devine ni
l'hébergeur, ni les services autorisés.

## 1. Paramétrage

Bloc `deployment` de `.md-ai-system/CONFIG.json` :

```json
{
  "deployment": {
    "hosting_target": "hostinger",
    "hosting_plan": null,
    "external_services_policy": "deny",
    "allowed_external_services": [],
    "media_hosting": "self_hosted"
  }
}
```

- `hosting_target` — hébergeur réel du projet. Aucune valeur par défaut devinée.
- `hosting_plan` — offre réelle (mutualisé, cloud, VPS). `null` tant qu'elle n'a
  pas été constatée ou fournie.
- `external_services_policy` — `deny` (défaut) ou `allow_listed`.
- `allowed_external_services` — dérogations explicitement validées, une par
  service, avec justification enregistrée dans la SOURCE OF TRUTH.
- `media_hosting` — `self_hosted` ou un service figurant dans
  `allowed_external_services`.

Si le bloc `deployment` est absent ou incomplet : `EN_ATTENTE_DE_DÉCISION`.
Ne jamais supposer l'hébergeur à partir du code, du domaine ou d'un usage courant.

## 2. Interdiction des fournisseurs externes

Lorsque `external_services_policy = "deny"`, il est interdit de proposer,
d'installer, de configurer ou de supposer un service tiers hébergé, notamment :

- plateformes d'hébergement/déploiement tierces (Vercel, Netlify, Render,
  Railway, Fly, Cloudflare Pages, Amplify, App Engine, etc.) ;
- bases de données ou backends managés (Supabase, Firebase, PlanetScale, Neon,
  MongoDB Atlas, Turso, etc.) ;
- authentification managée (Auth0, Clerk, Supabase Auth, Firebase Auth, etc.) ;
- stockage/CDN/média managés (S3, Cloudinary, imgix, Uploadcare, Bunny, etc.) ;
- fonctions serverless, edge functions et workers tiers ;
- files d'attente, cron ou monitoring tiers lorsqu'un équivalent existe sur
  l'hébergement réel.

Cette liste est indicative et non limitative : la règle porte sur la nature du
service (exécution ou stockage hors de l'hébergement du projet), pas sur un nom.

Conséquence obligatoire : toute solution retenue doit fonctionner avec les seules
capacités réellement offertes par `hosting_target`.

Dérogation : uniquement si le service est listé dans
`allowed_external_services`, avec justification, périmètre, alternative écartée
et coût, enregistrés comme décision verrouillée. Sans cela : `BLOQUÉ` ou
`EN_ATTENTE_DE_DÉCISION`, jamais un contournement silencieux.

## 3. Vérification du réel avant toute décision technique

Aucune capacité d'hébergement n'est supposée. Avant de retenir une stack, un
runtime, une base ou un mode de déploiement, constater réellement :

- runtimes disponibles et versions (PHP, Node, Python) ;
- possibilité ou non d'exécuter un processus persistant ;
- base de données réellement fournie et sa version ;
- accès SSH, Git, FTP/SFTP, panneau d'administration ;
- répertoire de publication réel du site ;
- tâches planifiées disponibles et granularité ;
- gestion DNS, sous-domaines, certificats TLS ;
- comptes e-mail et enregistrements SPF/DKIM/DMARC ;
- limites réelles : quota disque, mémoire, processus, taille d'upload,
  bande passante.

Ce qui ne peut pas être constaté est déclaré manquant, pas supposé.
Une capacité annoncée commercialement mais non vérifiée n'est pas une preuve.

## 4. Effet par catégorie

| Catégorie | Contrainte ajoutée |
|---|---|
| `02-STACK` | Ne retenir qu'une stack déployable telle quelle sur `hosting_target`. Écarter explicitement toute stack exigeant un fournisseur interdit. Enregistrer la contrainte comme décision verrouillée. |
| `03-BOOTSTRAP` | Le scaffold ne doit introduire aucune dépendance à un service interdit, y compris dans les valeurs par défaut d'un générateur. |
| `05-DATA-BACKEND-AUTH` | Base de données et authentification auto-hébergées sur l'hébergement réel. |
| `17-MEDIA-HERO-IMAGES-BLOG` | Voir §5. |
| `23-INTEGRATIONS` | Chaque intégration externe est vérifiée contre la politique ; une intégration interdite est un blocage documenté, pas une exception silencieuse. |
| `24-EMAIL-DNS` | E-mail et DNS gérés sur l'hébergement réel, sauf dérogation validée. |
| `25-PAYMENTS-ECOM` | Un prestataire de paiement reste un service externe : il exige une dérogation explicite ; seule l'intégration côté serveur du projet est concernée. |
| `26-JOBS-CRON` | Utiliser l'ordonnanceur réellement disponible sur l'hébergement ; pas de cron tiers. |
| `35-ANALYTICS-MONITORING`, `36-HEALTH-UPTIME` | Privilégier une solution auto-hébergée ; tout service tiers exige une dérogation. |
| `45-CI-CD` | La chaîne doit produire un artefact déployable sur `hosting_target` par les moyens réellement disponibles (Git, SSH, FTP/SFTP, publication manuelle documentée). |
| `46-ENV-PARITY` | La parité se mesure contre l'environnement réel de `hosting_target`, pas contre un environnement local idéalisé. |
| `47-STAGING-DEPLOY` | Le déploiement, le staging et le rollback utilisent uniquement les mécanismes de `hosting_target`. Le rollback reste non destructif. |

## 5. Médias — contrainte renforcée

Les médias sont un livrable critique du projet, pas un habillage.
`17-MEDIA-HERO-IMAGES-BLOG` reste la catégorie de référence ; les règles
existantes de son prompt s'appliquent intégralement et ne sont ni allégées, ni
remplacées par ce document.

S'y ajoutent, lorsque `media_hosting = "self_hosted"` :

- tous les fichiers médias sont hébergés sur `hosting_target` ; aucun CDN,
  aucun service d'optimisation d'images tiers, aucun hotlink vers une plateforme
  externe ;
- les formats et dérivés (WebP/AVIF, MP4/WebM, poster, tailles responsives) sont
  produits au build ou en amont, puis versionnés ou déposés sur l'hébergement ;
  aucune transformation à la volée par un service externe ;
- vidéo hero : encodage local, poids maîtrisé, `muted` + `playsinline`, poster
  obligatoire, fallback image, respect de `prefers-reduced-motion` et des
  connexions lentes ;
- LCP, CLS et poids réel sont mesurés sur l'hébergement réel, pas en local
  uniquement ;
- droits et licences de chaque média sont documentés (`18-ASSET-LICENSES`) ;
- les limites réelles de l'hébergement (taille d'upload, quota disque, bande
  passante) sont vérifiées avant de retenir un média lourd ;
- `MEDIA-MANIFEST.md` enregistre pour chaque média : page, type de hero, fichier,
  variantes desktop/mobile, fallback, ALT, poids, LCP, CLS, droits, statut.

Un média manquant, non optimisé, sans droits documentés ou non mesuré est un
écart réel : IA4 refuse.

## 6. Contrôles IA

- IA1 constate l'hébergement réel, les capacités disponibles et les services
  externes déjà présents dans le projet.
- IA2 revérifie indépendamment que la solution proposée ne dépend d'aucun service
  interdit, y compris de manière indirecte (dépendance transitive, SDK,
  configuration par défaut d'un framework, appel réseau au runtime).
- IA3 n'installe ni ne configure aucun service interdit, même temporairement,
  même « pour tester ».
- IA4 refuse si un service interdit subsiste dans le code, les dépendances, la
  configuration, les variables d'environnement ou la documentation.

Toute dépendance externe découverte et non prévue est un écart, pas une
fonctionnalité.
