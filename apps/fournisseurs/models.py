from django.db import models

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    if_fiscal = models.CharField("Identifiant Fiscal (IF)", max_length=50, unique=True)
    ice = models.CharField("Identifiant Commun de l'Entreprise (ICE)", max_length=50, blank=True, null=True)
    registre_commerce = models.CharField("Registre du Commerce (RC)", max_length=50, blank=True, null=True)
    adresse = models.TextField("Adresse", blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - IF: {self.if_fiscal}"