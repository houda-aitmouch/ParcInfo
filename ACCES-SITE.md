# 🌐 Accès au Site ParcInfo - Déploiement Kubernetes

## ✅ Services Accessibles

### 🎯 **Interface Principale**
- **URL** : http://localhost:3000
- **Statut** : ✅ **FONCTIONNEL**
- **Description** : Interface utilisateur React principale
- **Accès** : Ouvrez votre navigateur et allez sur http://localhost:3000

### 📊 **Dashboard de Gestion**
- **URL** : http://localhost:8501
- **Statut** : ✅ **FONCTIONNEL**
- **Description** : Tableau de bord Streamlit pour la gestion
- **Accès** : Ouvrez votre navigateur et allez sur http://localhost:8501

## ⚠️ Services en Maintenance

### 🔧 **Backend Django**
- **URL** : http://localhost:8000
- **Statut** : 🔄 **En cours de correction**
- **Problème** : Script d'entrée attend sur `db:5432` au lieu de `postgres-service:5432`
- **Solution** : En cours de résolution

### 🤖 **Chatbot**
- **URL** : http://localhost:8001
- **Statut** : 🔄 **En cours de démarrage**
- **Problème** : Problème de ressources mémoire
- **Solution** : En cours de résolution

## 🚀 Comment Accéder au Site

### Méthode 1 : Via le Script Automatique
```bash
cd /Users/HouDa/PycharmProjects/ParcInfo
./access-site.sh
```

### Méthode 2 : Accès Direct
1. **Interface Principale** : http://localhost:3000
2. **Dashboard** : http://localhost:8501

### Méthode 3 : Port-Forward Manuel
```bash
# Frontend React
kubectl port-forward -n parcinfo service/frontend-service 3000:3000 &

# Dashboard Streamlit
kubectl port-forward -n parcinfo service/streamlit-service 8501:8501 &
```

## 📱 Applications Disponibles

| Application | URL | Statut | Description |
|-------------|-----|--------|-------------|
| **Frontend React** | http://localhost:3000 | ✅ Fonctionnel | Interface utilisateur principale |
| **Dashboard Streamlit** | http://localhost:8501 | ✅ Fonctionnel | Tableau de bord de gestion |
| **Backend Django** | http://localhost:8000 | 🔄 En cours | API et administration |
| **Chatbot** | http://localhost:8001 | 🔄 En cours | Assistant IA |

## 🔧 Commandes Utiles

### Vérifier l'état des services
```bash
kubectl get pods -n parcinfo
kubectl get services -n parcinfo
```

### Voir les logs
```bash
kubectl logs -f deployment/frontend -n parcinfo
kubectl logs -f deployment/streamlit -n parcinfo
```

### Redémarrer un service
```bash
kubectl rollout restart deployment/frontend -n parcinfo
kubectl rollout restart deployment/streamlit -n parcinfo
```

## 🎉 Résultat

**Votre site ParcInfo est accessible via Kubernetes !**

- ✅ **Frontend React** : Interface utilisateur complète
- ✅ **Dashboard Streamlit** : Outils de gestion
- 🔄 **Backend Django** : En cours de finalisation
- 🔄 **Chatbot** : En cours de démarrage

**Commencez par accéder à http://localhost:3000 pour l'interface principale !**
