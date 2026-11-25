# World Picker — Apprendre mes pays

Jeu de géographie HTML5 autonome, en français. Ouvrir `index.html` dans un navigateur suffit; aucun serveur ni dépendance externe.

## Publication

1. Créer le dépôt public `Unschoolers/world-picker`, avec `main` comme branche principale.
2. Envoyer les fichiers de ce dossier à la racine du dépôt (y compris `.github/workflows/pages.yml`).
3. Dans Settings → Pages, sélectionner GitHub Actions comme source.
4. Dans Actions → Validate and publish, lancer Run workflow si le premier déploiement a précédé l'activation de Pages.

Les modifications sur `main` sont ensuite validées et publiées automatiquement. Les pull requests sont validées sans publication.

Adresse prévue : https://unschoolers.github.io/world-picker/

## Validation locale

Avec Python 3 et Node.js installés : `python3 scripts/check.py`. Ce contrôle vérifie le point d'entrée et la syntaxe JavaScript; ce n'est pas un test fonctionnel dans un navigateur.

## Installation et mode hors ligne

Ouvrir le site dans Chrome sur Android, puis utiliser Installer ou le menu du navigateur. Sur iOS, utiliser Safari → Partager → Sur l’écran d’accueil. Le manifest et le service worker permettent une ouverture autonome et le jeu hors ligne après la mise en cache initiale. Le workflow versionne le cache à chaque déploiement. Pour tester la PWA en local : `python3 -m http.server 8000`, puis ouvrir `http://localhost:8000/`.
