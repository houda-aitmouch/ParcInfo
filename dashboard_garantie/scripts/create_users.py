#!/usr/bin/env python3
"""
Script de création d'utilisateurs pour le Dashboard Garantie ParcInfo
Crée des utilisateurs avec différents rôles pour tester le dashboard
"""

import os
import sys
import django
from django.contrib.auth.models import Group, User

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

def create_users():
    """Crée des utilisateurs avec différents rôles"""
    print("👥 Création des utilisateurs pour le Dashboard Garantie")
    print("=" * 60)
    
    # Définir les utilisateurs à créer
    users_data = [
        {
            'username': 'gest_info',
            'email': 'gest.info@parcinfo.com',
            'password': 'gestinfo123',
            'first_name': 'Gestionnaire',
            'last_name': 'Informatique',
            'group': 'Gestionnaire Informatique',
            'description': 'Gestionnaire des commandes informatiques'
        },
        {
            'username': 'gest_bureau',
            'email': 'gest.bureau@parcinfo.com',
            'password': 'gestbureau123',
            'first_name': 'Gestionnaire',
            'last_name': 'Bureau',
            'group': 'Gestionnaire Bureau',
            'description': 'Gestionnaire des commandes bureautiques'
        },
        {
            'username': 'employe1',
            'email': 'employe1@parcinfo.com',
            'password': 'employe123',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'group': 'Employe',
            'description': 'Employé avec accès en lecture seule'
        },
        {
            'username': 'employe2',
            'email': 'employe2@parcinfo.com',
            'password': 'employe123',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'group': 'Employe',
            'description': 'Employé avec accès en lecture seule'
        },
        {
            'username': 'admin_garantie',
            'email': 'admin.garantie@parcinfo.com',
            'password': 'admingarantie123',
            'first_name': 'Admin',
            'last_name': 'Garantie',
            'group': 'Super Admin',
            'description': 'Administrateur spécialisé garantie'
        }
    ]
    
    created_users = []
    existing_users = []
    
    for user_data in users_data:
        username = user_data['username']
        
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            print(f"⚠️ Utilisateur {username} existe déjà")
            existing_users.append(user_data)
            continue
        
        try:
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=True,
                is_superuser=(user_data['group'] == 'Super Admin')
            )
            
            # Ajouter l'utilisateur au groupe approprié
            try:
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)
                print(f"✅ Utilisateur créé: {username} ({user_data['description']})")
                print(f"   - Groupe: {user_data['group']}")
                print(f"   - Mot de passe: {user_data['password']}")
                created_users.append(user_data)
            except Group.DoesNotExist:
                print(f"❌ Groupe '{user_data['group']}' non trouvé pour {username}")
                user.delete()
                
        except Exception as e:
            print(f"❌ Erreur lors de la création de {username}: {e}")
    
    # Résumé
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DE LA CRÉATION D'UTILISATEURS")
    print("=" * 60)
    
    print(f"✅ {len(created_users)} utilisateur(s) créé(s)")
    print(f"⚠️ {len(existing_users)} utilisateur(s) existant(s)")
    
    if created_users:
        print("\n🔑 Identifiants des nouveaux utilisateurs:")
        print("-" * 40)
        for user_data in created_users:
            print(f"👤 {user_data['username']}")
            print(f"   - Mot de passe: {user_data['password']}")
            print(f"   - Rôle: {user_data['group']}")
            print(f"   - Email: {user_data['email']}")
            print()
    
    print("🎯 Utilisateurs disponibles pour le dashboard:")
    print("-" * 40)
    print("👑 Super Admin:")
    print("   - superadmin / superadmin123")
    print("   - admin_garantie / admingarantie123")
    print()
    print("💻 Gestionnaire Informatique:")
    print("   - gest_info / gestinfo123")
    print()
    print("📋 Gestionnaire Bureau:")
    print("   - gest_bureau / gestbureau123")
    print()
    print("👤 Employés:")
    print("   - employe1 / employe123")
    print("   - employe2 / employe123")
    print()
    print("💡 Vous pouvez maintenant tester le dashboard avec ces utilisateurs!")

def list_users():
    """Liste tous les utilisateurs existants avec leurs groupes"""
    print("📋 Liste des utilisateurs existants")
    print("=" * 50)
    
    users = User.objects.all().order_by('username')
    
    if not users.exists():
        print("❌ Aucun utilisateur trouvé")
        return
    
    for user in users:
        groups = [group.name for group in user.groups.all()]
        groups_str = ", ".join(groups) if groups else "Aucun groupe"
        
        print(f"👤 {user.username}")
        print(f"   - Nom complet: {user.get_full_name()}")
        print(f"   - Email: {user.email}")
        print(f"   - Groupes: {groups_str}")
        print(f"   - Staff: {'Oui' if user.is_staff else 'Non'}")
        print(f"   - Superuser: {'Oui' if user.is_superuser else 'Non'}")
        print()

def delete_demo_users():
    """Supprime les utilisateurs de démonstration"""
    print("🧹 Suppression des utilisateurs de démonstration")
    print("=" * 50)
    
    demo_usernames = [
        'gest_info', 'gest_bureau', 'employe1', 'employe2', 'admin_garantie'
    ]
    
    deleted_count = 0
    for username in demo_usernames:
        try:
            user = User.objects.get(username=username)
            user.delete()
            print(f"✅ Utilisateur supprimé: {username}")
            deleted_count += 1
        except User.DoesNotExist:
            print(f"⚠️ Utilisateur {username} n'existe pas")
    
    print(f"\n🎯 {deleted_count} utilisateur(s) supprimé(s)")

def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--list":
            list_users()
        elif command == "--delete":
            delete_demo_users()
        elif command == "--help":
            print("📋 Commandes disponibles:")
            print("  python create_users.py              # Créer les utilisateurs de démo")
            print("  python create_users.py --list       # Lister tous les utilisateurs")
            print("  python create_users.py --delete     # Supprimer les utilisateurs de démo")
            print("  python create_users.py --help       # Afficher cette aide")
        else:
            print(f"❌ Commande inconnue: {command}")
            print("💡 Utilisez --help pour voir les commandes disponibles")
    else:
        create_users()

if __name__ == "__main__":
    main()
