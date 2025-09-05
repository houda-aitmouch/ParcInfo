#!/usr/bin/env python3
"""
Script pour télécharger manuellement les modèles Hugging Face
et les placer dans le bon répertoire de cache.
"""

import os
import sys
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_file_with_retry(url: str, filepath: Path, max_attempts: int = 5) -> bool:
    """
    Télécharge un fichier avec retry logic et gestion des timeouts
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    for attempt in range(max_attempts):
        try:
            logger.info(f"Tentative {attempt + 1}/{max_attempts} pour télécharger {url}")
            
            # Créer le répertoire parent si nécessaire
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Téléchargement avec timeout progressif
            timeout = (attempt + 1) * 60  # 60s, 120s, 180s, 240s, 300s
            
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()
            
            # Téléchargement par chunks pour éviter les timeouts
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Afficher le progrès
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if downloaded % (chunk_size * 100) == 0:  # Afficher tous les 100 chunks
                                logger.info(f"Progrès: {progress:.1f}% ({downloaded}/{total_size} bytes)")
            
            logger.info(f"✅ Fichier téléchargé: {filepath}")
            return True
            
        except Exception as e:
            logger.warning(f"Tentative {attempt + 1} échouée: {str(e)}")
            
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt * 10  # Attente exponentielle
                logger.info(f"Attente de {wait_time} secondes...")
                time.sleep(wait_time)
            else:
                logger.error(f"Toutes les tentatives ont échoué pour {url}")
                return False
    
    return False

def get_model_files(model_name: str) -> list:
    """
    Récupère la liste des fichiers du modèle depuis l'API Hugging Face
    """
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        
        # Récupérer les informations du modèle
        model_info = api.model_info(model_name)
        
        files = []
        for file_info in model_info.siblings:
            if file_info.rfilename.endswith(('.bin', '.safetensors', '.json', '.txt')):
                files.append({
                    'filename': file_info.rfilename,
                    'url': f"https://huggingface.co/{model_name}/resolve/main/{file_info.rfilename}",
                    'size': file_info.size
                })
        
        return files
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des fichiers du modèle: {e}")
        return []

def download_model_manually(model_name: str) -> bool:
    """
    Télécharge manuellement tous les fichiers d'un modèle
    """
    logger.info(f"Téléchargement manuel de {model_name}...")
    
    # Configuration des répertoires de cache
    cache_dir = Path.home() / '.cache' / 'huggingface' / 'hub'
    model_cache_dir = cache_dir / f"models--{model_name.replace('/', '--')}"
    
    # Récupérer la liste des fichiers
    files = get_model_files(model_name)
    
    if not files:
        logger.error("Impossible de récupérer la liste des fichiers du modèle")
        return False
    
    logger.info(f"Fichiers à télécharger: {len(files)}")
    
    success_count = 0
    for file_info in files:
        file_path = model_cache_dir / "snapshots" / "main" / file_info['filename']
        
        if file_path.exists():
            logger.info(f"Fichier déjà présent: {file_info['filename']}")
            success_count += 1
            continue
        
        if download_file_with_retry(file_info['url'], file_path):
            success_count += 1
    
    logger.info(f"Téléchargement terminé: {success_count}/{len(files)} fichiers")
    return success_count == len(files)

def main():
    """Fonction principale"""
    logger.info("Démarrage du téléchargement manuel des modèles...")
    
    # Modèles à télécharger
    models = [
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    ]
    
    success_count = 0
    for model_name in models:
        if download_model_manually(model_name):
            success_count += 1
            logger.info(f"✅ {model_name} téléchargé avec succès")
        else:
            logger.error(f"❌ Échec du téléchargement de {model_name}")
    
    if success_count == len(models):
        logger.info("🎉 Tous les modèles ont été téléchargés avec succès!")
        return 0
    else:
        logger.warning("⚠️ Certains modèles n'ont pas pu être téléchargés")
        return 1

if __name__ == "__main__":
    sys.exit(main())
