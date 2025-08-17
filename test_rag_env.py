#!/usr/bin/env python3
"""
Test RAG avec environnement virtuel pour ParcInfo
"""

import subprocess
import sys
import os

def test_rag_with_venv():
    """Test du RAG avec l'environnement virtuel"""
    print("🚀 Test RAG avec environnement virtuel")
    print("=" * 50)
    
    # Chemin vers l'environnement virtuel
    venv_python = "rag_env/bin/python"
    
    # Test sentence-transformers
    print("🧪 Test de sentence-transformers...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            "from sentence_transformers import SentenceTransformer; print('✅ Import réussi')"
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}")
        return False
    
    # Test d'initialisation du modèle
    print("\n🧪 Test d'initialisation du modèle...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
print('✅ Modèle initialisé')
print(f'Modèle: {model}')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}")
        return False
    
    # Test d'encodage
    print("\n🧪 Test d'encodage...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
sentences = ["Bonjour le monde", "Hello world", "Salut"]
embeddings = model.encode(sentences)
print('✅ Encodage réussi')
print(f'Forme des embeddings: {embeddings.shape}')
print(f'Nombre de phrases: {len(sentences)}')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}")
        return False
    
    return True

def test_rag_components():
    """Test des composants RAG Django"""
    print("\n🧪 Test des composants RAG Django...")
    
    # Vérifier que Django est installé
    try:
        result = subprocess.run([
            "rag_env/bin/python", "-c", 
            "import django; print(f'✅ Django {django.get_version()} installé')"
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Django non disponible: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    if test_rag_with_venv():
        print("\n✅ Tests RAG de base réussis !")
        
        if test_rag_components():
            print("\n🎉 Tous les tests RAG sont réussis !")
            print("\n💡 Le chatbot peut maintenant utiliser RAG avec l'environnement virtuel !")
            print("\n📝 Pour utiliser RAG dans Django, activez l'environnement virtuel :")
            print("   source rag_env/bin/activate")
            print("   python manage.py runserver")
        else:
            print("\n❌ Test des composants Django échoué")
    else:
        print("\n❌ Tests RAG de base échoués")
