# AGENTS.md — LA FIDUCIAIRE

Ce fichier s’applique à tout agent IA travaillant dans ce dépôt.

## 1. Lecture obligatoire

Lire dans cet ordre :

1. `markdown_docs/00_SOURCE_OF_TRUTH.md`
2. `PROMPT_MAITRE_LA_FIDUCIAIRE.md`
3. `markdown_docs/CONCEPT_BUSINESS.md`
4. `markdown_docs/ARCHITECTURE.md`
5. `markdown_docs/DESIGN_SYSTEM.md`
6. `markdown_docs/HOMEPAGE_COPY.md`
7. `markdown_docs/SEO_CONTENT.md`
8. `markdown_docs/DEPLOYMENT.md`
9. `md_ai_system_v5_1/DEPLOYMENT-CONSTRAINTS.md`
10. `md_ai_system_v5_1/.md-ai-system/CONFIG.json`

## 2. Infrastructure verrouillée

Production et infrastructure : **Hostinger uniquement**.

Interdits sans exception implicite :

- Supabase ;
- Vercel ;
- Netlify ;
- Firebase ;
- Render ;
- Railway ;
- Fly.io ;
- Neon ;
- PlanetScale ;
- Turso ;
- MongoDB Atlas ;
- Clerk ;
- Auth0 ;
- Cloudinary ;
- stockage objet, backend, auth, serverless, cron ou base managée hors Hostinger.

Ne pas ajouter une plateforme interdite « temporairement », « pour prototyper » ou « pour aller plus vite ».

Si Hostinger ne permet pas une fonction : adapter l’architecture ou marquer le blocage. Ne jamais contourner la contrainte avec un autre fournisseur.

## 3. Stack MVP

Conserver sauf décision explicite contraire :

- Astro ;
- TypeScript ;
- CSS natif avec variables CSS ;
- Markdown/MDX ;
- PHP pour le formulaire serveur ;
- GitHub pour le code ;
- Hostinger pour l’hébergement.

Aucune base de données n’est requise pour le MVP.

## 4. Phase dynamique future

Toute base, auth, stockage, job, média ou runtime serveur futur doit fonctionner sur Hostinger et être choisi uniquement après vérification du plan réel.

Ne jamais supposer que Node, MySQL/MariaDB, SSH, cron ou un processus persistant est disponible.

## 5. Design

Direction : **minimalisme suisse contemporain, premium mais accessible**.

Éviter :

- esthétique SaaS générique ;
- design de banque froide ;
- gradients décoratifs ;
- glassmorphism ;
- ombres lourdes ;
- faux avis/chiffres/clients ;
- photos corporate clichés ;
- animation gratuite.

## 6. Données et contenu

Ne pas inventer :

- adresse ;
- témoignages ;
- clients ;
- partenaires ;
- certifications ;
- chiffres ;
- résultats ;
- données locales ;
- mentions légales.

Les documents historiques comportent des artefacts d’encodage et des phrases tronquées. Ne jamais publier ces défauts ni inventer les fragments manquants.

## 7. Qualité

Avant commit applicatif :

```bash
npm run check
npm run build
```

Si le formulaire PHP est concerné et PHP est disponible :

```bash
php -l server/contact.php
```

Pour toute modification UI, vérifier un rendu mobile, tablette et desktop.

## 8. Git automatique

Avant commit :

```bash
git config user.name "SwissEliteVan"
git config user.email "214782361+SwissEliteVan@users.noreply.github.com"
```

Après validation :

```bash
git status --short
git diff --check
git add -- <fichiers_du_lot_validé>
git diff --cached --check
git diff --cached --stat
git diff --cached --quiet || git commit -m "<message_de_commit>"
BRANCH="$(git branch --show-current)"
git push origin "$BRANCH"
```

Ne pas demander confirmation lorsque le lot est validé et sûr.

Interdits automatiques :

- `git push --force` ;
- `git push --force-with-lease` ;
- `git reset --hard` ;
- `git clean -fd` ;
- écrasement de changements humains non analysés.

## 9. Contrôle avant clôture

Une phase ne peut pas être déclarée terminée si :

- elle dépend d’un service technique hors Hostinger ;
- le build ne passe pas ;
- le rendu n’a pas été contrôlé alors qu’il a changé ;
- des secrets sont présents ;
- du contenu fictif est présenté comme réel ;
- le commit/push n’a pas été effectué alors qu’il était possible.