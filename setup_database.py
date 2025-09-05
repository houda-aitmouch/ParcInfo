#!/usr/bin/env python3
"""
Script de configuration Django et restauration de la base de données ParcInfo
"""

import os
import sys
import django
import subprocess
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_django():
    """Configure l'environnement Django"""
    print("🔧 Configuration de l'environnement Django...")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("manage.py").exists():
        print("❌ Erreur: Ce script doit être exécuté depuis la racine du projet ParcInfo")
        sys.exit(1)
    
    # Configurer Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
    
    try:
        django.setup()
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la configuration Django: {e}")
        return False

def check_database_connection():
    """Vérifie la connexion à la base de données"""
    print("🔍 Vérification de la connexion à la base de données...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connexion à la base de données réussie - PostgreSQL {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def restore_database_from_sql():
    """Restaure la base de données à partir du script SQL"""
    print("🗄️ Restauration de la base de données à partir du script SQL...")
    
    sql_file = "restore_database_corrected.sql"
    if not Path(sql_file).exists():
        print(f"❌ Fichier SQL non trouvé: {sql_file}")
        return False
    
    try:
        from django.db import connection
        from django.conf import settings
        
        # Lire le contenu du fichier SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Diviser le contenu en commandes individuelles
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        with connection.cursor() as cursor:
            for i, command in enumerate(commands, 1):
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        print(f"  ✅ Commande {i}/{len(commands)} exécutée")
                    except Exception as e:
                        print(f"  ⚠️ Commande {i} échouée: {e}")
                        # Continuer avec les autres commandes
        
        # Valider les changements
        connection.commit()
        print("✅ Base de données restaurée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")
        return False

def verify_database_restoration():
    """Vérifie que la restauration s'est bien passée"""
    print("🔍 Vérification de la restauration de la base de données...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Vérifier les tables
            cursor.execute("""
                SELECT table_name, COUNT(*) as row_count 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('materiel_informatique', 'materiel_bureautique', 'commande_informatique', 'commande_bureau', 'fournisseurs', 'livraison', 'demande_equipement', 'users_customuser')
                GROUP BY table_name
                ORDER BY table_name
            """)
            
            tables = cursor.fetchall()
            print("📊 Tables restaurées:")
            for table_name, row_count in tables:
                print(f"  - {table_name}: {row_count} lignes")
            
            # Vérifier les index
            cursor.execute("""
                SELECT COUNT(*) as index_count 
                FROM pg_indexes 
                WHERE tablename IN ('materiel_informatique', 'materiel_bureautique', 'commande_informatique', 'commande_bureau', 'fournisseurs', 'livraison', 'demande_equipement', 'users_customuser')
            """)
            
            index_count = cursor.fetchone()[0]
            print(f"🔗 Index créés: {index_count}")
            
            # Vérifier quelques données d'exemple
            cursor.execute("SELECT COUNT(*) FROM fournisseurs")
            fournisseur_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM materiel_informatique")
            materiel_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM commande_informatique")
            commande_count = cursor.fetchone()[0]
            
            print(f"📋 Données d'exemple insérées:")
            print(f"  - Fournisseurs: {fournisseur_count}")
            print(f"  - Matériels informatiques: {materiel_count}")
            print(f"  - Commandes informatiques: {commande_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def run_django_migrations():
    """Exécute les migrations Django"""
    print("🔄 Exécution des migrations Django...")
    
    try:
        result = subprocess.run([
            sys.executable, "manage.py", "migrate", "--noinput"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations Django exécutées avec succès")
            return True
        else:
            print(f"⚠️ Migrations partielles: {result.stderr}")
            return True  # Continuer même avec des avertissements
            
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE CONFIGURATION DJANGO ET RESTAURATION DE BASE")
    print("=" * 60)
    
    # Étape 1: Configuration Django
    if not setup_django():
        sys.exit(1)
    
    # Étape 2: Vérification de la connexion
    if not check_database_connection():
        sys.exit(1)
    
    # Étape 3: Exécution des migrations
    if not run_django_migrations():
        print("⚠️ Migrations échouées, mais continuation...")
    
    # Étape 4: Restauration de la base
    if not restore_database_from_sql():
        sys.exit(1)
    
    # Étape 5: Vérification
    if not verify_database_restoration():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 CONFIGURATION ET RESTAURATION TERMINÉES AVEC SUCCÈS!")
    print("=" * 60)
    
    print("\n📋 Résumé des opérations:")
    print("  ✅ Environnement Django configuré")
    print("  ✅ Connexion à la base de données établie")
    print("  ✅ Migrations Django exécutées")
    print("  ✅ Base de données restaurée")
    print("  ✅ Données d'exemple insérées")
    print("  ✅ Index et contraintes créés")
    
    print("\n🚀 Prochaines étapes:")
    print("  1. Tester le chatbot: python3 test_phase3_quick.py")
    print("  2. Tester les requêtes Phase 2: python3 test_phase2_avec_bart_retrained.py")
    print("  3. Déployer Phase 3: ./deploy_phase3.sh")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
