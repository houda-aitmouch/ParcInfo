from django.db import models

class Fournisseur(models.Model):
    CATEGORIE_CHOICES = [
        ('informatique', 'Matériel Informatique'),
        ('bureautique', 'Matériel Bureautique'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom du fournisseur")
    email = models.EmailField(verbose_name="Adresse e-mail")
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIE_CHOICES,
        verbose_name="Catégorie de matériel"
    )

    numero_contrat = models.CharField(
        max_length=100,
        verbose_name="Numéro de contrat"
    )
    date_derniere_commande = models.DateField(blank=True, null=True, verbose_name="Date de la dernière commande")

    def __str__(self):
        return f"{self.nom} - {self.get_categorie_display()}"

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['categorie', 'nom']