#!/usr/bin/env python3
"""
Script pour vérifier que le modèle BART est bien téléchargé et fonctionnel
"""

import os
import sys
import time
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_bart_model():
    """Vérifie que le modèle BART est téléchargé et fonctionnel"""
    try:
        from transformers import pipeline
        logger.info("✅ Import de transformers réussi")
    except ImportError as e:
        logger.error(f"❌ Impossible d'importer transformers: {e}")
        return False
    
    model_name = "facebook/bart-large-mnli"
    
    try:
        logger.info(f"🔍 Vérification du modèle BART: {model_name}")
        
        # Charger le modèle
        model = pipeline(
            "zero-shot-classification", 
            model=model_name,
            device=-1  # CPU only
        )
        
        logger.info("✅ Modèle BART chargé avec succès")
        
        # Test du modèle
        test_text = "I need help with my computer"
        test_labels = ["technical support", "general inquiry", "complaint"]
        
        result = model(test_text, test_labels)
        
        logger.info(f"✅ Test du modèle réussi:")
        logger.info(f"   Texte: {test_text}")
        logger.info(f"   Labels: {test_labels}")
        logger.info(f"   Résultat: {result['labels'][0]} (score: {result['scores'][0]:.3f})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification du modèle BART: {e}")
        return False

def verify_sentence_transformer():
    """Vérifie que le modèle sentence-transformers est téléchargé et fonctionnel"""
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("✅ Import de sentence_transformers réussi")
    except ImportError as e:
        logger.error(f"❌ Impossible d'importer sentence_transformers: {e}")
        return False
    
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    try:
        logger.info(f"🔍 Vérification du modèle sentence-transformers: {model_name}")
        
        # Charger le modèle
        model = SentenceTransformer(model_name)
        
        logger.info("✅ Modèle sentence-transformers chargé avec succès")
        
        # Test du modèle
        test_texts = ["Bonjour, comment allez-vous ?", "Hello, how are you?"]
        embeddings = model.encode(test_texts)
        
        logger.info(f"✅ Test du modèle réussi:")
        logger.info(f"   Textes: {test_texts}")
        logger.info(f"   Embeddings shape: {embeddings.shape}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification du modèle sentence-transformers: {e}")
        return False

def check_cache_directory():
    """Vérifie le répertoire de cache des modèles"""
    cache_dir = Path("/app/.cache/huggingface")
    
    if not cache_dir.exists():
        logger.warning(f"⚠️ Répertoire de cache n'existe pas: {cache_dir}")
        cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Répertoire de cache créé: {cache_dir}")
    else:
        logger.info(f"✅ Répertoire de cache existe: {cache_dir}")
    
    # Vérifier l'espace disque
    try:
        import shutil
        total, used, free = shutil.disk_usage(cache_dir)
        logger.info(f"💾 Espace disque - Total: {total//1024//1024//1024}GB, Libre: {free//1024//1024//1024}GB")
    except Exception as e:
        logger.warning(f"⚠️ Impossible de vérifier l'espace disque: {e}")

def main():
    """Fonction principale de vérification"""
    logger.info("🚀 Vérification des modèles téléchargés...")
    
    # Vérifier le répertoire de cache
    check_cache_directory()
    
    # Vérifier les modèles
    bart_ok = verify_bart_model()
    st_ok = verify_sentence_transformer()
    
    # Résumé
    logger.info("📊 Résumé de la vérification:")
    logger.info(f"   BART: {'✅ OK' if bart_ok else '❌ ÉCHEC'}")
    logger.info(f"   Sentence Transformers: {'✅ OK' if st_ok else '❌ ÉCHEC'}")
    
    if bart_ok and st_ok:
        logger.info("🎉 Tous les modèles sont fonctionnels!")
        return 0
    else:
        logger.error("💥 Certains modèles ne fonctionnent pas correctement")
        return 1

if __name__ == "__main__":
    sys.exit(main())
