from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommandeInformatiquePermissions:
    """Permissions personnalisées pour l'app commande_informatique"""
    
    @classmethod
    def create_permissions(cls):
        """Crée les permissions personnalisées pour les commandes informatiques"""
        from .models import Commande, LigneCommande
        
        # Permissions pour Commande
        commande_ct = ContentType.objects.get_for_model(Commande)
        
        permissions_commande = [
            ('view_commande_informatique', 'Consulter les commandes informatiques'),
            ('add_commande_informatique', 'Ajouter des commandes informatiques'),
            ('change_commande_informatique', 'Modifier les commandes informatiques'),
            ('delete_commande_informatique', 'Supprimer les commandes informatiques'),
            ('export_commande_informatique', 'Exporter les commandes informatiques en Excel'),
            ('approve_commande_informatique', 'Approuver les commandes informatiques'),
            ('validate_commande_informatique', 'Valider les commandes informatiques'),
            ('cancel_commande_informatique', 'Annuler les commandes informatiques'),
        ]
        
        for codename, name in permissions_commande:
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=commande_ct,
            )
        
        # Permissions pour LigneCommande
        ligne_ct = ContentType.objects.get_for_model(LigneCommande)
        
        permissions_ligne = [
            ('view_ligne_commande_informatique', 'Consulter les lignes de commande informatiques'),
            ('add_ligne_commande_informatique', 'Ajouter des lignes de commande informatiques'),
            ('change_ligne_commande_informatique', 'Modifier les lignes de commande informatiques'),
            ('delete_ligne_commande_informatique', 'Supprimer les lignes de commande informatiques'),
        ]
        
        for codename, name in permissions_ligne:
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=ligne_ct,
            )
    
    @classmethod
    def get_all_permissions(cls):
        """Retourne toutes les permissions de l'app"""
        return [
            'view_commande_informatique',
            'add_commande_informatique', 
            'change_commande_informatique',
            'delete_commande_informatique',
            'export_commande_informatique',
            'approve_commande_informatique',
            'validate_commande_informatique',
            'cancel_commande_informatique',
            'view_ligne_commande_informatique',
            'add_ligne_commande_informatique',
            'change_ligne_commande_informatique', 
            'delete_ligne_commande_informatique',
        ] 