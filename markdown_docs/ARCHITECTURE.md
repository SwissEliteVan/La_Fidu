# Architecture Technique - LA FIDUCIAIRE

## Objectif

Construire un site public rapide, maintenable, indexable et compatible avec un hébergement Hostinger.

Le MVP ne contient pas de coffre-fort documentaire propriétaire.

## Choix technique

### Frontend

- **Astro** : Génération de pages statiques rapides et SEO-friendly.
- **TypeScript** : Code plus fiable et maintenable.
- **CSS natif avec variables** : Moins de dépendances et contrôle complet du design.
- **Lucide Icons** : Icô·²·nes sobres et cohé·²rentes.
- **Markdown ou MDX** : Articles SEO faciles à maintenir.

### Backend minimal

- **Endpoint PHP sé.
- Envoi vers une adresse professionnelle.
- Protection anti-spam.
- Validation serveur.
- Aucun document comptable accepté.

### Portail client

Le bouton "Espace client" redirige vers l'outil externe validé·² par la fiduciaire.

Ne pas créer de système d'authentification propriétaire dans le MVP.

## Arborescence du projet

```
la-fiduciaire/
├── public/
│   ├── favicon.svg
│   ├── logo.svg
│   ├── og-image.jpg
│   ├── robots.txt
│   └── sitemap.xml
├── src/
│   ├── components/
│   │   ├── Button.astro
│   │   ├── ContactForm.astro
│   │   ├── Footer.astro
│   │   ├── Header.astro
│   │   ├── LocalTrustBar.astro
│   │   ├── PricingCard.astro
│   │   ├── ServiceCard.astro
│   │   └── TestimonialCard.astro
│   ├── content/
│   │   ├── config.ts
│   │   └── blog/
│   │       ├── comptabilite-independant-vevey.md
│   │       ├── cout-fiduciaire-sarl-vaud.md
│   │       └── declaration-tva-vaud.md
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── BlogLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── a-propos.astro
│   │   ├── contact.astro
│   │   ├── tarifs.astro
│   │   ├── espace-client.astro
│   │   ├── services/
│   │   │   ├── index.astro
│   │   │   ├── independants.astro
│   │   │   ├── pme.astro
│   │   │   ├── salaries.astro
│   │   │   ├── tva.astro
│   │   │   └── creation-entreprise.astro
│   │   ├── ressources/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── fiduciaire-vevey.astro
│   │   ├── fiduciaire-riviera-vaudoise.astro
│   │   └── fiduciaire-lausanne.astro
│   ├── styles/
│   │   ├── global.css
│   │   └── tokens.css
│   └── data/
│       ├── navigation.ts
│       ├── pricing.ts
│       └── services.ts
├── server/
│   └── contact.php
├── .env.example
├── .gitignore
├── astro.config.mjs
├── package.json
├── tsconfig.json
├── README.md
├── CONCEPT_BUSINESS.md
├── DESIGN_SYSTEM.md
├── ARCHITECTURE.md
└── DEPLOYMENT.md
```

## Routes publiques

- `/` - Accueil
- `/a-propos` - À propos
- `/contact` - Contact
- `/tarifs` - Tarifs
- `/espace-client` - Espace client
- `/services` - Services
- `/services/independants` - Indé·²pendants
- `/services/pme` - PME
- `/services/salaries` - Salaires
- `/services/tva` - TVA
- `/services/creation-entreprise` - Cré.
- `/ressources` - Ressources
- `/ressources/[slug]` - Article
- `/fiduciaire-vevey` - Fiduciaire Vevey
- `/fiduciaire-riviera-vaudoise` - Fiduciaire Riviera
- `/fiduciaire-lausanne` - Fiduciaire Lausanne

## Composants

### Header

Navigation principale, logo, CTA et accès au portail client.

### Footer

Coordonné·²es, zones desservies, liens lé.

### PricingCard

Affiche le nom, le tarif de dé.

### ContactForm

Formulaire public avec validation cô.

### ServiceCard

Carte ré.

### LocalTrustBar

Zone pré.

### FAQ

Questions fré.

## SEO technique

Chaque page doit disposer de :

- Un title unique.
- Une meta-description unique.
- Une URL courte.
- Un seul H1.
- Des H2 structuré·²s.
- Un canonical.
- Un Open Graph title.
- Une image Open Graph.
- Un texte alternatif.
- Des liens internes pertinents.

### À créer

- `robots.txt`
- `sitemap.xml`
- Donné·²es JSON-LD Organization
- Donné·²es JSON-LD LocalBusiness si les informations sont exactes
- Donné·²es JSON-LD Article pour le blog

