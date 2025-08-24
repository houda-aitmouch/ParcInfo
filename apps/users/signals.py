from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import NotificationDemande

@receiver(post_save, sender='demande_equipement.DemandeEquipement')
def creer_notification_demande(sender, instance, created, **kwargs):
    """
    Crée une notification automatique pour les employés quand le statut d'une demande change
    """
    if not created:  # Seulement si c'est une mise à jour
        try:
            # Vérifier si le statut a changé
            if hasattr(instance, 'tracker') and instance.tracker.has_changed('statut'):
                # Créer la notification
                titre = f"Demande {instance.numero_demande} - {instance.get_statut_display()}"
                
                # Messages personnalisés selon le statut - plus détaillés pour les employés
                messages = {
                    'en_attente': f"Votre demande {instance.numero_demande} est en attente de validation par la hiérarchie.",
                    'approuvee': f"🎉 Votre demande {instance.numero_demande} a été approuvée ! L'équipement sera commandé prochainement.",
                    'rejetee': f"❌ Votre demande {instance.numero_demande} a été rejetée. Contactez votre responsable pour plus de détails.",
                    'en_cours': f"🔄 Votre demande {instance.numero_demande} est en cours de traitement. Nous vous tiendrons informé.",
                    'terminee': f"✅ Votre demande {instance.numero_demande} a été traitée avec succès. L'équipement est disponible.",
                    'en_attente_signature': f"✍️ Votre demande {instance.numero_demande} nécessite votre signature pour validation.",
                    'signature_requise': f"✍️ Signature requise pour votre demande {instance.numero_demande}. Veuillez la signer rapidement.",
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

# Signal pour les demandes nécessitant une signature
@receiver(post_save, sender='demande_equipement.DemandeEquipement')
def creer_notification_signature(sender, instance, created, **kwargs):
    """
    Crée une notification spéciale quand une demande nécessite une signature
    """
    if not created:
        try:
            # Vérifier si la demande nécessite une signature
            if hasattr(instance, 'signature_requise') and instance.signature_requise:
                # Vérifier si on n'a pas déjà créé une notification pour ce statut
                if not NotificationDemande.objects.filter(
                    utilisateur=instance.demandeur,
                    demande_id=instance.id,
                    statut_demande='signature_requise'
                ).exists():
                    
                    titre = f"✍️ Signature requise - Demande {instance.numero_demande}"
                    message = f"Votre demande {instance.numero_demande} nécessite votre signature pour être traitée. Veuillez la signer rapidement."
                    
                    NotificationDemande.objects.create(
                        utilisateur=instance.demandeur,
                        type_notification='demande_equipement',
                        titre=titre,
                        message=message,
                        statut_demande='signature_requise',
                        demande_id=instance.id
                    )
                    
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur lors de la création de la notification de signature: {e}")

# Suppression des notifications pour les commandes - les employés ne doivent recevoir que des notifications pour leurs demandes
