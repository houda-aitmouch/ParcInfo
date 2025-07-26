from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Command(BaseCommand):
    help = 'Configure les permissions et groupes pour ParcInfo'

    def handle(self, *args, **options):
        self.stdout.write('Configuration des permissions et groupes...')
        
        # Créer les permissions personnalisées
        self.create_custom_permissions()
        
        # Créer les groupes avec leurs permissions
        self.create_groups_with_permissions()
        
        self.stdout.write(
            self.style.SUCCESS('Configuration terminée avec succès!')
        )

    def create_custom_permissions(self):
        """Crée les permissions personnalisées pour toutes les apps"""
        self.stdout.write('Création des permissions personnalisées...')
        
        # Permissions pour les commandes informatiques
        try:
            from apps.commande_informatique.permissions import CommandeInformatiquePermissions
            CommandeInformatiquePermissions.create_permissions()
            self.stdout.write('✓ Permissions commande_informatique créées')
        except Exception as e:
            self.stdout.write(f'⚠ Erreur permissions commande_informatique: {e}')
        
        # Permissions pour les commandes bureau
        try:
            from apps.commande_bureau.permissions import CommandeBureauPermissions
            CommandeBureauPermissions.create_permissions()
            self.stdout.write('✓ Permissions commande_bureau créées')
        except Exception as e:
            self.stdout.write(f'⚠ Erreur permissions commande_bureau: {e}')
        
        # Permissions pour les matériels informatiques
        try:
            from apps.materiel_informatique.permissions import MaterielInformatiquePermissions
            MaterielInformatiquePermissions.create_permissions()
            self.stdout.write('✓ Permissions materiel_informatique créées')
        except Exception as e:
            self.stdout.write(f'⚠ Erreur permissions materiel_informatique: {e}')
        
        # Permissions pour les matériels bureautiques
        try:
            from apps.materiel_bureautique.permissions import MaterielBureautiquePermissions
            MaterielBureautiquePermissions.create_permissions()
            self.stdout.write('✓ Permissions materiel_bureautique créées')
        except Exception as e:
            self.stdout.write(f'⚠ Erreur permissions materiel_bureautique: {e}')

    def create_groups_with_permissions(self):
        """Crée les groupes avec leurs permissions spécifiques"""
        self.stdout.write('Création des groupes avec permissions...')
        
        # Groupe Super Admin
        super_admin_group, created = Group.objects.get_or_create(name='Super Admin')
        if created:
            self.stdout.write('✓ Groupe Super Admin créé')
        
        # Donner toutes les permissions au Super Admin
        all_permissions = Permission.objects.all()
        super_admin_group.permissions.set(all_permissions)
        self.stdout.write(f'✓ {all_permissions.count()} permissions assignées au Super Admin')
        
        # Groupe Gestionnaire Informatique
        gest_info_group, created = Group.objects.get_or_create(name='Gestionnaire Informatique')
        if created:
            self.stdout.write('✓ Groupe Gestionnaire Informatique créé')
        
        # Permissions pour Gestionnaire Informatique
        gest_info_permissions = Permission.objects.filter(
            codename__in=[
                # Commandes informatiques
                'view_commande_informatique', 'add_commande_informatique', 
                'change_commande_informatique', 'delete_commande_informatique',
                'export_commande_informatique', 'approve_commande_informatique',
                'view_ligne_commande_informatique', 'add_ligne_commande_informatique',
                'change_ligne_commande_informatique', 'delete_ligne_commande_informatique',
                # Matériels informatiques
                'view_materiel_informatique', 'add_materiel_informatique',
                'change_materiel_informatique', 'delete_materiel_informatique',
                'export_materiel_informatique', 'assign_materiel_informatique',
                'maintenance_materiel_informatique',
                # Fournisseurs (lecture seule)
                'view_fournisseur',
            ]
        )
        gest_info_group.permissions.set(gest_info_permissions)
        self.stdout.write(f'✓ {gest_info_permissions.count()} permissions assignées au Gestionnaire Informatique')
        
        # Groupe Gestionnaire Bureau
        gest_bureau_group, created = Group.objects.get_or_create(name='Gestionnaire Bureau')
        if created:
            self.stdout.write('✓ Groupe Gestionnaire Bureau créé')
        
        # Permissions pour Gestionnaire Bureau
        gest_bureau_permissions = Permission.objects.filter(
            codename__in=[
                # Commandes bureau
                'view_commande_bureau', 'add_commande_bureau',
                'change_commande_bureau', 'delete_commande_bureau',
                'export_commande_bureau', 'approve_commande_bureau',
                'view_ligne_commande_bureau', 'add_ligne_commande_bureau',
                'change_ligne_commande_bureau', 'delete_ligne_commande_bureau',
                # Matériels bureautiques
                'view_materiel_bureautique', 'add_materiel_bureautique',
                'change_materiel_bureautique', 'delete_materiel_bureautique',
                'export_materiel_bureautique', 'assign_materiel_bureautique',
                'maintenance_materiel_bureautique',
                # Fournisseurs (lecture seule)
                'view_fournisseur',
            ]
        )
        gest_bureau_group.permissions.set(gest_bureau_permissions)
        self.stdout.write(f'✓ {gest_bureau_permissions.count()} permissions assignées au Gestionnaire Bureau')
        
        # Groupe Employé
        employe_group, created = Group.objects.get_or_create(name='Employe')
        if created:
            self.stdout.write('✓ Groupe Employé créé')
        
        # Permissions pour Employé (lecture seule)
        employe_permissions = Permission.objects.filter(
            codename__in=[
                # Lecture seule des commandes
                'view_commande_informatique', 'view_commande_bureau',
                'view_ligne_commande_informatique', 'view_ligne_commande_bureau',
                # Lecture seule des matériels
                'view_materiel_informatique', 'view_materiel_bureautique',
                # Lecture seule des fournisseurs
                'view_fournisseur',
            ]
        )
        employe_group.permissions.set(employe_permissions)
        self.stdout.write(f'✓ {employe_permissions.count()} permissions assignées à l\'Employé')
        
        # Créer un utilisateur Super Admin par défaut s'il n'existe pas
        if not User.objects.filter(username='superadmin').exists():
            superadmin = User.objects.create_user(
                username='superadmin',
                email='superadmin@parcinfo.com',
                password='superadmin123',
                first_name='Super',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )
            superadmin.groups.add(super_admin_group)
            self.stdout.write('✓ Utilisateur superadmin créé (username: superadmin, password: superadmin123)')
        else:
            self.stdout.write('✓ Utilisateur superadmin existe déjà') 