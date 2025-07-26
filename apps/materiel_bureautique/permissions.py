from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class MaterielBureautiquePermissions:
    """Permissions personnalisées pour l'app materiel_bureautique"""
    
    @classmethod
    def create_permissions(cls):
        """Crée les permissions personnalisées pour les matériels bureautiques"""
        from .models import MaterielBureau
        
        # Permissions pour MaterielBureau
        materiel_ct = ContentType.objects.get_for_model(MaterielBureau)
        
        permissions_materiel = [
            ('view_materiel_bureautique', 'Peut voir les matériels bureautiques'),
            ('add_materiel_bureautique', 'Peut ajouter des matériels bureautiques'),
            ('change_materiel_bureautique', 'Peut modifier les matériels bureautiques'),
            ('delete_materiel_bureautique', 'Peut supprimer les matériels bureautiques'),
            ('export_materiel_bureautique', 'Peut exporter les matériels bureautiques'),
            ('assign_materiel_bureautique', 'Peut assigner des matériels bureautiques'),
            ('maintenance_materiel_bureautique', 'Peut gérer la maintenance des matériels bureautiques'),
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
            'view_materiel_bureautique',
            'add_materiel_bureautique', 
            'change_materiel_bureautique',
            'delete_materiel_bureautique',
            'export_materiel_bureautique',
            'assign_materiel_bureautique',
            'maintenance_materiel_bureautique',
        ] 