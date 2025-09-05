from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    username_validator = RegexValidator(
        regex=r'^[\w.@+\- ]+$',  # autorise les espaces
        message="Ce champ peut contenir des lettres, chiffres, @/./+/-/_ et espaces."
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text="Requis. 150 caractères max. Lettres, chiffres, @/./+/-/_ et espaces autorisés.",
        error_messages={
            "unique": "Un utilisateur avec ce nom existe déjà.",
        },
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username

class NotificationDemande(models.Model):
    """Modèle pour les notifications de traitement des demandes d'équipement"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
        ('refusee', 'Refusée'),
        ('en_cours', 'En cours de traitement'),
        ('terminee', 'Terminée'),
        ('en_attente_signature', 'En attente de signature'),
        ('signature_requise', 'Signature requise'),
    ]
    
    TYPE_CHOICES = [
        ('demande_equipement', 'Demande d\'équipement'),
        ('demande_bureau', 'Demande bureautique'),
    ]
    
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_demande')
    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    statut_demande = models.CharField(max_length=20, choices=STATUT_CHOICES)
    demande_id = models.IntegerField(help_text="ID de la demande concernée")
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Notification de demande"
        verbose_name_plural = "Notifications de demandes"
    
    def __str__(self):
        return f"Notification pour {self.utilisateur.username} - {self.titre}"
    
    def marquer_comme_lu(self):
        """Marque la notification comme lue"""
        from django.utils import timezone
        self.lu = True
        self.date_lecture = timezone.now()
        self.save()
    
    @property
    def est_recente(self):
        """Vérifie si la notification est récente (moins de 24h)"""
        from django.utils import timezone
        from datetime import timedelta
        return self.date_creation > timezone.now() - timedelta(hours=24)
    
    @property
    def badge_couleur(self):
        """Retourne la couleur du badge selon le statut"""
        couleurs = {
            'en_attente': 'bg-yellow-100 text-yellow-800',
            'approuvee': 'bg-green-100 text-green-800',
            'rejetee': 'bg-red-100 text-red-800',
            'refusee': 'bg-red-100 text-red-800',
            'en_cours': 'bg-blue-100 text-blue-800',
            'terminee': 'bg-gray-100 text-gray-800',
            'en_attente_signature': 'bg-orange-100 text-orange-800',
            'signature_requise': 'bg-purple-100 text-purple-800',
        }
        return couleurs.get(self.statut_demande, 'bg-gray-100 text-gray-800')