# ParcInfo - Gestion de Parc Informatique (Version Docker Corrigée)

## 🚀 Démarrage Rapide

### Prérequis
- Docker et Docker Compose installés
- Ports 80, 3000, 8000, 8001, 8501 disponibles

### Démarrage Automatique
```bash
# Démarrage complet avec nettoyage
./start-docker-complete.sh

# Ou démarrage simple
docker-compose up -d
```

### Test des Services
```bash
# Tester que tous les services fonctionnent
./test-docker-services.sh
```

## 🏗️ Architecture des Services

### Services Docker
1. **PostgreSQL Database** (`db`)
   - Port: 5432
   - Base: `parcinfo_db`
   - Utilisateur: `Houda`
   - Mot de passe: `houda123`

2. **Backend Django** (`backend`)
   - Port: 8000
   - URL: http://localhost:8000
   - Gestion des API et logique métier

3. **Frontend React** (`frontend`)
   - Port: 3000
   - URL: http://localhost:3000
   - Interface utilisateur moderne

4. **Chatbot Service** (`chatbot`)
   - Port: 8001
   - URL: http://localhost:8001
   - Service d'IA pour assistance

5. **Streamlit Dashboard** (`streamlit`)
   - Port: 8501
   - URL: http://localhost:8501
   - Tableaux de bord et analytics

6. **Nginx Proxy** (`nginx`)
   - Port: 80
   - URL: http://localhost:80
   - Reverse proxy et gestion des fichiers statiques

## 🔧 Corrections Apportées

### 1. Configuration Base de Données
- ✅ HOST par défaut corrigé de `host.docker.internal` vers `db`
- ✅ Configuration PostgreSQL optimisée
- ✅ Health checks ajoutés

### 2. Dockerfile Frontend
- ✅ Correction du chemin de build React (`/app/dist/` au lieu de `/app/../static/react/`)
- ✅ Configuration Nginx améliorée
- ✅ Gestion des fichiers statiques Django et React

### 3. Dockerfile Backend
- ✅ Dépendances système complètes (gcc, g++, make)
- ✅ Script de démarrage robuste
- ✅ Gestion des migrations automatique

### 4. Dockerfile Chatbot
- ✅ Script de démarrage dédié
- ✅ Gestion des dépendances IA
- ✅ Configuration optimisée

### 5. Dockerfile Streamlit
- ✅ Dépendances système complètes
- ✅ Script de démarrage dédié
- ✅ Configuration Streamlit optimisée

### 6. Configuration Nginx
- ✅ Proxy correct vers tous les services
- ✅ Gestion des fichiers statiques
- ✅ Headers de sécurité

## 📋 Commandes Utiles

### Gestion des Services
```bash
# Voir le statut
docker-compose ps

# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart <service_name>

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

### Accès aux Conteneurs
```bash
# Accéder au backend
docker-compose exec backend bash

# Accéder à la base de données
docker-compose exec db psql -U Houda -d parcinfo_db

# Voir les logs d'un service spécifique
docker-compose logs -f backend
```

### Maintenance
```bash
# Nettoyer les images inutilisées
docker system prune -f

# Reconstruire une image
docker-compose build --no-cache <service_name>

# Voir l'utilisation des ressources
docker stats
```

## 🐛 Dépannage

### Problèmes Courants

1. **Erreur de connexion à la base de données**
   ```bash
   # Vérifier que PostgreSQL est démarré
   docker-compose logs db
   
   # Redémarrer la base de données
   docker-compose restart db
   ```

2. **Erreur de build du frontend**
   ```bash
   # Nettoyer et reconstruire
   docker-compose build --no-cache frontend
   ```

3. **Ports déjà utilisés**
   ```bash
   # Vérifier les ports utilisés
   lsof -i :80 -i :3000 -i :8000 -i :8001 -i :8501
   
   # Arrêter les processus qui utilisent les ports
   sudo kill -9 <PID>
   ```

4. **Problèmes de permissions**
   ```bash
   # Donner les permissions d'exécution
   chmod +x *.sh
   ```

### Logs Détaillés
```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs backend
docker-compose logs frontend
docker-compose logs chatbot
docker-compose logs streamlit
docker-compose logs nginx
docker-compose logs db
```

## 🌐 URLs d'Accès

- **Application principale**: http://localhost:80
- **Backend API**: http://localhost:8000
- **Frontend React**: http://localhost:3000
- **Chatbot**: http://localhost:8001
- **Dashboard Streamlit**: http://localhost:8501

## 📝 Notes Importantes

1. **Premier démarrage**: Le premier démarrage peut prendre 5-10 minutes pour télécharger et construire les images
2. **Base de données**: Les données sont persistantes dans le volume Docker `postgres_data`
3. **Fichiers statiques**: Servis par le service frontend via Nginx
4. **Migrations**: Exécutées automatiquement au démarrage
5. **Cache**: Les modèles IA sont mis en cache dans `~/.cache/huggingface`

## 🔄 Mise à Jour

```bash
# Arrêter les services
docker-compose down

# Mettre à jour le code
git pull

# Reconstruire et redémarrer
docker-compose up -d --build
```

## 📞 Support

En cas de problème, vérifiez :
1. Les logs des services
2. La configuration des ports
3. L'état des conteneurs
4. La connectivité réseau

Utilisez `./test-docker-services.sh` pour un diagnostic automatique.
