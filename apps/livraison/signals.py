from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.commande_informatique.models import Commande as CommandeInfo
from apps.commande_bureau.models import CommandeBureau
from apps.fournisseurs.models import Fournisseur
from .models import Livraison


@receiver(post_save, sender=CommandeInfo)
def update_livraisons_informatique_on_commande_change(sender, instance, **kwargs):
    """
    Met à jour les livraisons liées quand une commande informatique est modifiée
    """
    # Trouver toutes les livraisons liées à cette commande
    livraisons = Livraison.objects.filter(commande_informatique=instance)
    
    for livraison in livraisons:
        # Mettre à jour le numéro de commande si nécessaire
        if livraison.numero_commande != instance.numero_commande:
            livraison.numero_commande = instance.numero_commande
            livraison.save(update_fields=['numero_commande', 'date_modification'])
        
        # Déclencher une sauvegarde pour mettre à jour date_modification
        livraison.save(update_fields=['date_modification'])


@receiver(post_save, sender=CommandeBureau)
def update_livraisons_bureau_on_commande_change(sender, instance, **kwargs):
    """
    Met à jour les livraisons liées quand une commande bureau est modifiée
    """
    # Trouver toutes les livraisons liées à cette commande
    livraisons = Livraison.objects.filter(commande_bureau=instance)
    
    for livraison in livraisons:
        # Mettre à jour le numéro de commande si nécessaire
        if livraison.numero_commande != instance.numero_commande:
            livraison.numero_commande = instance.numero_commande
            livraison.save(update_fields=['numero_commande', 'date_modification'])
        
        # Déclencher une sauvegarde pour mettre à jour date_modification
        livraison.save(update_fields=['date_modification'])


@receiver(post_save, sender=Fournisseur)
def update_livraisons_on_fournisseur_change(sender, instance, **kwargs):
    """
    Met à jour les livraisons liées quand un fournisseur est modifié
    """
    # Mettre à jour les livraisons des commandes informatiques
    livraisons_info = Livraison.objects.filter(
        commande_informatique__fournisseur=instance
    )
    
    for livraison in livraisons_info:
        livraison.save(update_fields=['date_modification'])
    
    # Mettre à jour les livraisons des commandes bureau
    livraisons_bureau = Livraison.objects.filter(
        commande_bureau__fournisseur=instance
    )
    
    for livraison in livraisons_bureau:
        livraison.save(update_fields=['date_modification'])


@receiver(post_delete, sender=CommandeInfo)
def delete_livraisons_on_commande_info_delete(sender, instance, **kwargs):
    """
    Supprime les livraisons liées quand une commande informatique est supprimée
    """
    # Les livraisons seront automatiquement supprimées grâce à on_delete=CASCADE
    # Ce signal est juste pour le logging si nécessaire
    pass


@receiver(post_delete, sender=CommandeBureau)
def delete_livraisons_on_commande_bureau_delete(sender, instance, **kwargs):
    """
    Supprime les livraisons liées quand une commande bureau est supprimée
    """
    # Les livraisons seront automatiquement supprimées grâce à on_delete=CASCADE
    # Ce signal est juste pour le logging si nécessaire
    pass
