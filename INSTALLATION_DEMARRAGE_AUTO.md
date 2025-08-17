# 🚀 Configuration du Démarrage Automatique - ParcInfo

Ce guide explique comment configurer le démarrage automatique de Django et Streamlit.

## 📋 Méthodes Disponibles

### 🎯 Méthode 1 : Lancement Manuel (Recommandé pour le développement)

```bash
# Dans le répertoire du projet
./launch_project.sh
```

### 🎯 Méthode 2 : Alias de Commande

Après avoir ajouté l'alias, vous pouvez simplement taper :
```bash
parcinfo
```

### 🎯 Méthode 3 : Démarrage Automatique au Démarrage du Système

#### Sur macOS :

1. **Copier le fichier plist** :
```bash
cp com.parcinfo.startup.plist ~/Library/LaunchAgents/
```

2. **Charger le service** :
```bash
launchctl load ~/Library/LaunchAgents/com.parcinfo.startup.plist
```

3. **Démarrer le service** :
```bash
launchctl start com.parcinfo.startup
```

#### Sur Linux :

1. **Créer un service systemd** :
```bash
sudo cp startup_parcinfo.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/startup_parcinfo.sh
```

2. **Créer le fichier service** :
```bash
sudo tee /etc/systemd/system/parcinfo.service << EOF
[Unit]
Description=ParcInfo Django and Streamlit
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/Users/HouDa/PycharmProjects/ParcInfo
ExecStart=/usr/local/bin/startup_parcinfo.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

3. **Activer et démarrer le service** :
```bash
sudo systemctl enable parcinfo.service
sudo systemctl start parcinfo.service
```

#### Sur Windows :

1. **Créer un raccourci** vers `launch_project.bat`
2. **Placer le raccourci** dans `C:\Users\[USERNAME]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

## 🔧 Gestion des Services

### macOS
```bash
# Arrêter le service
launchctl stop com.parcinfo.startup

# Désactiver le service
launchctl unload ~/Library/LaunchAgents/com.parcinfo.startup.plist

# Vérifier le statut
launchctl list | grep parcinfo
```

### Linux
```bash
# Arrêter le service
sudo systemctl stop parcinfo.service

# Désactiver le service
sudo systemctl disable parcinfo.service

# Vérifier le statut
sudo systemctl status parcinfo.service
```

## 📊 Vérification

Après configuration, vérifiez que les services fonctionnent :

```bash
# Vérifier Django
curl -I http://localhost:8000

# Vérifier Streamlit
curl -I http://localhost:8501
```

## 🛠️ Dépannage

### Logs sur macOS
```bash
# Voir les logs
tail -f /tmp/parcinfo.log
tail -f /tmp/parcinfo_error.log
```

### Logs sur Linux
```bash
# Voir les logs
sudo journalctl -u parcinfo.service -f
```

## ⚠️ Notes Importantes

- Les services démarrent automatiquement au démarrage du système
- Les ports 8000 et 8501 doivent être disponibles
- Le projet doit être dans le répertoire spécifié
- Les dépendances Python doivent être installées

## 🎉 Avantages

- ✅ Démarrage automatique au boot
- ✅ Redémarrage automatique en cas de crash
- ✅ Gestion des logs
- ✅ Configuration système native
