from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class FournisseursPermissions:
    """Permissions personnalisées pour l'app fournisseurs"""
    
    @classmethod
    def create_permissions(cls):
        """Crée les permissions personnalisées pour les fournisseurs"""
        from .models import Fournisseur
        
        # Permissions pour Fournisseur
        fournisseur_ct = ContentType.objects.get_for_model(Fournisseur)
        
        permissions_fournisseur = [
            ('view_fournisseur', 'Consulter les fournisseurs'),
            ('add_fournisseur', 'Ajouter des fournisseurs'),
            ('change_fournisseur', 'Modifier les fournisseurs'),
            ('delete_fournisseur', 'Supprimer les fournisseurs'),
            ('export_fournisseur', 'Exporter la liste des fournisseurs en Excel'),
            ('contact_fournisseur', 'Contacter les fournisseurs'),
            ('evaluate_fournisseur', 'Évaluer les fournisseurs'),
            ('blacklist_fournisseur', 'Mettre un fournisseur en liste noire'),
        ]
        
        for codename, name in permissions_fournisseur:
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=fournisseur_ct,
            )
    
    @classmethod
    def get_all_permissions(cls):
        """Retourne toutes les permissions de l'app"""
        return [
            'view_fournisseur',
            'add_fournisseur', 
            'change_fournisseur',
            'delete_fournisseur',
            'export_fournisseur',
            'contact_fournisseur',
            'evaluate_fournisseur',
            'blacklist_fournisseur',
        ] 