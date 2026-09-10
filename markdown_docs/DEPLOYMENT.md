# Déploiement sur Hostinger - LA FIDUCIAIRE

## Objectif

Dé·²ployer la version statique du site Astro sur le domaine officiel de LA FIDUCIAIRE.

La mé.

## 1. Pré.

### Installer les dé.

```bash
npm install
```

### Vé.

```bash
npm run check
```

### Cré.

```bash
npm run build
```

Le dossier de production gé.

### Tester le build localement

```bash
npm run preview
```

### Vé.

- La page d'accueil s'affiche.
- Les liens fonctionnent.
- Les images sont visibles.
- Le formulaire pointe vers la bonne destination.
- Les URLs sont correctes.
- Le site est responsive.

## 2. Configurer les variables

### Cré.

Ne jamais le publier dans GitHub.

### Exemple de variables

```env
PUBLIC_SITE_URL=https://www.exemple.ch
PUBLIC_BOOKING_URL=https://calendly.com/exemple
PUBLIC_CLIENT_PORTAL_URL=https://portail.exemple.ch
```

Les variables secrè·²tes destiné.

## 3. Cré.

### Cré.

```
la-fiduciaire
```

### Initialiser Git

```bash
git init
```

### Ajouter les fichiers

```bash
git add .
```

### Cré.

```bash
git commit -m "Initial website structure"
```

### Associer le dé.

```bash
git remote add origin https://github.com/UTILISATEUR/la-fiduciaire.git
```

### Envoyer la branche principale

```bash
git branch -M main
git push -u origin main
```

### Vé.

- `.env`
- Les mots de passe.
- Les exports clients.
- Les fichiers privé.

## 4. Configurer le domaine

### Dans Hostinger

1. Ouvrir hPanel.
2. Aller dans Domaines.
3. Sé.
4. Ouvrir la zone DNS.
5. Vé.

### Configuration habituelle

- `A` pour le domaine racine vers l'adresse IP Hostinger.
- `CNAME` pour `www` vers le domaine racine, selon les instructions affich.
- Supprimer les anciens enregistrements contradictoires.
- Conserver les enregistrements e-mail existants si la messagerie est utilisé.
- Ne pas modifier les enregistrements MX sans vé.

La propagation DNS peut prendre du temps. Tester le domaine racine et la version `www`.

## 5. Activer le certificat SSL

### Dans hPanel

1. Ouvrir le site.
2. Aller dans la section SSL.
3. Activer le certificat pour le domaine et le sous-domaine `www`.
4. Attendre l' é.
5. Activer la redirection HTTP vers HTTPS si l'option est disponible.

### Tester

- `https://exemple.ch`
- `https://www.exemple.ch`

Le site doit utiliser une seule version canonique.

## 6. Cré.

### Pour un site statique

1. Ouvrir hPanel.
2. Aller dans Websites.
3. Sé.
4. Ouvrir File Manager.
5. Accé·²der au dossier `public_html`.
6. Sauvegarder les fichiers existants si né.
7. Supprimer la page de dé.
8. Ouvrir le dossier local `dist`.
9. Sé.
10. Cré.
11. Té.
12. Extraire l'archive.
13. Vé.
14. Vé.
15. Supprimer l'archive ZIP après extraction.
16. Ouvrir le domaine dans un navigateur privé.

### Attention

Il faut télé.

## 7. Dé.

### Si le plan Hostinger permet la connexion Git

1. Ouvrir hPanel.
2. Aller dans Websites.
3. Choisir le site.
4. Ouvrir Advanced puis Git, selon l'interface affich.
5. Connecter le compte GitHub.
6. Sé.
7. Choisir la branche `main`.
8. Dé.
9. Dé.
   ```bash
   npm install
   ```
10. Dé.
    ```bash
    npm run build
    ```
11. Dé.
    ```bash
    dist
    ```
12. Lancer le dé.
13. Ouvrir l'URL publique.
14. Consulter les logs en cas d'erreur.

### Si Hostinger ne propose pas une configuration Astro adapté.

Utiliser le dé.

## 8. Formulaire PHP

### Placer le fichier PHP

Placer le fichier PHP dans un emplacement non accessible directement si la configuration Hostinger le permet.

### Si l'endpoint est public

- Ne jamais inclure de mot de passe dans le frontend.
- Valider tous les champs cô.
- Utiliser un honeypot.
- Limiter les requê·²tes.
- Refuser les pièces jointes.
- Ne pas renvoyer les données saisies dans une ré.
- Utiliser une adresse e-mail professionnelle.
- Tester la ré.

Le formulaire ne doit pas accepter de documents comptables au lancement.

## 9. Configuration e-mail

### Cré.

```
contact@exemple.ch
```

### Configurer les enregistrements

Configurer les enregistrements SPF, DKIM et DMARC selon les instructions du fournisseur e-mail.

### Tester

- Ré.
- Ré.
- Ré.
- Dé.
- Signature e-mail.
- Message automatique de confirmation.

## 10. Vé.

### Tester

- `/robots.txt`
- `/sitemap.xml`
- Les balises title.
- Les meta-descriptions.
- Les URLs canoniques.
- Les aperç·²us Open Graph.
- Les données structur.
- Les erreurs 404.
- Les redirections HTTP vers HTTPS.
- La version mobile.

### Ajouter le domaine

Ajouter le domaine dans Google Search Console et envoyer le sitemap.

### Cré.

Cré·²er ou vé.

## 11. Tests finaux

### Fonctionnels

- Navigation.
- CTA.
- Formulaire.
- Prise de rendez-vous.
- Portail client.
- Té.
- E-mail.
- Carte et adresse.

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

## 12. Sauvegarde et maintenance

### Actions ré.

- Conserver le code sur GitHub.
- Exporter ré.
- Vé.
- Mettre à jour Astro et les bibliothè·²ques.
- Contrô·²·ler les formulaires chaque mois.
- Vé.
- Publier ré.
- Ré.
- Vé.

## 13. Phase 2

Une application dynamique peut être ajouté.

- Authentification sé.
- Base de données.
- Tableau de bord.
- Gestion des prospects.
- Notifications.
- Connexion à un portail documentaire spé.
- API de prise de rendez-vous.
- Espace administrateur.

Cette phase ne doit être lancé.

## Checklist de dé.

- [ ] Projet préparé·² localement.
- [ ] Variables configuré·²es.
- [ ] Dé.
- [ ] Domaine configuré·².
- [ ] SSL activé·².
- [ ] Site cré.
- [ ] Formulaire fonctionnel.
- [ ] E-mail configuré·².
- [ ] SEO vé.
- [ ] Tests effectué.
- [ ] Sauvegarde planifié·²e.
- [ ] Maintenance organisé.
