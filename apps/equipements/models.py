from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Equipement(models.Model):
    sn_article = models.CharField(max_length=50, verbose_name="N° de série")  # ✅ Nouvelle colonne
    code_inventaire = models.CharField(max_length=50, verbose_name="Code N° Inventaire")
    date_service = models.DateField(null=True, blank=True, verbose_name="Date de service")
    designation = models.CharField(max_length=100, verbose_name="Désignation")
    description = models.TextField(blank=True, verbose_name="Description")
    prix_ht_mad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix HT en MAD")
    fournisseur = models.CharField(max_length=100, blank=True, verbose_name="Fournisseur")
    numero_facture = models.CharField(max_length=50, blank=True, verbose_name="N° Facture")
    date_garantie = models.DateField(null=True, blank=True, verbose_name="Date de garantie")
    STATUT_CHOICES = [
        ('affecte', 'Affecté'),
        ('panne', 'En panne'),
        ('maintenance', 'Maintenance'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='affecte', verbose_name="Statut")  # ✅ Statut

    is_public = models.BooleanField(default=False, verbose_name="Public")  # ✅ Public

    LIEU_CHOICES = [
        ('etage1', 'Étage 1'),
        ('etage2', 'Étage 2'),
        ('etage3', 'Étage 3'),
    ]
    lieu_affectation = models.CharField(max_length=20, choices=LIEU_CHOICES, blank=True, verbose_name="Lieu")  # ✅ Lieu

    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilisateur")  # ✅ Utilisateur

    observations = models.TextField(blank=True, verbose_name="Observations")  # ✅ Observations

    def __str__(self):
        return f"{self.code_inventaire} - {self.designation}"


class Materiel(models.Model):
    code_inventaire = models.CharField(max_length=100, unique=True)
    date_mise_en_service = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    designation = models.TextField(null=True, blank=True)
    prix_ht_mad = models.FloatField(null=True, blank=True)
    fournisseur = models.CharField(max_length=255, null=True, blank=True)

    etat_article = models.CharField(
        max_length=50,
        choices=[
            ("opérationnel", "Opérationnel"),
            ("réparation", "Réparation"),
            ("réforme", "Réforme")
        ],
        null=True, blank=True
    )
    lieu_affectation = models.CharField(max_length=255, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)

    affecte_a = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materiels_affectes",
        verbose_name="Affecté à"
    )

    def __str__(self):
        return f"{self.code_inventaire} - {self.designation}"