# 🛍️ E-Commerce Django — Déployé avec Docker & MySQL

Application e-commerce complète développée avec **Django**, connectée à **MySQL**, et déployée avec **Docker Compose**.

---

## 📋 Fonctionnalités

- 🛒 Catalogue de produits avec catégories et filtres
- ⭐ Produits vedettes et système d'avis / notation
- 🔍 Recherche et tri des produits
- 🛍️ Panier d'achat (session)
- ❤️ Liste de favoris (wishlist)
- 📦 Gestion des commandes (en attente, confirmée, expédiée, livrée)
- 🎟️ Codes promo / coupons de réduction
- 👤 Authentification (inscription, connexion, profil)
- 📧 Newsletter
- 🔧 Interface d'administration Django

---

## 🏗️ Architecture

```
Navigateur
    │
    ▼ http://localhost:8000
Conteneur Django (web)
    │
    ▼ MySQL HOST=db
Conteneur MySQL (db)
    │
    ▼
Volume Docker (db_data)
```

---

## 🚀 Technologies utilisées

| Technologie | Rôle |
|---|---|
| Django 5.x | Framework web backend |
| MySQL | Base de données |
| Docker & Docker Compose | Conteneurisation et déploiement |
| Gunicorn | Serveur WSGI |
| WhiteNoise | Fichiers statiques |
| Bootstrap 5 | Interface utilisateur |
| Font Awesome 6 | Icônes |

---

## 📁 Structure du projet

```
ecommerce/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .dockerignore
├── entrypoint.sh
├── ecommerce/          # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/           # App produits, commandes, panier
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── accounts/           # App authentification
│   ├── views.py
│   └── templates/
└── static/             # CSS, JS, Bootstrap
```

---

## ⚙️ Installation et lancement

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé et lancé

### 1. Cloner le projet

```bash
git clone https://github.com/TON_USERNAME/ecommerce-django-docker.git
cd ecommerce-django-docker/ecommerce
```

### 2. Créer le fichier `.env`

```env
DJANGO_SECRET_KEY=change-this-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=DB_ECOMMERCE
MYSQL_USER=django
MYSQL_PASSWORD=django
MYSQL_HOST=db
MYSQL_PORT=3306
```

### 3. Lancer les conteneurs

```bash
docker compose up -d --build
```

### 4. Créer un superutilisateur

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Accéder à l'application

| URL | Description |
|---|---|
| http://localhost:8000/products/ | Catalogue produits |
| http://localhost:8000/admin | Interface d'administration |

---

## 🛠️ Commandes utiles

```bash
# Voir l'état des conteneurs
docker compose ps

# Voir les logs Django
docker compose logs -f web

# Appliquer les migrations
docker compose exec web python manage.py migrate

# Redémarrer Django
docker compose restart web

# Arrêter les conteneurs
docker compose down
```

---

## 🗄️ Modèles de données

- **Product** — nom, prix, stock, image, catégorie, produit vedette
- **Category** — nom, description, image
- **Order / OrderItem** — commandes avec statut et articles
- **Review** — avis et notes (1 à 5 étoiles) par utilisateur
- **Wishlist** — favoris par utilisateur
- **Coupon** — codes promo avec pourcentage de réduction
- **Newsletter** — abonnements email

---

## 👨‍💻 Auteur

Développé dans le cadre du module **Développement Web avec Django** — EMI Rabat, année universitaire 2025–2026.
