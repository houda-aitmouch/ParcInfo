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
            ('view_commande_informatique', 'Peut voir les commandes informatiques'),
            ('add_commande_informatique', 'Peut ajouter des commandes informatiques'),
            ('change_commande_informatique', 'Peut modifier les commandes informatiques'),
            ('delete_commande_informatique', 'Peut supprimer les commandes informatiques'),
            ('export_commande_informatique', 'Peut exporter les commandes informatiques'),
            ('approve_commande_informatique', 'Peut approuver les commandes informatiques'),
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
            ('view_ligne_commande_informatique', 'Peut voir les lignes de commande informatiques'),
            ('add_ligne_commande_informatique', 'Peut ajouter des lignes de commande informatiques'),
            ('change_ligne_commande_informatique', 'Peut modifier les lignes de commande informatiques'),
            ('delete_ligne_commande_informatique', 'Peut supprimer les lignes de commande informatiques'),
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
            'view_ligne_commande_informatique',
            'add_ligne_commande_informatique',
            'change_ligne_commande_informatique', 
            'delete_ligne_commande_informatique',
        ] 