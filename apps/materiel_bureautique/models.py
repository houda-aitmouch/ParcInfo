from django.db import models
from django.contrib.auth import get_user_model
from apps.commande_bureau.models import LigneCommandeBureau, CommandeBureau
from datetime import timedelta
from dateutil.relativedelta import relativedelta

User = get_user_model()

class MaterielBureau(models.Model):
    code_inventaire = models.CharField(max_length=100, unique=True)
    commande = models.ForeignKey(CommandeBureau, on_delete=models.PROTECT, related_name='materiels_bureau')
    ligne_commande = models.ForeignKey(LigneCommandeBureau, on_delete=models.PROTECT, related_name='materiels_bureau')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(
        max_length=50,
        choices=[
            ('operationnel', 'Opérationnel'),
            ('affecte', 'Affecté'),
            ('reparation', 'Réparation'),
            ('reforme', 'Réforme'),
        ],
        default='operationnel'
    )
    lieu_stockage = models.CharField(
        max_length=20,
        choices=[
            ('', '---------'),
            ('etage1', 'Etage 1'),
            ('etage2', 'Etage 2'),
            ('etage3', 'Etage 3'),
        ],
        blank=True,
        default=''
    )
    observation = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Matériel de bureau"
        verbose_name_plural = "Matériels de bureau"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.code_inventaire} - {self.ligne_commande.designation.nom}"

    @property
    def designation(self):
        """Désignation du matériel (depuis la ligne de commande)"""
        return self.ligne_commande.designation.nom

    @property
    def description(self):
        """Description du matériel (depuis la ligne de commande)"""
        return self.ligne_commande.description.nom

    @property
    def prix_unitaire(self):
        """Prix unitaire (depuis la ligne de commande)"""
        return self.ligne_commande.prix_unitaire

    @property
    def fournisseur(self):
        """Fournisseur (depuis la commande)"""
        return self.commande.fournisseur.nom

    @property
    def numero_facture(self):
        """Numéro de facture (depuis la commande)"""
        return self.commande.numero_facture

    @property
    def date_service_calculee(self):
        """
        Date de service = date de réception + 1 jour
        """
        date_reception = self.ligne_commande.commande.date_reception
        if date_reception:
            return date_reception + timedelta(days=1)
        return None

    @property
    def date_fin_garantie_calculee(self):
        date_service = self.date_service_calculee
        commande = self.ligne_commande.commande
        try:
            valeur = int(commande.duree_garantie_valeur)
        except (TypeError, ValueError):
            return None
        unite = (commande.duree_garantie_unite or '').strip().lower()
        if date_service and valeur and unite:
            if unite in ['jours', 'jour', 'j', 'jours.', 'jour.']:
                return date_service + timedelta(days=valeur)
            elif unite in ['mois', 'mois.', 'm']:
                return date_service + relativedelta(months=valeur)
            elif unite in ['ans', 'an', 'annee', 'année', 'annees', 'années', 'ans.', 'an.']:
                return date_service + relativedelta(years=valeur)
        return None
