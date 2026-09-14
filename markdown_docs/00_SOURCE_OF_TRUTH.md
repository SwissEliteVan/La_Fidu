# 00_SOURCE_OF_TRUTH — LA FIDUCIAIRE

Ce document verrouille les décisions qui ne doivent pas être redéfinies silencieusement par le code, une IA ou un ancien document.

## 1. Produit

Nom de travail : **LA FIDUCIAIRE**.

Positionnement : fiduciaire digitale de proximité pour Vevey, la Riviera vaudoise et Lausanne.

Promesse : apporter de la clarté comptable et financière, avec une relation humaine, des forfaits transparents, des explications compréhensibles et un accompagnement proactif.

Le site public sert principalement à :

- présenter les services ;
- présenter les offres et tarifs ;
- rassurer ;
- générer des demandes de devis ;
- permettre la prise de rendez-vous ;
- orienter vers l’espace client validé ;
- développer le référencement local et les contenus.

## 2. Stack MVP verrouillée

Le MVP public utilise :

```text
Astro
TypeScript
CSS natif + variables CSS
Markdown / MDX
PHP pour le formulaire serveur
GitHub pour le versionnement
Hostinger pour l’hébergement
```

Aucune base de données n’est nécessaire pour le MVP.

Le site public ne doit pas développer au lancement :

- coffre-fort documentaire propriétaire ;
- messagerie financière interne ;
- gestion de salaires propriétaire ;
- tableau de bord comptable propriétaire ;
- système de paiement ;
- automatisation fiscale non validée ;
- authentification propriétaire sans besoin confirmé.

## 3. Hébergement et infrastructure — décision absolue

**Hostinger est l’unique cible autorisée pour l’hébergement et l’infrastructure technique du produit.**

La politique est :

```text
hosting_target = hostinger
external_services_policy = deny
allowed_external_services = []
media_hosting = self_hosted
```

Cette décision s’applique au MVP et aux futures phases dynamiques.

## 4. Interdictions infrastructure

Sans nouvelle décision explicite de l’utilisateur, il est interdit de développer ou déployer avec :

- Supabase ;
- Vercel ;
- Netlify ;
- Firebase ;
- Render ;
- Railway ;
- Fly.io ;
- Cloudflare Workers/Pages comme runtime applicatif ;
- AWS Amplify ;
- Neon ;
- PlanetScale ;
- Turso ;
- MongoDB Atlas ;
- Aiven ;
- Clerk ;
- Auth0 ;
- Cloudinary ;
- tout backend-as-a-service ;
- toute base managée externe ;
- toute authentification managée externe ;
- tout stockage applicatif externe ;
- toute fonction serverless externe ;
- tout cron/job/queue externe utilisé comme composant du produit.

La liste est non limitative. Toute solution qui déplace l’exécution ou le stockage du produit hors Hostinger est interdite.

## 5. Phase dynamique future

Si une phase dynamique devient nécessaire :

1. constater le plan Hostinger réel ;
2. constater les runtimes réellement disponibles ;
3. constater la base réellement disponible ;
4. constater SSH/Git/FTP/SFTP/cron/SSL/quota ;
5. choisir uniquement une architecture compatible Hostinger.

Si une base est nécessaire, utiliser uniquement une base fournie ou hébergeable sur Hostinger. Ne jamais résoudre le besoin en créant automatiquement un projet Supabase, Neon, Firebase ou équivalent.

Si une authentification est nécessaire, elle doit être exécutée sur Hostinger.

Si du stockage applicatif est nécessaire, il doit être hébergé sur Hostinger et conçu avec les protections adaptées.

Si Hostinger ne permet pas une capacité, adapter le produit ou déclarer le blocage. Ne jamais migrer silencieusement vers un autre fournisseur.

## 6. Services métier externes

Les documents historiques prévoient éventuellement des liens vers des outils métier externes déjà validés, par exemple un portail client spécialisé ou un service de rendez-vous.

Ces liens ne sont pas une autorisation d’utiliser ces fournisseurs comme backend, base, stockage ou hébergement du site.

Toute nouvelle intégration externe nécessite une décision explicite avant implémentation.

## 7. Déploiement

Le build Astro doit produire un artefact statique déployable sur Hostinger.

Mode de publication :

- Git Hostinger si disponible ;
- SSH/SFTP/FTP Hostinger ;
- publication manuelle documentée du build `dist/` ;
- PHP exécuté sur Hostinger pour le formulaire MVP.

Ne jamais déployer ailleurs comme fallback ou environnement temporaire.

## 8. Médias

Les médias du site sont auto-hébergés sur Hostinger.

Pas de CDN ou service d’optimisation média externe requis pour faire fonctionner le produit.

Optimiser localement ou au build les formats, tailles et variantes.

## 9. Design

Direction verrouillée : **minimalisme suisse contemporain, premium mais accessible**.

Le site doit exprimer : confiance, précision, proximité, calme, modernité et compétence.

Il ne doit pas ressembler à :

- une banque froide ;
- une app grand public ludique ;
- un dashboard SaaS ;
- un template générique surchargé d’effets.

## 10. Contenu réel uniquement

Ne pas publier comme réalité :

- faux avis ;
- faux témoignages ;
- faux clients ;
- fausse adresse ;
- faux partenaires ;
- fausses certifications ;
- faux résultats ;
- faux chiffres.

Les données de démonstration restent explicitement marquées `DEMO`.

## 11. Documents historiques corrompus

Certains `.md` actuels contiennent du mojibake et des phrases tronquées.

Ils restent utiles comme source métier, mais :

- ne pas publier les caractères corrompus ;
- ne pas inventer les fragments manquants ;
- faire valider les informations réellement ambiguës ;
- les décisions du présent fichier priment sur toute suggestion technique contradictoire.

## 12. Git

Identité obligatoire pour les nouveaux commits locaux :

```text
user.name = SwissEliteVan
user.email = 214782361+SwissEliteVan@users.noreply.github.com
```

Les lots validés sont commités et poussés automatiquement, sans force push.

## 13. Phrase normative

```text
TOUT COMPOSANT TECHNIQUE DU PRODUIT DOIT ÊTRE CONÇU POUR HOSTINGER.
UNE LIMITE HOSTINGER NE JUSTIFIE JAMAIS SUPABASE, VERCEL OU UN AUTRE FOURNISSEUR EN CONTOURNEMENT.
```