#!/usr/bin/env python3
"""
Test simple du système RAG pour ParcInfo
Teste sentence-transformers sans Django
"""

def test_sentence_transformers():
    """Test de sentence-transformers"""
    print("🧪 Test de sentence-transformers...")
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Import de sentence_transformers réussi")
        
        # Test d'initialisation du modèle
        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ Modèle d'embedding initialisé")
        
        # Test d'encodage simple
        sentences = ["Bonjour le monde", "Hello world", "Salut"]
        embeddings = model.encode(sentences)
        print(f"✅ Encodage réussi: {embeddings.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur sentence_transformers: {e}")
        return False

def test_rag_components():
    """Test des composants RAG"""
    print("\n🧪 Test des composants RAG...")
    
    try:
        # Test d'import des modules RAG
        import sys
        import os
        
        # Ajouter le répertoire du projet
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        # Test d'import des modèles
        from apps.chatbot.rag_manager import RAGManager
        print("✅ RAGManager importé")
        
        from apps.chatbot.core_chatbot import ParcInfoChatbot
        print("✅ ParcInfoChatbot importé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur composants RAG: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test RAG Simple ParcInfo")
    print("=" * 40)
    
    # Test sentence-transformers
    if test_sentence_transformers():
        print("\n✅ sentence-transformers opérationnel")
        
        # Test des composants RAG
        if test_rag_components():
            print("\n🎉 Tous les tests RAG sont réussis !")
            print("\n💡 Le chatbot peut maintenant utiliser RAG !")
        else:
            print("\n❌ Test des composants RAG échoué")
    else:
        print("\n❌ sentence-transformers non opérationnel")
