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
            if hasattr(instance, '_statut_changed') and instance._statut_changed:
                
                # VÉRIFIER QUE LE DEMANDEUR EST UN EMPLOYÉ (pas un admin/gestionnaire)
                demandeur = instance.demandeur
                if demandeur.is_superuser or demandeur.groups.filter(name__in=['Super Admin', 'Gestionnaire Informatique', 'Gestionnaire Bureau']).exists():
                    # Ne pas créer de notification pour les administrateurs/gestionnaires
                    return
                
                # Construire le titre avec plus d'informations contextuelles
                titre = f"Demande D{instance.id:03d} - {instance.get_statut_display()}"
                
                # Construire un message détaillé avec les informations de la demande
                def get_demande_details():
                    """Retourne les détails de la demande pour le message"""
                    details = []
                    
                    # Type d'article
                    if instance.type_article == 'materiel':
                        details.append("matériel")
                        if instance.categorie == 'informatique':
                            details.append("informatique")
                        elif instance.categorie == 'bureau':
                            details.append("de bureau")
                    elif instance.type_article == 'fourniture':
                        details.append("fourniture")
                        if instance.fourniture:
                            details.append(f"'{instance.fourniture.nom}'")
                    
                    # Désignation pour les matériels
                    if instance.type_article == 'materiel' and instance.designation:
                        details.append(f"({instance.designation.nom})")
                    
                    # Type de demande
                    if instance.type_demande != 'nouveau':
                        details.append(f"- {instance.get_type_demande_display().lower()}")
                    
                    return " ".join(details)
                
                demande_details = get_demande_details()
                
                # Messages personnalisés selon le statut - plus détaillés pour les employés
                messages = {
                    'en_attente': f"Votre demande de {demande_details} est en attente de validation par la hiérarchie.",
                    'approuvee': f"🎉 Votre demande de {demande_details} a été approuvée ! Veuillez signer la décharge pour recevoir l'équipement.",
                    'rejetee': f"❌ Votre demande de {demande_details} a été rejetée. Contactez votre responsable pour plus de détails.",
                    'en_cours': f"🔄 Votre demande de {demande_details} est en cours de traitement. Nous vous tiendrons informé.",
                    'terminee': f"✅ Votre demande de {demande_details} a été traitée avec succès. L'équipement est disponible.",
                    'en_attente_signature': f"✍️ Votre demande de {demande_details} nécessite votre signature pour validation.",
                    'signature_requise': f"✍️ Signature requise pour votre demande de {demande_details}. Veuillez la signer rapidement.",
                }
                
                message = messages.get(instance.statut, f"Le statut de votre demande de {demande_details} a changé.")
                
                # Créer la notification
                NotificationDemande.objects.create(
                    utilisateur=instance.demandeur,
                    type_notification='demande_equipement',
                    titre=titre,
                    message=message,
                    statut_demande=instance.statut,
                    demande_id=instance.id
                )
                
                # Nettoyer les attributs temporaires
                if hasattr(instance, '_statut_changed'):
                    delattr(instance, '_statut_changed')
                if hasattr(instance, '_old_statut'):
                    delattr(instance, '_old_statut')
                
        except Exception as e:
            # Logger l'erreur mais ne pas faire échouer le signal
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur lors de la création de la notification: {e}")

# Signal pour les demandes nécessitant une signature
@receiver(post_save, sender='demande_equipement.DemandeEquipement')
def creer_notification_signature(sender, instance, created, **kwargs):
    """
    Crée une notification spéciale UNIQUEMENT pour les employés quand une demande nécessite une signature
    """
    if not created:
        try:
            # Vérifier si la demande nécessite une signature
            if hasattr(instance, 'signature_requise') and instance.signature_requise:
                
                # VÉRIFIER QUE LE DEMANDEUR EST UN EMPLOYÉ (pas un admin/gestionnaire)
                demandeur = instance.demandeur
                if demandeur.is_superuser or demandeur.groups.filter(name__in=['Super Admin', 'Gestionnaire Informatique', 'Gestionnaire Bureau']).exists():
                    # Ne pas créer de notification pour les administrateurs/gestionnaires
                    return
                
                # Vérifier si on n'a pas déjà créé une notification pour ce statut
                if not NotificationDemande.objects.filter(
                    utilisateur=instance.demandeur,
                    demande_id=instance.id,
                    statut_demande='signature_requise'
                ).exists():
                    
                    # Construire les détails de la demande
                    def get_demande_details():
                        """Retourne les détails de la demande pour le message"""
                        details = []
                        
                        # Type d'article
                        if instance.type_article == 'materiel':
                            details.append("matériel")
                            if instance.categorie == 'informatique':
                                details.append("informatique")
                            elif instance.categorie == 'bureau':
                                details.append("de bureau")
                        elif instance.type_article == 'fourniture':
                            details.append("fourniture")
                            if instance.fourniture:
                                details.append(f"'{instance.fourniture.nom}'")
                        
                        # Désignation pour les matériels
                        if instance.type_article == 'materiel' and instance.designation:
                            details.append(f"({instance.designation.nom})")
                        
                        # Type de demande
                        if instance.type_demande != 'nouveau':
                            details.append(f"- {instance.get_type_demande_display().lower()}")
                        
                        return " ".join(details)
                    
                    demande_details = get_demande_details()
                    
                    titre = f"✍️ Signature requise - Demande D{instance.id:03d}"
                    message = f"Votre demande de {demande_details} nécessite votre signature pour être traitée. Veuillez la signer rapidement."
                    
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
