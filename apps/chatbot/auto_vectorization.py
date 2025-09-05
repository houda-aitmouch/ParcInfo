# apps/chatbot/auto_vectorization.py
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.chatbot.models import DocumentVector

# Handle missing sentence_transformers gracefully
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

logger = logging.getLogger(__name__)

# Configuration complète des modèles avec priorités et champs spécifiques
MODEL_CONFIGS = {
    # Fournisseurs - Priorité haute
    'fournisseurs.Fournisseur': {
        'priority': 90,
        'fields': ['nom', 'if_fiscal', 'ice', 'registre_commerce', 'adresse'],
        'context': 'Informations fournisseur'
    },
    
    # Matériel informatique - Priorité maximale
    'materiel_informatique.MaterielInformatique': {
        'priority': 100,
        'fields': ['numero_serie', 'code_inventaire', 'statut', 'lieu_stockage', 'observation', 'marque', 'modele'],
        'context': 'Équipement informatique'
    },
    
    # Commandes informatique
    'commande_informatique.Commande': {
        'priority': 85,
        'fields': ['mode_passation', 'numero_commande', 'date_commande', 'date_reception', 'numero_facture'],
        'context': 'Commande informatique'
    },
    'commande_informatique.Designation': {
        'priority': 75,
        'fields': ['nom', 'description'],
        'context': 'Désignation équipement IT'
    },
    'commande_informatique.Description': {
        'priority': 70,
        'fields': ['description'],
        'context': 'Description équipement IT'
    },
    'commande_informatique.LigneCommande': {
        'priority': 80,
        'fields': ['quantite', 'prix_unitaire'],
        'context': 'Ligne commande IT'
    },
    
    # Matériel bureautique
    'materiel_bureautique.MaterielBureau': {
        'priority': 95,
        'fields': ['numero_serie', 'code_inventaire', 'statut', 'lieu_stockage', 'observation', 'marque', 'modele'],
        'context': 'Équipement bureautique'
    },
    
    # Commandes bureau
    'commande_bureau.CommandeBureau': {
        'priority': 80,
        'fields': ['mode_passation', 'numero_commande', 'date_commande', 'date_reception', 'numero_facture'],
        'context': 'Commande bureau'
    },
    'commande_bureau.DesignationBureau': {
        'priority': 70,
        'fields': ['nom', 'description'],
        'context': 'Désignation équipement bureau'
    },
    'commande_bureau.DescriptionBureau': {
        'priority': 65,
        'fields': ['description'],
        'context': 'Description équipement bureau'
    },
    'commande_bureau.LigneCommandeBureau': {
        'priority': 75,
        'fields': ['quantite', 'prix_unitaire'],
        'context': 'Ligne commande bureau'
    },
    
    # Demandes équipement
    'demande_equipement.DemandeEquipement': {
        'priority': 85,
        'fields': ['demandeur', 'date_demande', 'statut', 'categorie', 'type_article', 'type_demande'],
        'context': 'Demande équipement'
    },
    'demande_equipement.ArchiveDecharge': {
        'priority': 70,
        'fields': ['date_decharge', 'motif', 'statut'],
        'context': 'Archive décharge'
    },
    
    # Livraisons
    'livraison.Livraison': {
        'priority': 75,
        'fields': ['date_livraison', 'statut', 'transporteur', 'numero_suivi'],
        'context': 'Livraison'
    },
    
    # Utilisateurs (informations publiques uniquement)
    'users.CustomUser': {
        'priority': 60,
        'fields': ['username', 'first_name', 'last_name', 'email', 'is_active'],
        'context': 'Utilisateur système'
    },
    
    # DocumentVector pour indexation complète
    'chatbot.DocumentVector': {
        'priority': 50,
        'fields': ['content', 'model_name', 'app_label', 'source'],
        'context': 'Document vectorisé'
    },
    
    # Modèles manquants identifiés
    'chatbot.Interaction': {
        'priority': 55,
        'fields': ['query', 'response', 'intent', 'confidence'],
        'context': 'Interaction chatbot'
    }
}

