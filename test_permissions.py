#!/usr/bin/env python
"""
Script de test pour vérifier les permissions et groupes
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


def test_permissions():
    """Test des permissions et groupes"""
    print("🔍 Test des permissions et groupes ParcInfo")
    print("=" * 50)
    
    # 1. Vérifier les groupes
    print("\n📋 Groupes d'utilisateurs :")
    groups = Group.objects.all()
    for group in groups:
        print(f"  • {group.name} ({group.user_set.count()} membres, {group.permissions.count()} permissions)")
    
    # 2. Vérifier les permissions par app
    print("\n🔐 Permissions par application :")
    apps = ['commande_informatique', 'commande_bureau', 'materiel_informatique', 'materiel_bureautique', 'fournisseurs']
    
    for app in apps:
        permissions = Permission.objects.filter(content_type__app_label=app)
        print(f"  • {app}: {permissions.count()} permissions")
        for perm in permissions[:3]:  # Afficher les 3 premières
            print(f"    - {perm.codename}: {perm.name}")
        if permissions.count() > 3:
            print(f"    ... et {permissions.count() - 3} autres")
    
    # 3. Vérifier l'utilisateur superadmin
    print("\n👤 Utilisateur superadmin :")
    try:
        superadmin = User.objects.get(username='superadmin')
        print(f"  • Username: {superadmin.username}")
        print(f"  • Email: {superadmin.email}")
        print(f"  • Groupes: {[g.name for g in superadmin.groups.all()]}")
        print(f"  • Permissions directes: {superadmin.user_permissions.count()}")
        
        # Calculer les permissions totales (directes + via groupes)
        total_permissions = set()
        for group in superadmin.groups.all():
            total_permissions.update(group.permissions.all())
        total_permissions.update(superadmin.user_permissions.all())
        
        print(f"  • Permissions totales: {len(total_permissions)}")
        
    except User.DoesNotExist:
        print("  ❌ Utilisateur superadmin non trouvé")
    
    # 4. Test des permissions spécifiques
    print("\n✅ Test des permissions spécifiques :")
    
    # Permissions commande informatique
    commande_info_perms = Permission.objects.filter(
        codename__startswith='commande_informatique'
    )
    print(f"  • Permissions commande_informatique: {commande_info_perms.count()}")
    
    # Permissions commande bureau
    commande_bureau_perms = Permission.objects.filter(
        codename__startswith='commande_bureau'
    )
    print(f"  • Permissions commande_bureau: {commande_bureau_perms.count()}")
    
    # Permissions matériel informatique
    materiel_info_perms = Permission.objects.filter(
        codename__startswith='materiel_informatique'
    )
    print(f"  • Permissions materiel_informatique: {materiel_info_perms.count()}")
    
    # Permissions matériel bureautique
    materiel_bureau_perms = Permission.objects.filter(
        codename__startswith='materiel_bureautique'
    )
    print(f"  • Permissions materiel_bureautique: {materiel_bureau_perms.count()}")
    
    # 5. Vérifier les permissions des groupes
    print("\n🎯 Permissions par groupe :")
    
    group_permissions = {
        'Super Admin': ['Toutes les permissions'],
        'Gestionnaire Informatique': [
            'view_commande_informatique', 'add_commande_informatique',
            'view_materiel_informatique', 'add_materiel_informatique'
        ],
        'Gestionnaire Bureau': [
            'view_commande_bureau', 'add_commande_bureau',
            'view_materiel_bureautique', 'add_materiel_bureautique'
        ],
        'Employe': [
            'view_commande_informatique', 'view_commande_bureau',
            'view_materiel_informatique', 'view_materiel_bureautique'
        ]
    }
    
    for group_name, expected_perms in group_permissions.items():
        try:
            group = Group.objects.get(name=group_name)
            print(f"  • {group_name}: {group.permissions.count()} permissions")
            
            if group_name != 'Super Admin':
                for perm_codename in expected_perms:
                    has_perm = group.permissions.filter(codename=perm_codename).exists()
                    status = "✅" if has_perm else "❌"
                    print(f"    {status} {perm_codename}")
                    
        except Group.DoesNotExist:
            print(f"  ❌ Groupe {group_name} non trouvé")
    
    print("\n" + "=" * 50)
    print("🎉 Test terminé !")
    
    # 6. Instructions d'accès
    print("\n🚀 Pour accéder à l'admin personnalisé :")
    print("  • URL: http://127.0.0.1:8000/admin/")
    print("  • Username: superadmin")
    print("  • Password: superadmin123")
    print("\n📖 Documentation: docs/GESTION_PERMISSIONS.md")


if __name__ == '__main__':
    test_permissions() 