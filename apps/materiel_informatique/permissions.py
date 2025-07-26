from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class MaterielInformatiquePermissions:
    """Permissions personnalisées pour l'app materiel_informatique"""
    
    @classmethod
    def create_permissions(cls):
        """Crée les permissions personnalisées pour les matériels informatiques"""
        from .models import MaterielInformatique
        
        # Permissions pour MaterielInformatique
        materiel_ct = ContentType.objects.get_for_model(MaterielInformatique)
        
        permissions_materiel = [
            ('view_materiel_informatique', 'Peut voir les matériels informatiques'),
            ('add_materiel_informatique', 'Peut ajouter des matériels informatiques'),
            ('change_materiel_informatique', 'Peut modifier les matériels informatiques'),
            ('delete_materiel_informatique', 'Peut supprimer les matériels informatiques'),
            ('export_materiel_informatique', 'Peut exporter les matériels informatiques'),
            ('assign_materiel_informatique', 'Peut assigner des matériels informatiques'),
            ('maintenance_materiel_informatique', 'Peut gérer la maintenance des matériels informatiques'),
        ]
        
        for codename, name in permissions_materiel:
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=materiel_ct,
            )
    
    @classmethod
    def get_all_permissions(cls):
        """Retourne toutes les permissions de l'app"""
        return [
            'view_materiel_informatique',
            'add_materiel_informatique', 
            'change_materiel_informatique',
            'delete_materiel_informatique',
            'export_materiel_informatique',
            'assign_materiel_informatique',
            'maintenance_materiel_informatique',
        ] 