# 🚀 Guide de Déploiement ParcInfo

## 📋 Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- Git
- Accès SSH au serveur de production

## 🔧 Configuration

### 1. Variables d'environnement

Copiez le fichier d'exemple et configurez vos variables :

```bash
cp env.production.example .env.production
```

Modifiez les valeurs dans `.env.production` :

- `SECRET_KEY` : Clé secrète Django (générez une nouvelle clé)
- `DATABASE_URL` : URL de connexion à la base de données
- `ALLOWED_HOSTS` : Domaines autorisés
- `EMAIL_*` : Configuration email (optionnel)

### 2. Secrets GitHub

Configurez les secrets suivants dans votre repository GitHub :

- `SSH_HOST` : Adresse IP du serveur de production
- `SSH_USER` : Nom d'utilisateur SSH
- `SSH_KEY` : Clé privée SSH

## 🐳 Déploiement avec Docker

### Déploiement local

```bash
# Cloner le repository
git clone https://github.com/votre-username/ParcInfo.git
cd ParcInfo

# Déploiement automatique
./deploy.sh
```

### Déploiement manuel

```bash
# Construction des images
docker-compose build

# Démarrage des services
docker-compose up -d

# Vérification du statut
docker-compose ps
```

## 🌐 Services

- **Backend Django** : http://localhost:8000
- **Frontend React** : http://localhost:3000
- **Chatbot** : http://localhost:8001
- **Application complète** : http://localhost (via Nginx)

## 🔄 CI/CD

Le déploiement automatique est configuré via GitHub Actions :

1. **Push sur main** → Déclenche le workflow
2. **Build des images** → Construction des conteneurs Docker
3. **Push vers GHCR** → Publication des images
4. **Déploiement SSH** → Mise à jour sur le serveur

## 📊 Monitoring

### Logs des services

```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f chatbot
```

### Statut des conteneurs

```bash
docker-compose ps
```

### Utilisation des ressources

```bash
docker stats
```

## 🔧 Maintenance

### Mise à jour

```bash
# Récupération des dernières modifications
git pull origin main

# Redéploiement
./deploy.sh
```

### Sauvegarde de la base de données

```bash
# Sauvegarde
docker-compose exec db pg_dump -U parcinfo parcinfo > backup.sql

# Restauration
docker-compose exec -T db psql -U parcinfo parcinfo < backup.sql
```

### Nettoyage

```bash
# Arrêt des services
docker-compose down

# Suppression des volumes
docker-compose down -v

# Nettoyage complet
docker system prune -a
```

## 🚨 Dépannage

### Problèmes courants

1. **Port déjà utilisé** : Vérifiez qu'aucun service n'utilise les ports 80, 8000, 3000, 8001
2. **Base de données non accessible** : Vérifiez que PostgreSQL est démarré
3. **Fichiers statiques manquants** : Exécutez `python manage.py collectstatic`

### Logs d'erreur

```bash
# Logs détaillés
docker-compose logs --tail=100 backend
```

## 📞 Support

Pour toute question ou problème :

1. Vérifiez les logs des services
2. Consultez la documentation Django
3. Ouvrez une issue sur GitHub

---

**Note** : Ce guide assume un déploiement sur un serveur Linux avec Docker installé.
