#!/usr/bin/env python3
"""
Script simple de restauration de la base de données ParcInfo
Exécute les étapes dans l'ordre correct
"""
import os
import sys
import django
import psycopg2
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

def restore_database():
    """Restaure la base de données étape par étape"""
    print("🗄️ Restauration de la base de données ParcInfo...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Étape 1: Créer les tables
            print("📋 Étape 1: Création des tables...")
            
            # Table fournisseurs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fournisseurs (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(200) NOT NULL,
                    ice VARCHAR(50) UNIQUE,
                    adresse TEXT,
                    telephone VARCHAR(20),
                    email VARCHAR(100),
                    contact_principal VARCHAR(100),
                    statut VARCHAR(50) DEFAULT 'actif',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table fournisseurs créée")
            
            # Table users_customuser
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_customuser (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(150) UNIQUE NOT NULL,
                    email VARCHAR(254) UNIQUE NOT NULL,
                    first_name VARCHAR(150),
                    last_name VARCHAR(150),
                    role VARCHAR(50) DEFAULT 'utilisateur',
                    departement VARCHAR(100),
                    date_embauche DATE,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_staff BOOLEAN DEFAULT FALSE,
                    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table users_customuser créée")
            
            # Table commande_informatique
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commande_informatique (
                    id SERIAL PRIMARY KEY,
                    numero_commande VARCHAR(50) UNIQUE NOT NULL,
                    date_commande DATE NOT NULL,
                    date_livraison_prevue DATE,
                    date_livraison_effective DATE,
                    montant_total DECIMAL(10,2),
                    statut VARCHAR(50) DEFAULT 'en_cours',
                    fournisseur_id INTEGER NOT NULL,
                    utilisateur_id INTEGER,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table commande_informatique créée")
            
            # Table commande_bureau
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commande_bureau (
                    id SERIAL PRIMARY KEY,
                    numero_commande VARCHAR(50) UNIQUE NOT NULL,
                    date_commande DATE NOT NULL,
                    date_livraison_prevue DATE,
                    date_livraison_effective DATE,
                    montant_total DECIMAL(10,2),
                    statut VARCHAR(50) DEFAULT 'en_cours',
                    fournisseur_id INTEGER NOT NULL,
                    utilisateur_id INTEGER,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table commande_bureau créée")
            
            # Table materiel_informatique
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materiel_informatique (
                    id SERIAL PRIMARY KEY,
                    code_inventaire VARCHAR(50) UNIQUE NOT NULL,
                    designation VARCHAR(200) NOT NULL,
                    marque VARCHAR(100),
                    modele VARCHAR(100),
                    date_acquisition DATE,
                    prix_acquisition DECIMAL(10,2),
                    garantie_until DATE,
                    statut VARCHAR(50) DEFAULT 'actif',
                    localisation VARCHAR(100),
                    commande_id INTEGER,
                    fournisseur_id INTEGER,
                    utilisateur_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table materiel_informatique créée")
            
            # Table materiel_bureautique
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materiel_bureautique (
                    id SERIAL PRIMARY KEY,
                    code_inventaire VARCHAR(50) UNIQUE NOT NULL,
                    designation VARCHAR(200) NOT NULL,
                    marque VARCHAR(100),
                    modele VARCHAR(100),
                    date_acquisition DATE,
                    prix_acquisition DECIMAL(10,2),
                    garantie_until DATE,
                    statut VARCHAR(50) DEFAULT 'actif',
                    localisation VARCHAR(100),
                    commande_id INTEGER,
                    fournisseur_id INTEGER,
                    utilisateur_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table materiel_bureautique créée")
            
            # Table livraison
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livraison (
                    id SERIAL PRIMARY KEY,
                    commande_id INTEGER NOT NULL,
                    date_prevue DATE NOT NULL,
                    date_effective DATE,
                    statut VARCHAR(50) DEFAULT 'en_attente',
                    transporteur VARCHAR(100),
                    numero_suivi VARCHAR(100),
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table livraison créée")
            
            # Table demande_equipement
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS demande_equipement (
                    id SERIAL PRIMARY KEY,
                    utilisateur_id INTEGER NOT NULL,
                    type_equipement VARCHAR(100) NOT NULL,
                    description TEXT,
                    priorite VARCHAR(20) DEFAULT 'normale',
                    statut VARCHAR(50) DEFAULT 'en_attente',
                    date_demande DATE DEFAULT CURRENT_DATE,
                    date_approbation DATE,
                    date_reception DATE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("  ✅ Table demande_equipement créée")
            
            # Étape 2: Insérer les données
            print("\n📊 Étape 2: Insertion des données...")
            
            # Fournisseurs
            cursor.execute("""
                INSERT INTO fournisseurs (nom, ice, adresse, telephone, email, contact_principal) VALUES
                ('COHESIUM ICE', '001234567890123', '123 Rue Hassan II, Casablanca', '+212-5-22-123456', 'contact@cohesium.ma', 'Ahmed Benali'),
                ('TECHNOLOGIE PLUS SARL', '001234567890124', '456 Avenue Mohammed V, Rabat', '+212-5-37-123456', 'info@techplus.ma', 'Fatima Zahra'),
                ('INFORMATIQUE EXPRESS', '001234567890125', '789 Boulevard Al Massira, Marrakech', '+212-5-24-123456', 'contact@infoxpress.ma', 'Karim El Amrani'),
                ('DIGITAL SOLUTIONS', '001234567890126', '321 Rue Ibn Batouta, Tanger', '+212-5-39-123456', 'hello@digitalsolutions.ma', 'Sara Bennani'),
                ('SMART TECH ICE', '001234567890127', '654 Avenue Hassan I, Fès', '+212-5-35-123456', 'info@smarttech.ma', 'Omar Tazi')
                ON CONFLICT (ice) DO NOTHING
            """)
            print("  ✅ Fournisseurs insérés")
            
            # Utilisateurs
            cursor.execute("""
                INSERT INTO users_customuser (username, email, first_name, last_name, is_staff, is_active, is_superuser, password, date_joined) VALUES
                ('admin', 'admin@parcinfo.ma', 'Administrateur', 'Système', TRUE, TRUE, TRUE, 'pbkdf2_sha256$600000$test123$hash', CURRENT_TIMESTAMP),
                ('gestionnaire_bureau', 'bureau@parcinfo.ma', 'Gestionnaire', 'Bureau', FALSE, TRUE, FALSE, 'pbkdf2_sha256$600000$test123$hash', CURRENT_TIMESTAMP),
                ('utilisateur1', 'user1@parcinfo.ma', 'Utilisateur', 'Test', FALSE, TRUE, FALSE, 'pbkdf2_sha256$600000$test123$hash', CURRENT_TIMESTAMP),
                ('technicien', 'tech@parcinfo.ma', 'Technicien', 'Support', FALSE, TRUE, FALSE, 'pbkdf2_sha256$600000$test123$hash', CURRENT_TIMESTAMP),
                ('manager', 'manager@parcinfo.ma', 'Manager', 'Projet', FALSE, TRUE, FALSE, 'pbkdf2_sha256$600000$test123$hash', CURRENT_TIMESTAMP)
                ON CONFLICT (username) DO NOTHING
            """)
            print("  ✅ Utilisateurs insérés")
            
            # Commandes informatiques
            cursor.execute("""
                INSERT INTO commande_informatique (numero_commande, date_commande, date_livraison_prevue, date_livraison_effective, montant_total, statut, fournisseur_id, utilisateur_id) VALUES
                ('BC23', '2025-08-15', '2025-08-20', '2025-08-20', 15000.00, 'livree', 1, 1),
                ('BC24', '2025-08-18', '2025-08-25', '2025-08-22', 8500.00, 'livree', 2, 2),
                ('BC25', '2025-08-20', '2025-08-30', NULL, 12000.00, 'en_cours', 3, 3),
                ('BC26', '2025-08-22', '2025-09-01', NULL, 9500.00, 'en_cours', 4, 4),
                ('BC27', '2025-08-25', '2025-09-05', NULL, 18000.00, 'en_cours', 5, 5)
                ON CONFLICT (numero_commande) DO NOTHING
            """)
            print("  ✅ Commandes informatiques insérées")
            
            # Étape 3: Créer les index
            print("\n🔗 Étape 3: Création des index...")
            
            # Index essentiels
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_materiel_code_inventaire ON materiel_informatique(code_inventaire)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_commande_numero ON commande_informatique(numero_commande)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_fournisseur_ice ON fournisseurs(ice)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_username ON users_customuser(username)")
            
            print("  ✅ Index créés")
            
            # Valider les changements
            connection.commit()
            print("\n✅ Base de données restaurée avec succès!")
            
            # Vérification finale
            print("\n🔍 Vérification finale...")
            cursor.execute("SELECT COUNT(*) FROM fournisseurs")
            fournisseur_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users_customuser")
            user_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM commande_informatique")
            commande_count = cursor.fetchone()[0]
            
            print(f"  📊 Fournisseurs: {fournisseur_count}")
            print(f"  📊 Utilisateurs: {user_count}")
            print(f"  📊 Commandes: {commande_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")
        return False

if __name__ == "__main__":
    success = restore_database()
    sys.exit(0 if success else 1)
