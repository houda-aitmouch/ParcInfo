from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommandeBureauPermissions:
    """Permissions personnalisées pour l'app commande_bureau"""
    
    @classmethod
    def create_permissions(cls):
        """Crée les permissions personnalisées pour les commandes bureau"""
        from .models import CommandeBureau, LigneCommandeBureau
        
        # Permissions pour CommandeBureau
        commande_ct = ContentType.objects.get_for_model(CommandeBureau)
        
        permissions_commande = [
            ('view_commande_bureau', 'Peut voir les commandes bureau'),
            ('add_commande_bureau', 'Peut ajouter des commandes bureau'),
            ('change_commande_bureau', 'Peut modifier les commandes bureau'),
            ('delete_commande_bureau', 'Peut supprimer les commandes bureau'),
            ('export_commande_bureau', 'Peut exporter les commandes bureau'),
            ('approve_commande_bureau', 'Peut approuver les commandes bureau'),
        ]
        
        for codename, name in permissions_commande:
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=commande_ct,
            )
        
        # Permissions pour LigneCommandeBureau
        ligne_ct = ContentType.objects.get_for_model(LigneCommandeBureau)
        
        permissions_ligne = [
            ('view_ligne_commande_bureau', 'Peut voir les lignes de commande bureau'),
            ('add_ligne_commande_bureau', 'Peut ajouter des lignes de commande bureau'),
            ('change_ligne_commande_bureau', 'Peut modifier les lignes de commande bureau'),
            ('delete_ligne_commande_bureau', 'Peut supprimer les lignes de commande bureau'),
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
            'view_commande_bureau',
            'add_commande_bureau', 
            'change_commande_bureau',
            'delete_commande_bureau',
            'export_commande_bureau',
            'approve_commande_bureau',
            'view_ligne_commande_bureau',
            'add_ligne_commande_bureau',
            'change_ligne_commande_bureau', 
            'delete_ligne_commande_bureau',
        ] 