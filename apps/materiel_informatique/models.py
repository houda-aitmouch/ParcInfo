from django.db import models
from django.contrib.auth import get_user_model
from apps.commande_informatique.models import LigneCommande, Commande
from datetime import timedelta
from dateutil.relativedelta import relativedelta

User = get_user_model()

class MaterielInformatique(models.Model):
    numero_serie = models.CharField(max_length=100)
    code_inventaire = models.CharField(max_length=100)
    commande = models.ForeignKey(Commande, on_delete=models.PROTECT, related_name='materiels')
    ligne_commande = models.ForeignKey(LigneCommande, on_delete=models.PROTECT, related_name='materiels')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(
        max_length=50,
        choices=[
            ('nouveau', 'Nouveau'),
            ('affecte', 'Affecté'),
            ('en panne', 'En panne'),
            ('en maintenance', 'En maintenance'),
        ],
        default='nouveau'
    )
    public = models.BooleanField(default=True)
    lieu_stockage = models.CharField(
        max_length=20,
        choices=[
            ('etage1', 'Etage 1'),
            ('etage2', 'Etage 2'),
            ('etage3', 'Etage 3'),
        ],
        default='etage1'
    )
    observation = models.TextField(blank=True)
    # Les champs suivants sont supprimés : designation, description, prix_unitaire, fournisseur, numero_facture, date_service, date_fin_garantie
    # Les dates peuvent être calculées dynamiquement dans le template

    def __str__(self):
        return f"{self.numero_serie} - {self.code_inventaire}"

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