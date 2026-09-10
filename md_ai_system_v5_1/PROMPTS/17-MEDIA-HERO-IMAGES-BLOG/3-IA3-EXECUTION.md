# MEDIA / HERO / IMAGES / BLOG

ÉTAPE: `3-IA3-EXECUTION.md`
CATÉGORIE: `17-MEDIA-HERO-IMAGES-BLOG`

PÉRIMÈTRE
Audit média obligatoire de TOUTES les pages. Pour chaque page, décider si le hero utilise vidéo, image, SVG, motion, 3D, composition CSS ou aucun média. Homepage : étudier en priorité un hero vidéo plein écran. Couvrir vidéo desktop + mobile, poster, WebM + MP4 si pertinent, autoplay uniquement muted, playsinline, loop seulement si mesure valide, reduced-motion, save-data/réseau lent, responsive, LCP/CLS/poids, contraste texte/média mesuré, droits/licences, ALT pour images utiles. Interdire image générique répétée partout sans justification et toute fausse preuve commerciale.

Pour CHAQUE PAGE documenter exactement :
PAGE
TYPE DE HERO
MEDIA UTILISÉ
FICHIER
DESKTOP
MOBILE
FALLBACK
ALT
POIDS
LCP
CLS
DROITS
STATUT

BLOG : couverture spécifique par article ; jamais la même image pour tous ; version desktop, mobile et social/OG ; cohérence artistique globale ; luminance/contraste ; compression ; ALT ; droits ; association article → média enregistrée dans le manifest.

Créer/maintenir : `MEDIA-MANIFEST.md`, `HERO-VIDEO-RULES.md`, `MOTION-LIBRARIES.md`. IA4 verrouille le résultat dans SOURCE OF TRUTH.

DÉPENDANCES RÉELLES
12-DESIGN-SYSTEM-BRAND, 16-CONTENT-BLOG

PROJECT_PROFILES CONCERNÉS
all

LECTURES SYSTÈME OBLIGATOIRES — à lire directement dans le workspace VS Code
- `TEMPLATES/STAGES/3-IA3-EXECUTION.md`
- `COMMON-RULES.md`
- `TEMPLATES/GIT-INJECTION-TEMPLATE.md`
- `WORKFLOW-RULES.md`
- `SOURCE-OF-TRUTH-RULES.md`
- `POLICY-PROFILES.md`
- `NEXT-PROMPT-RULES.md`
- `.md-ai-system/state/17-MEDIA-HERO-IMAGES-BLOG.json`
- `.md-ai-system/STATE.json`

GIT CRITIQUE
Appliquer obligatoirement `TEMPLATES/GIT-INJECTION-TEMPLATE.md`. Les règles complètes ne sont pas dupliquées ici.

ORDRE
L'ordre de lecture n'est pas l'ordre des dépendances. Utiliser `EXECUTION-MATRIX.md` et `DEPENDENCY-GRAPH.json`.

PROCHAIN PROMPT
À la fin, appliquer `NEXT-PROMPT-RULES.md`, proposer le prochain prompt logique, puis lire soi-même le fichier correspondant dans le workspace VS Code pour vérifier qu'il existe. Ne pas demander à l'utilisateur de copier son contenu.
