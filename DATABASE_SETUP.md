# ParcInfo - Configuration Base de Données

## 🚀 Démarrage Rapide

### Développement Local (avec PostgreSQL local)

```bash
# 1. Démarrer PostgreSQL localement
brew services start postgresql@14

# 2. Activer l'environnement virtuel
source rag_env/bin/activate

# 3. Démarrer le serveur Django
python manage.py runserver 127.0.0.1:9000
```

### Développement avec Docker (avec PostgreSQL dans Docker)

```bash
# Utiliser le script automatisé
./docker-start.sh

# Ou manuellement :
docker-compose up --build -d
docker-compose exec web python manage.py migrate
```

## 📊 Configuration Base de Données

### Local (.env)
- **Host**: localhost
- **User**: Houda
- **Password**: (vide)
- **Database**: parcinfo_db

### Docker (.env.docker)
- **Host**: db (nom du service Docker)
- **User**: parcinfo_user
- **Password**: parcinfo_password
- **Database**: parcinfo_db

## 🔧 Commandes Utiles

```bash
# Voir les logs Docker
docker-compose logs -f

# Arrêter Docker
docker-compose down

# Accéder au shell du conteneur web
docker-compose exec web bash

# Accéder à PostgreSQL dans Docker
docker-compose exec db psql -U parcinfo_user -d parcinfo_db
```

## 🌐 URLs

- **Local**: http://127.0.0.1:9000
- **Docker**: http://localhost:8000
- **PostgreSQL Docker**: localhost:5432
