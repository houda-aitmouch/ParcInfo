# 📚 Système d'Archivage Automatique des Décharges

## 🎯 Objectif

Le système d'archivage automatique permet de :
- **Archiver automatiquement** toutes les décharges signées
- **Maintenir une trace électronique** de toutes les décharges
- **Faciliter la recherche** et la consultation des archives
- **Assurer la conformité** avec les exigences de traçabilité

## 🔧 Fonctionnement

### 1. Archivage Automatique lors de la Signature
- Quand un utilisateur signe sa décharge, elle est **automatiquement archivée**
- Le PDF de la décharge est généré et stocké dans les archives
- Un numéro d'archive unique est attribué (format: `ARCH-YYYYMMDD-XXXX`)

### 2. Archivage des Demandes Existantes
- Les demandes signées qui n'ont pas encore été archivées peuvent être archivées manuellement
- Utilisez la commande Django pour archiver toutes les demandes en attente

## 🛠️ Commandes Disponibles

### Archivage Manuel
```bash
# Voir ce qui serait archivé (sans effectuer l'archivage)
python manage.py archiver_demandes_signees --dry-run

# Archiver toutes les demandes signées non archivées
python manage.py archiver_demandes_signees

# Archiver avec un utilisateur spécifique
python manage.py archiver_demandes_signees --user=superadmin
```

### Script d'Archivage Automatique
```bash
# Exécuter le script d'archivage automatique
python scripts/archivage_automatique.py
```

## 📅 Planification Automatique

### Avec Cron (Linux/Mac)
```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour exécuter l'archivage tous les jours à 2h du matin
0 2 * * * cd /chemin/vers/ParcInfo && python scripts/archivage_automatique.py >> logs/archivage.log 2>&1
```

### Avec Task Scheduler (Windows)
1. Ouvrir "Planificateur de tâches"
2. Créer une nouvelle tâche
3. Programmer l'exécution quotidienne
4. Action : exécuter `python scripts/archivage_automatique.py`

## 📊 Structure des Archives

### Modèle ArchiveDecharge
- **demande** : Lien vers la demande d'équipement
- **fichier_pdf** : Fichier PDF de la décharge archivée
- **numero_archive** : Numéro unique d'archive (auto-généré)
- **date_archivage** : Date et heure de l'archivage
- **archive_par** : Utilisateur qui a effectué l'archivage
- **statut_archive** : Statut de l'archive (actif/inactif/supprimé)
- **notes** : Notes d'archivage

### Numérotation des Archives
Format : `ARCH-YYYYMMDD-XXXX`
- **ARCH** : Préfixe fixe
- **YYYYMMDD** : Date de création (année-mois-jour)
- **XXXX** : Numéro séquentiel sur 4 chiffres

## 🔍 Consultation des Archives

### Interface Web
- **URL** : `/demandes/archives/`
- **Accès** : Tous les utilisateurs autorisés
- **Fonctionnalités** :
  - Recherche par nom ou numéro d'archive
  - Filtrage par catégorie et type
  - Pagination des résultats
  - Téléchargement des PDF

### Permissions
- **Super Admin** : Accès à toutes les archives
- **Gestionnaire Informatique** : Archives informatiques uniquement
- **Gestionnaire Bureau** : Archives bureau uniquement

## 📁 Organisation des Fichiers

```
ParcInfo/
├── media/
│   └── archives/
│       └── decharges/          # PDFs des décharges archivées
├── scripts/
│   └── archivage_automatique.py  # Script d'archivage automatique
└── apps/demande_equipement/
    └── management/
        └── commands/
            └── archiver_demandes_signees.py  # Commande Django
```

## 🚨 Gestion des Erreurs

### Logs d'Archivage
- Les erreurs sont loggées dans la console
- Pour la production, rediriger vers un fichier de log
- Surveiller régulièrement les logs pour détecter les problèmes

### Erreurs Courantes
1. **Fichier PDF manquant** : Vérifier la génération du PDF
2. **Permissions insuffisantes** : Vérifier les droits d'écriture
3. **Espace disque insuffisant** : Surveiller l'espace disponible

## 🔄 Maintenance

### Nettoyage des Archives
- Supprimer les archives obsolètes si nécessaire
- Compresser les anciens fichiers PDF
- Sauvegarder régulièrement les archives

### Surveillance
- Vérifier quotidiennement que l'archivage s'exécute
- Surveiller l'espace disque utilisé
- Contrôler l'intégrité des fichiers PDF

## 📞 Support

En cas de problème avec l'archivage :
1. Vérifier les logs d'erreur
2. Tester la commande manuellement
3. Contrôler les permissions et l'espace disque
4. Contacter l'administrateur système 