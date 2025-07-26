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
            ('view_materiel_bureautique', 'Consulter les matériels bureautiques'),
            ('add_materiel_bureautique', 'Ajouter des matériels bureautiques'),
            ('change_materiel_bureautique', 'Modifier les matériels bureautiques'),
            ('delete_materiel_bureautique', 'Supprimer les matériels bureautiques'),
            ('export_materiel_bureautique', 'Exporter les matériels bureautiques en Excel'),
            ('assign_materiel_bureautique', 'Assigner des matériels bureautiques aux utilisateurs'),
            ('maintenance_materiel_bureautique', 'Gérer la maintenance des matériels bureautiques'),
            ('inventory_materiel_bureautique', 'Effectuer l\'inventaire des matériels bureautiques'),
            ('repair_materiel_bureautique', 'Marquer les matériels bureautiques en réparation'),
            ('retire_materiel_bureautique', 'Mettre à la retraite les matériels bureautiques'),
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
            'inventory_materiel_bureautique',
            'repair_materiel_bureautique',
            'retire_materiel_bureautique',
        ] 