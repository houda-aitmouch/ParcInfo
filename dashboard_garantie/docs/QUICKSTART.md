# 🚀 Démarrage Rapide - Dashboard Garantie

## ⚡ Installation Express (5 minutes)

### 1. Installation des dépendances
```bash
./install_dependencies.sh
```

### 2. Test de la configuration
```bash
python test_dashboard.py
```

### 3. Lancement du dashboard
```bash
./launch_dashboard.sh
```

## 🎯 Fonctionnalités Clés

- **🔐 Authentification** : Utilise les utilisateurs Django existants
- **👥 Gestion des rôles** : Accès différencié selon les permissions
- **📊 Visualisations** : Graphiques et métriques en temps réel
- **🚨 Alertes** : Notifications pour les garanties expirant bientôt

## 🔑 Identifiants de Test

- **Super Admin** : `superadmin` / `superadmin123`
- **Gestionnaire Informatique** : Créez un utilisateur et assignez-le au groupe
- **Gestionnaire Bureau** : Créez un utilisateur et assignez-le au groupe

## 📱 Accès au Dashboard

Une fois lancé, le dashboard est accessible à :
```
http://localhost:8501
```

## 🧪 Données de Test

Pour tester avec des données d'exemple :
```bash
python demo_data.py          # Créer des données de test
python demo_data.py --cleanup # Supprimer les données de test
```

## 🆘 En cas de problème

1. **Vérifiez la configuration** : `python test_dashboard.py`
2. **Consultez le README** : `README_DASHBOARD.md`
3. **Vérifiez les logs** : Messages d'erreur dans le terminal

## 📋 Checklist de Vérification

- [ ] Python 3.8+ installé
- [ ] Base de données Django accessible
- [ ] Permissions configurées (`python manage.py setup_permissions`)
- [ ] Dépendances installées
- [ ] Dashboard accessible sur http://localhost:8501

## 🎉 C'est parti !

Votre dashboard est maintenant prêt à être utilisé ! 🎊