Ne pas publier de fausses adresses, faux avis ou fausses informations locales.

## Formulaire

### Champs

- Nom.
- Société.
- E-mail.
- Té.
- Commune.
- Forme juridique.
- Besoin.
- Nombre approximatif de pièces mensuelles.
- Message.
- Consentement à la politique de confidentialité·².

### Exigences

Le formulaire doit :

- Vé.
- Vé.
- Refuser les fichiers joints dans le MVP.
- Inclure un champ honeypot.
- Ajouter une limitation de fré.
- Retourner un message de confirmation gé.
- Ne pas afficher l'adresse e-mail de destination dans le frontend.

## Base de données

### MVP

Aucune base de données n'est né.

Les prospects sont reçus dans une boî·²te e-mail professionnelle ou un CRM.

### Phase 2

Une base peut être envisagé·²e pour :

- Le suivi des leads.
- Les demandes de devis.
- Les rendez-vous.
- Les campagnes marketing.

Elle ne doit pas stocker de documents comptables sans conception de sé.

### Modèle prospect proposé.

Table `leads` :

- `id`
- `created_at`
- `name`
- `company`
- `email`
- `phone`
- `city`
- `legal_form`
- `need`
- `monthly_documents`
- `message`
- `consent_at`
- `status`
- `source`

Valeurs possibles pour `status` :

- `new`
- `contacted`
- `qualified`
- `proposal_sent`
- `won`
- `lost`

## Sé.

### Principes

- HTTPS obligatoire.
- Secrets dans des variables d'environnement.
- Aucun secret dans Git.
- Validation serveur.
- Protection anti-spam.
- Limitation de fré.
- Backups ré.
- Accès administrateur limité.
- Portail documentaire externe.
- Journalisation minimale.
- Suppression des données selon une politique interne dé.

### Conformité·² nLPD

- Traitement des données personnelles conforme.
- Information claire sur l'utilisation des données.
- Consentement explicite pour le marketing.
- Droit d'accè·²s et de suppression.
- Durée de conservation limitée.
- Sécurité approprié·²e.

## Performance

### Optimisations

- Images au format WebP ou AVIF.
- Dimensions dé.
- Lazy loading sauf image principale.
- Pas de bibliothè·²que JavaScript lourde.
- CSS regroupé·².
- Polices limité.
- Score Lighthouse à contrôler avant mise en ligne.

### Objectifs

- Score Lighthouse > 90.
- Temps de chargement < 3s.
- First Contentful Paint < 1.5s.
- Time to Interactive < 3.5s.

## Tests avant publication

### Fonctionnels

- Navigation desktop et mobile.
- Formulaire valide et invalide.
- Liens internes.
- Liens externes.
- CTA.
- Portail client.
- Meta-donné·²es.
- Sitemap.
- Robots.
- Page 404.

### Responsive

- iPhone.
- Android.
- Tablette.
- Ordinateur portable.
- Grand é.

### Accessibilité·²

- Navigation au clavier.
- Focus.
- Contraste.
- Labels.
- Texte alternatif.
- Taille des textes.

### Performance

- Images compressé·²es.
- Pas de scripts inutiles.
- Pas de vid é.
- Vé.

## Données structur.

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "LA FIDUCIAIRE",
  "url": "https://www.exemple.ch",
  "logo": "https://www.exemple.ch/logo.svg",
  "description": "Fiduciaire digitale de proximité pour Vevey, la Riviera vaudoise et Lausanne",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Vevey",
    "addressRegion": "VD",
    "addressCountry": "CH"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+41 21 123 45 67",
    "contactType": "customer service"
  }
}
```

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "AccountingService",
  "name": "LA FIDUCIAIRE",
  "image": "https://www.exemple.ch/og-image.jpg",
  "url": "https://www.exemple.ch",
  "telephone": "+41 21 123 45 67",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rue du Lac 12",
    "addressLocality": "Vevey",
    "postalCode": "1800",
    "addressRegion": "VD",
    "addressCountry": "CH"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "08:30",
    "closes": "17:30"
  },
  "priceRange": "CHF"
}
```

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Combien coûte une fiduciaire en Suisse ?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Les tarifs varient selon la structure, le volume et les services. Nos forfaits commencent dès CHF 190 par mois HT."
    }
  }]
}
```

## Checklist pré.

- [ ] Arborescence créé.
- [ ] Composants dé.
- [ ] Routes configuré·²es.
- [ ] SEO technique implé·²menté·².
- [ ] Formulaire fonctionnel.
- [ ] Sécurité vé.
- [ ] Performance optimisé·²e.
- [ ] Tests effectué.
- [ ] Données structur.
- [ ] Documentation complé·²té·²e.
