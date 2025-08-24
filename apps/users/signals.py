from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import NotificationDemande

@receiver(post_save, sender='demande_equipement.DemandeEquipement')
def creer_notification_demande(sender, instance, created, **kwargs):
    """
    Crée une notification automatique quand le statut d'une demande change
    """
    if not created:  # Seulement si c'est une mise à jour
        try:
            # Vérifier si le statut a changé
            if instance.tracker.has_changed('statut'):
                # Créer la notification
                titre = f"Demande {instance.numero_demande} - {instance.get_statut_display()}"
                
                # Message personnalisé selon le statut
                messages = {
                    'en_attente': f"Votre demande {instance.numero_demande} est en attente de traitement.",
                    'approuvee': f"Votre demande {instance.numero_demande} a été approuvée !",
                    'rejetee': f"Votre demande {instance.numero_demande} a été rejetée.",
                    'en_cours': f"Votre demande {instance.numero_demande} est en cours de traitement.",
                    'terminee': f"Votre demande {instance.numero_demande} a été traitée avec succès.",
                }
                
                message = messages.get(instance.statut, f"Le statut de votre demande {instance.numero_demande} a changé.")
                
                # Créer la notification
                NotificationDemande.objects.create(
                    utilisateur=instance.demandeur,
                    type_notification='demande_equipement',
                    titre=titre,
                    message=message,
                    statut_demande=instance.statut,
                    demande_id=instance.id
                )
                
        except Exception as e:
            # Logger l'erreur mais ne pas faire échouer le signal
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur lors de la création de la notification: {e}")

@receiver(post_save, sender='commande_bureau.CommandeBureau')
def creer_notification_commande_bureau(sender, instance, created, **kwargs):
    """
    Crée une notification pour les commandes bureautiques
    """
    if not created and hasattr(instance, 'tracker') and instance.tracker.has_changed('statut'):
        try:
            # Créer la notification pour l'utilisateur concerné
            if instance.utilisateur:
                titre = f"Commande Bureau {instance.numero_commande} - {instance.get_statut_display()}"
                message = f"Le statut de votre commande bureautique {instance.numero_commande} a changé."
                
                NotificationDemande.objects.create(
                    utilisateur=instance.utilisateur,
                    type_notification='demande_bureau',
                    titre=titre,
                    message=message,
                    statut_demande=instance.statut,
                    demande_id=instance.id
                )
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur lors de la création de la notification commande bureau: {e}")

@receiver(post_save, sender='commande_informatique.Commande')
def creer_notification_commande_info(sender, instance, created, **kwargs):
    """
    Crée une notification pour les commandes informatiques
    """
    if not created and hasattr(instance, 'tracker') and instance.tracker.has_changed('statut'):
        try:
            # Créer la notification pour l'utilisateur concerné
            if instance.utilisateur:
                titre = f"Commande IT {instance.numero_commande} - {instance.get_statut_display()}"
                message = f"Le statut de votre commande informatique {instance.numero_commande} a changé."
                
                NotificationDemande.objects.create(
                    utilisateur=instance.utilisateur,
                    type_notification='demande_equipement',
                    titre=titre,
                    message=message,
                    statut_demande=instance.statut,
                    demande_id=instance.id
                )
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur lors de la création de la notification commande info: {e}")
