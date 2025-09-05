#!/usr/bin/env python3
"""
Script pour télécharger les modèles Hugging Face avec gestion des timeouts
et retry logic robuste.
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_huggingface_config():
    """Configure les paramètres Hugging Face pour éviter les timeouts"""
    os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '1800'  # 30 minutes
    os.environ['HF_HUB_DOWNLOAD_RETRY_DELAY'] = '10'  # 10 secondes entre les tentatives
    os.environ['HF_HUB_DOWNLOAD_RETRIES'] = '5'  # 5 tentatives
    os.environ['HF_HUB_DOWNLOAD_BACKOFF_FACTOR'] = '2'  # Facteur d'exponentiation
    os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
    
    # Configuration des caches
    cache_dir = Path.home() / '.cache' / 'huggingface'
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ['HF_HOME'] = str(cache_dir)
    os.environ['TRANSFORMERS_CACHE'] = str(cache_dir)
    os.environ['SENTENCE_TRANSFORMERS_HOME'] = str(cache_dir)

def download_model_with_retry(model_name: str, max_attempts: int = 5) -> bool:
    """
    Télécharge un modèle avec retry logic robuste
    
    Args:
        model_name: Nom du modèle à télécharger
        max_attempts: Nombre maximum de tentatives
        
    Returns:
        bool: True si le téléchargement a réussi, False sinon
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        logger.error(f"Impossible d'importer sentence_transformers: {e}")
        return False
    except Exception as e:
        logger.error(f"Erreur lors de l'import de sentence_transformers: {e}")
        return False
    
    for attempt in range(max_attempts):
        try:
            logger.info(f"Tentative {attempt + 1}/{max_attempts} pour télécharger {model_name}")
            
            # Téléchargement avec timeout personnalisé
            model = SentenceTransformer(model_name)
            
            # Test du modèle
            test_text = "Test du modèle"
            embeddings = model.encode(test_text)
            logger.info(f"Modèle {model_name} téléchargé et testé avec succès!")
            return True
            
        except Exception as e:
            logger.warning(f"Tentative {attempt + 1} échouée: {str(e)}")
            
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt * 10  # Attente exponentielle: 10s, 20s, 40s, 80s
                logger.info(f"Attente de {wait_time} secondes avant la prochaine tentative...")
                time.sleep(wait_time)
            else:
                logger.error(f"Toutes les tentatives ont échoué pour {model_name}")
                return False
    
    return False

def download_bart_model_with_retry(max_attempts: int = 3) -> bool:
    """
    Télécharge le modèle BART avec retry logic robuste
    
    Args:
        max_attempts: Nombre maximum de tentatives
        
    Returns:
        bool: True si le téléchargement a réussi, False sinon
    """
    try:
        from transformers import pipeline
    except ImportError as e:
        logger.error(f"Impossible d'importer transformers: {e}")
        return False
    except Exception as e:
        logger.error(f"Erreur lors de l'import de transformers: {e}")
        return False
    
    for attempt in range(max_attempts):
        try:
            logger.info(f"Tentative {attempt + 1}/{max_attempts} pour télécharger BART...")
            
            # Téléchargement du modèle BART
            model = pipeline(
                "zero-shot-classification", 
                model="facebook/bart-large-mnli",
                device=-1  # CPU only
            )
            
            # Test du modèle
            test_result = model("This is a test", ["positive", "negative"])
            logger.info(f"Modèle BART téléchargé et testé avec succès!")
            return True
            
        except Exception as e:
            logger.warning(f"Tentative {attempt + 1} échouée: {str(e)}")
            
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt * 15  # Attente exponentielle: 15s, 30s, 60s
                logger.info(f"Attente de {wait_time} secondes avant la prochaine tentative...")
                time.sleep(wait_time)
            else:
                logger.error(f"Toutes les tentatives ont échoué pour BART")
                return False
    
    return False

def main():
    """Fonction principale"""
    logger.info("Démarrage du téléchargement des modèles...")
    
    # Configuration
    setup_huggingface_config()
    
    # Modèles à télécharger
    models = [
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        # Ajoutez d'autres modèles si nécessaire
    ]
    
    success_count = 0
    total_models = len(models)
    
    # Télécharger les modèles sentence-transformers
    for model_name in models:
        logger.info(f"Téléchargement de {model_name}...")
        
        if download_model_with_retry(model_name):
            success_count += 1
            logger.info(f"✅ {model_name} téléchargé avec succès")
        else:
            logger.error(f"❌ Échec du téléchargement de {model_name}")
    
    # Télécharger le modèle BART séparément
    logger.info("Téléchargement du modèle BART...")
    if download_bart_model_with_retry():
        logger.info("✅ Modèle BART téléchargé avec succès")
    else:
        logger.warning("⚠️ Échec du téléchargement du modèle BART")
    
    logger.info(f"Résumé: {success_count}/{total_models} modèles sentence-transformers téléchargés avec succès")
    
    if success_count == total_models:
        logger.info("🎉 Tous les modèles ont été téléchargés avec succès!")
        return 0
    else:
        logger.warning("⚠️ Certains modèles n'ont pas pu être téléchargés")
        return 1

if __name__ == "__main__":
    sys.exit(main())
