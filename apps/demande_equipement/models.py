from django.db import models
from django.contrib.auth import get_user_model
from apps.commande_informatique.models import Designation as DesignationInfo, Description as DescriptionInfo
from apps.commande_bureau.models import DesignationBureau, DescriptionBureau

User = get_user_model()

class DemandeEquipement(models.Model):
    CATEGORIE_CHOICES = [
        ('informatique', 'Informatique'),
        ('bureau', 'Bureau'),
    ]
    
    TYPE_DEMANDE_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('renouvellement', 'Renouvellement'),
        ('reparation', 'Réparation'),
        ('service', 'Service'),
        ('deplacement', 'Déplacement'),
    ]
    
    TYPE_ARTICLE_CHOICES = [
        ('materiel', 'Matériel'),
        ('fourniture', 'Fourniture'),
    ]
    
    # Informations de base
    demandeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_equipement')
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('refusee', 'Refusée'),
    ], default='en_attente')
    
    # Catégorie et type
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    type_article = models.CharField(max_length=20, choices=TYPE_ARTICLE_CHOICES)
    type_demande = models.CharField(max_length=20, choices=TYPE_DEMANDE_CHOICES)
    
    # Désignation et description (pour matériel uniquement)
    designation_info = models.ForeignKey(
        DesignationInfo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='demandes_info'
    )
    description_info = models.ForeignKey(
        DescriptionInfo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='demandes_info'
    )
    designation_bureau = models.ForeignKey(
        DesignationBureau, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='demandes_bureau'
    )
    description_bureau = models.ForeignKey(
        DescriptionBureau, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='demandes_bureau'
    )
    
    # Fourniture (pour fourniture uniquement)
    fourniture = models.ForeignKey(
        'Fourniture',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demandes_fourniture',
        verbose_name="Fourniture demandée"
    )
    
    # Dates
    date_approbation = models.DateTimeField(null=True, blank=True)
    date_affectation = models.DateTimeField(null=True, blank=True)
    
    # Matériel sélectionné pour l'affectation
    materiel_selectionne_id = models.IntegerField(null=True, blank=True)
    
    # Signature de la décharge
    decharge_signee = models.BooleanField(default=False)
    date_signature = models.DateTimeField(null=True, blank=True)
    signature_image = models.CharField(max_length=255, null=True, blank=True, help_text="Chemin vers l'image de signature électronique")
    
    class Meta:
        verbose_name = "Demande d'équipement"
        verbose_name_plural = "Demandes d'équipement"
        ordering = ['-date_demande']
    
    def __str__(self):
        return f"Demande {self.id} - {self.demandeur.username} - {self.get_categorie_display()}"
    
    @property
    def designation(self):
        """Retourne la désignation selon la catégorie"""
        if self.categorie == 'informatique':
            return self.designation_info
        elif self.categorie == 'bureau':
            return self.designation_bureau
        return None
    
    @property
    def description(self):
        """Retourne la description selon la catégorie"""
        if self.categorie == 'informatique':
            return self.description_info
        elif self.categorie == 'bureau':
            return self.description_bureau
        return None
    
    def clean(self):
        """Validation personnalisée"""
        from django.core.exceptions import ValidationError
        
        # Pour les fournitures, type_demande doit être 'nouveau'
        if self.type_article == 'fourniture' and self.type_demande != 'nouveau':
            raise ValidationError("Pour les fournitures, le type de demande doit être 'Nouveau'")
        
        # Pour les fournitures, fourniture obligatoire et pas de désignation/description
        if self.type_article == 'fourniture':
            if not self.fourniture:
                raise ValidationError("Pour les fournitures, la sélection d'une fourniture est obligatoire")
            if self.designation_info or self.description_info or self.designation_bureau or self.description_bureau:
                raise ValidationError("Les fournitures ne doivent pas avoir de désignation ou description")
        
        # Pour les matériels, désignation et description obligatoires, pas de fourniture
        if self.type_article == 'materiel':
            if not self.designation or not self.description:
                raise ValidationError("Pour les matériels, la désignation et la description sont obligatoires")
            if self.fourniture:
                raise ValidationError("Les matériels ne doivent pas avoir de fourniture sélectionnée")

class ArchiveDecharge(models.Model):
    """Modèle pour l'archivage électronique des décharges signées"""
    demande = models.OneToOneField(DemandeEquipement, on_delete=models.CASCADE, related_name='archive_decharge')
    fichier_pdf = models.FileField(upload_to='archives/decharges/', verbose_name="Fichier PDF archivé")
    date_archivage = models.DateTimeField(auto_now_add=True, verbose_name="Date d'archivage")
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Archivé par")
    numero_archive = models.CharField(max_length=50, unique=True, verbose_name="Numéro d'archive")
    statut_archive = models.CharField(
        max_length=20,
        choices=[
            ('actif', 'Actif'),
            ('inactif', 'Inactif'),
            ('supprime', 'Supprimé'),
        ],
        default='actif',
        verbose_name="Statut de l'archive"
    )
    notes = models.TextField(blank=True, verbose_name="Notes d'archivage")
    
    class Meta:
        verbose_name = "Archive de décharge"
        verbose_name_plural = "Archives de décharges"
        ordering = ['-date_archivage']
    
    def __str__(self):
        return f"Archive {self.numero_archive} - {self.demande.demandeur.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.numero_archive:
            # Générer un numéro d'archive unique
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            count = ArchiveDecharge.objects.filter(
                numero_archive__startswith=f'ARCH-{date_str}'
            ).count() + 1
            self.numero_archive = f'ARCH-{date_str}-{count:04d}'
        super().save(*args, **kwargs)


class Fourniture(models.Model):
    """Modèle pour gérer les fournitures informatiques et bureautiques"""
    TYPE_CHOICES = [
        ('informatique', 'Informatique'),
        ('bureautique', 'Bureautique'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name="Nom de la fourniture")
    numero_serie = models.CharField(max_length=100, unique=True, verbose_name="Numéro de série")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type de fourniture")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Fourniture"
        verbose_name_plural = "Fournitures"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} - {self.numero_serie}"
    
    @classmethod
    def get_by_categorie(cls, categorie):
        """Retourne les fournitures selon la catégorie (informatique/bureau)"""
        if categorie == 'informatique':
            return cls.objects.filter(type='informatique', actif=True)
        elif categorie == 'bureau':
            return cls.objects.filter(type='bureautique', actif=True)
        return cls.objects.none()