def _get_model_content(obj, config):
    """Extrait le contenu pertinent d'un objet selon sa configuration"""
    try:
        fields = config.get('fields', [])
        context = config.get('context', 'Données')
        
        # Extraction des champs spécifiés
        content_parts = [f"Type: {context}"]
        
        for field in fields:
            if hasattr(obj, field):
                value = getattr(obj, field)
                if value is not None:
                    # Formatage spécial pour certains types
                    if hasattr(value, 'strftime'):  # Dates
                        value = value.strftime('%Y-%m-%d')
                    elif hasattr(value, '__str__'):
                        value = str(value)
                    
                    content_parts.append(f"{field}: {value}")
        
        # Ajout d'informations de relation si disponibles
        if hasattr(obj, 'fournisseur') and obj.fournisseur:
            try:
                if hasattr(obj.fournisseur, 'nom'):
                    content_parts.append(f"fournisseur: {obj.fournisseur.nom}")
                else:
                    content_parts.append(f"fournisseur: {str(obj.fournisseur)}")
            except Exception as e:
                logger.warning(f"Erreur relation fournisseur {obj.__class__.__name__}: {e}")
        
        content = " | ".join(content_parts)
        
        # Validation du contenu minimum
        if len(content.strip()) < 10:
            return None
            
        return content
        
    except Exception as e:
        logger.warning(f"Erreur extraction contenu {obj.__class__.__name__}: {e}")
        return None

def _vectorize_model_batch(model_class, config, embedding_model):
    """Vectorise un modèle par batch"""
    results = []
    model_key = f"{model_class._meta.app_label}.{model_class.__name__}"
    
    try:
        content_type = ContentType.objects.get_for_model(model_class)
        objects = list(model_class.objects.all())
        
        if not objects:
            logger.info(f"  {model_key}: 0 records (empty)")
            return results
        
        # Traitement par batch
        batch_size = 50
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            
            for obj in batch:
                content = _get_model_content(obj, config)
                if content:
                    try:
                        # Génération de l'embedding
                        embedding = embedding_model.encode(content).tolist()
                        
                        results.append({
                            'content_type': content_type,
                            'object_id': obj.pk,
                            'content': content,
                            'embedding': embedding,
                            'model_name': model_class.__name__,
                            'app_label': model_class._meta.app_label
                        })
                    except Exception as e:
                        logger.error(f"Erreur embedding {model_key} ID {obj.pk}: {e}")
        
        logger.info(f"  {model_key}: {len(results)} records processed")
        return results
        
    except Exception as e:
        logger.error(f"Erreur traitement modèle {model_key}: {e}")
        return results

def vectorize_all_models():
    """Vectorisation complète et optimisée de tous les modèles"""
    logger.info("🚀 Début de la vectorisation complète...")
    
    # Nettoyage des anciens vecteurs
    with transaction.atomic():
        deleted_count = DocumentVector.objects.all().delete()[0]
        logger.info(f"🗑️ Suppression de {deleted_count} anciens vecteurs")
    
    # Tri des modèles par priorité
    sorted_configs = sorted(MODEL_CONFIGS.items(), 
                           key=lambda x: x[1].get('priority', 50), 
                           reverse=True)
    
    total_processed = 0
    
    # Initialisation du modèle d'embedding (une seule fois)
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        logger.error("❌ La bibliothèque sentence_transformers n'est pas installée. Veuillez l'installer avec 'pip install sentence-transformers'.")
        return 0

    try:
        import torch
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device=device)
        logger.info(f"✅ Modèle d'embedding initialisé sur device: {device}")
    except Exception as e:
        logger.error(f"❌ Erreur initialisation embedding: {e}")
        return 0
    
    # Traitement séquentiel pour éviter les problèmes de mémoire
    for model_key, config in sorted_configs:
        try:
            app_label, model_name = model_key.split('.')
            model_class = apps.get_model(app_label, model_name)
            
            logger.info(f"🔄 Traitement {model_key}...")
            vectors = _vectorize_model_batch(model_class, config, embedding_model)
            
            # Sauvegarde immédiate par modèle
            if vectors:
                with transaction.atomic():
                    vector_objects = [
                        DocumentVector(**vector_data) for vector_data in vectors
                    ]
                    DocumentVector.objects.bulk_create(vector_objects, batch_size=50)
                    logger.info(f"  ✅ {len(vectors)} vecteurs sauvegardés pour {model_key}")
                    total_processed += len(vectors)
            else:
                logger.info(f"  ⚠️ Aucun vecteur généré pour {model_key}")
                
        except Exception as e:
            logger.error(f"❌ Erreur traitement {model_key}: {e}")
            continue
    
    # Statistiques finales
    final_count = DocumentVector.objects.count()
    logger.info(f"✅ Vectorisation terminée: {total_processed} documents indexés")
    logger.info(f"📊 Total vecteurs en base: {final_count}")
    
    return final_count