from django.db import models
from apps.fournisseurs.models import Fournisseur

class Designation(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Description(models.Model):
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='descriptions')
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    MODE_PASSATION_CHOICES = [
        ('BC', 'Bon de Commande'),
        ('Contrat', 'Contrat'),
        ('AO', "Appel d'Offres"),
    ]

    mode_passation = models.CharField(max_length=10, choices=MODE_PASSATION_CHOICES)
    numero_commande = models.CharField(max_length=100)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date_commande = models.DateField()
    date_reception = models.DateField(null=True, blank=True)
    numero_facture = models.CharField(max_length=100, null=True, blank=True)
    DUREE_UNITE_CHOICES = [
        ('jour', 'Jour(s)'),
        ('mois', 'Mois'),
        ('annee', 'Année'),
    ]
    duree_garantie_valeur = models.PositiveIntegerField("Durée de garantie", default=1)
    duree_garantie_unite = models.CharField("Unité de durée", max_length=10, choices=DUREE_UNITE_CHOICES, default='mois')

    def __str__(self):
        return f"{self.mode_passation} - {self.numero_commande}"


# apps/commande/models.py

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.designation.nom} - {self.description.nom}"