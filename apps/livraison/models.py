from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Livraison(models.Model):
    """Modèle pour gérer les livraisons des commandes informatique et bureau"""
    
    # Types de commandes
    TYPE_COMMANDE_CHOICES = [
        ('informatique', 'Commande Informatique'),
        ('bureau', 'Commande Bureau'),
    ]
    
    # Statuts de livraison
    STATUT_LIVRAISON_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('retardee', 'Retardée'),
        ('annulee', 'Annulée'),
    ]
    
    # Informations de base
    numero_commande = models.CharField(max_length=50, verbose_name="Numéro de commande")
    type_commande = models.CharField(max_length=20, choices=TYPE_COMMANDE_CHOICES, verbose_name="Type de commande")
    
    # Références aux commandes
    commande_informatique = models.ForeignKey(
        'commande_informatique.Commande', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name="Commande Informatique"
    )
    commande_bureau = models.ForeignKey(
        'commande_bureau.CommandeBureau', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name="Commande Bureau"
    )
    
    # Informations de livraison
    date_livraison_prevue = models.DateField(verbose_name="Date de livraison prévue")
    date_livraison_effective = models.DateField(null=True, blank=True, verbose_name="Date de livraison effective")
    statut_livraison = models.CharField(
        max_length=20, 
        choices=STATUT_LIVRAISON_CHOICES, 
        default='en_attente', 
        verbose_name="Statut de livraison"
    )
    
    # Conformité et réception
    conforme = models.BooleanField(default=True, verbose_name="Conforme")
    pv_reception_recu = models.BooleanField(
        default=False,
        verbose_name="PV réception validé ?",
        help_text="Cochez si le PV de réception a bien été validé et signé"
    )
    
    # Informations supplémentaires
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Traçabilité
    cree_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='livraisons_crees', 
        verbose_name="Créé par"
    )
    modifie_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='livraisons_modifiees', 
        verbose_name="Modifié par"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ['-date_creation']
        unique_together = ['numero_commande', 'type_commande']
    
    def __str__(self):
        return f"Livraison {self.numero_commande} - {self.get_type_commande_display()}"
    
    def save(self, *args, **kwargs):
        # Définir automatiquement le type de commande selon la commande liée
        if self.commande_informatique and not self.type_commande:
            self.type_commande = 'informatique'
            self.numero_commande = self.commande_informatique.numero_commande
        elif self.commande_bureau and not self.type_commande:
            self.type_commande = 'bureau'
            self.numero_commande = self.commande_bureau.numero_commande
        
        super().save(*args, **kwargs)
    
    @property
    def commande(self):
        """Retourne la commande associée (informatique ou bureau)"""
        return self.commande_informatique or self.commande_bureau
    
    @property
    def materiels(self):
        """Retourne les matériels de la commande"""
        if self.commande_informatique:
            return self.commande_informatique.lignes.all()
        elif self.commande_bureau:
            return self.commande_bureau.lignes.all()
        return []
    
    @property
    def fournisseur(self):
        """Retourne le fournisseur de la commande"""
        if self.commande_informatique:
            return self.commande_informatique.fournisseur
        elif self.commande_bureau:
            return self.commande_bureau.fournisseur
        return None
    
    @property
    def montant_total(self):
        """Retourne le montant total de la commande"""
        if self.commande_informatique:
            return self.commande_informatique.montant_total
        elif self.commande_bureau:
            return self.commande_bureau.montant_total
        return 0
