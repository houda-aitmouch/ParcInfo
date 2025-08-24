"""
Configuration personnalisée pour l'admin Django ParcInfo
"""

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class ParcInfoAdminSite(AdminSite):
    """Site d'administration personnalisé pour ParcInfo"""
    
    # Titre et en-tête
    site_header = _('Administration ParcInfo')
    site_title = _('ParcInfo Admin')
    index_title = _('Tableau de bord ParcInfo')
    
    # Configuration du site
    site_url = '/'
    enable_nav_sidebar = True
    
    def index(self, request, extra_context=None):
        """Page d'accueil personnalisée avec statistiques"""
        extra_context = extra_context or {}
        
        # Statistiques des utilisateurs
        from apps.users.models import CustomUser
        extra_context['user_count'] = CustomUser.objects.count()
        
        # Statistiques des équipements
        try:
            from apps.materiel_informatique.models import MaterielInformatique
            from apps.materiel_bureautique.models import MaterielBureau
            extra_context['equipment_count'] = (
                MaterielInformatique.objects.count() + 
                MaterielBureau.objects.count()
            )
        except ImportError:
            extra_context['equipment_count'] = 0
        
        # Statistiques des demandes
        try:
            from apps.demande_equipement.models import DemandeEquipement
            extra_context['demand_count'] = DemandeEquipement.objects.count()
        except ImportError:
            extra_context['demand_count'] = 0
        
        return super().index(request, extra_context)

# Instance du site admin personnalisé
admin_site = ParcInfoAdminSite(name='parcinfo_admin')

# Configuration des modèles d'administration
def configure_admin_models():
    """Configure tous les modèles d'administration"""
    
    # Configuration des utilisateurs
    from apps.users.admin import CustomUserAdmin, CustomGroupAdmin, NotificationDemandeAdmin
    from apps.users.models import CustomUser, NotificationDemande
    from django.contrib.auth.models import Group
    
    admin_site.register(CustomUser, CustomUserAdmin)
    admin_site.register(Group, CustomGroupAdmin)
    admin_site.register(NotificationDemande, NotificationDemandeAdmin)
    
    # Configuration des fournisseurs
    try:
        from apps.fournisseurs.admin import FournisseurAdmin
        from apps.fournisseurs.models import Fournisseur
        admin_site.register(Fournisseur, FournisseurAdmin)
    except ImportError:
        pass
    
    # Configuration des commandes informatiques
    try:
        from apps.commande_informatique.admin import CommandeAdmin, LigneCommandeAdmin
        from apps.commande_informatique.models import Commande, LigneCommande
        admin_site.register(Commande, CommandeAdmin)
        admin_site.register(LigneCommande, LigneCommandeAdmin)
    except ImportError:
        pass
    
    # Configuration des commandes bureau
    try:
        from apps.commande_bureau.admin import CommandeBureauAdmin, LigneCommandeBureauAdmin
        from apps.commande_bureau.models import CommandeBureau, LigneCommandeBureau
        admin_site.register(CommandeBureau, CommandeBureauAdmin)
        admin_site.register(LigneCommandeBureau, LigneCommandeBureauAdmin)
    except ImportError:
        pass
    
    # Configuration des matériels informatiques
    try:
        from apps.materiel_informatique.admin import MaterielInformatiqueAdmin
        from apps.materiel_informatique.models import MaterielInformatique
        admin_site.register(MaterielInformatique, MaterielInformatiqueAdmin)
    except ImportError:
        pass
    
    # Configuration des matériels bureautiques
    try:
        from apps.materiel_bureautique.admin import MaterielBureauAdmin
        from apps.materiel_bureautique.models import MaterielBureau
        admin_site.register(MaterielBureau, MaterielBureauAdmin)
    except ImportError:
        pass
    
    # Configuration des demandes d'équipement
    try:
        from apps.demande_equipement.admin import DemandeEquipementAdmin
        from apps.demande_equipement.models import DemandeEquipement
        admin_site.register(DemandeEquipement, DemandeEquipementAdmin)
    except ImportError:
        pass
    
    # Configuration des livraisons
    try:
        from apps.livraison.admin import LivraisonAdmin
        from apps.livraison.models import Livraison
        admin_site.register(Livraison, LivraisonAdmin)
    except ImportError:
        pass
    
    # Configuration du chatbot
    try:
        from apps.chatbot.admin import ChatbotInteractionAdmin
        from apps.chatbot.models import ChatbotInteraction
        admin_site.register(ChatbotInteraction, ChatbotInteractionAdmin)
    except ImportError:
        pass

# Configuration des permissions
def configure_permissions():
    """Configure les permissions du système"""
    
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    
    # Créer les groupes s'ils n'existent pas
    groups_data = [
        'Super Admin',
        'Gestionnaire Informatique', 
        'Gestionnaire Bureau',
        'Employé'
    ]
    
    for group_name in groups_data:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✅ Groupe créé: {group_name}")
    
    # Permissions spécifiques pour chaque groupe
    permissions_config = {
        'Super Admin': {
            'description': 'Accès complet à tous les modules du système',
            'permissions': [
                # Toutes les permissions
            ]
        },
        'Gestionnaire Informatique': {
            'description': 'Gestion des équipements informatiques et commandes IT',
            'permissions': [
                'add_materielinformatique',
                'change_materielinformatique',
                'delete_materielinformatique',
                'view_materielinformatique',
                'add_commande',
                'change_commande',
                'delete_commande',
                'view_commande',
                'add_lignecommande',
                'change_lignecommande',
                'delete_lignecommande',
                'view_lignecommande',
                'add_demandeequipement',
                'change_demandeequipement',
                'view_demandeequipement',
                'add_livraison',
                'change_livraison',
                'view_livraison',
            ]
        },
        'Gestionnaire Bureau': {
            'description': 'Gestion des équipements bureautiques et commandes bureau',
            'permissions': [
                'add_materielbureau',
                'change_materielbureau',
                'delete_materielbureau',
                'view_materielbureau',
                'add_commandebureau',
                'change_commandebureau',
                'delete_commandebureau',
                'view_commandebureau',
                'add_lignecommandebureau',
                'change_lignecommandebureau',
                'delete_lignecommandebureau',
                'view_lignecommandebureau',
                'add_demandeequipement',
                'change_demandeequipement',
                'view_demandeequipement',
                'add_livraison',
                'change_livraison',
                'view_livraison',
            ]
        },
        'Employé': {
            'description': 'Accès limité aux demandes et équipements personnels',
            'permissions': [
                'add_demandeequipement',
                'change_demandeequipement',
                'view_demandeequipement',
                'view_materielinformatique',
                'view_materielbureau',
                'view_commande',
                'view_lignecommande',
                'view_commandebureau',
                'view_lignecommandebureau',
                'view_livraison',
            ]
        }
    }
    
    # Appliquer les permissions
    for group_name, config in permissions_config.items():
        try:
            group = Group.objects.get(name=group_name)
            
            # Ajouter la description au groupe
            if hasattr(group, 'description'):
                group.description = config['description']
                group.save()
            
            # Ajouter les permissions spécifiques
            if 'permissions' in config and config['permissions']:
                permissions = []
                for perm_codename in config['permissions']:
                    try:
                        # Essayer de trouver la permission par son nom
                        perm = Permission.objects.get(codename=perm_codename)
                        permissions.append(perm)
                    except Permission.DoesNotExist:
                        # Si pas trouvé, essayer de le créer
                        print(f"⚠️ Permission non trouvée: {perm_codename}")
                        continue
                
                if permissions:
                    group.permissions.set(permissions)
                    print(f"✅ Permissions mises à jour pour {group_name}")
            
        except Group.DoesNotExist:
            print(f"❌ Groupe non trouvé: {group_name}")

# Fonction principale de configuration
def setup_admin():
    """Configure complètement l'admin Django"""
    print("🚀 Configuration de l'admin Django ParcInfo...")
    
    # Configurer les modèles
    configure_admin_models()
    
    # Configurer les permissions
    configure_permissions()
    
    print("✅ Admin Django ParcInfo configuré avec succès!")
    return admin_site

if __name__ == "__main__":
    # Test de la configuration
    import os
    import django
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
    django.setup()
    
    setup_admin()
