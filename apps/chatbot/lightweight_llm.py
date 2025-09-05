#!/usr/bin/env python3
"""
Module LLM léger pour remplacer Ollama dans les fallbacks
Utilise DistilBERT pour des réponses rapides et efficaces
"""

import os
import json
import logging
import time
from typing import Dict, Any, Optional, List
import torch
from transformers import (
    DistilBertTokenizer, 
    DistilBertForSequenceClassification,
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class LightweightLLM:
    """LLM léger pour remplacer Ollama dans les fallbacks"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.embedding_model = None
        self.qa_pipeline = None
        self.classification_pipeline = None
        
        # Configuration pour la performance
        self.max_length = 512
        self.batch_size = 8
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        
        # Cache pour les réponses fréquentes
        self.response_cache = {}
        self.cache_ttl = 1800  # 30 minutes
        
        logger.info(f"Initialisation du LLM léger sur {self.device}")
        
    def initialize(self) -> bool:
        """Initialise le modèle léger"""
        try:
            logger.info(f"Chargement du modèle: {self.model_name}")
            
            # Charger le tokenizer et le modèle
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
            self.model = DistilBertForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=2  # Binary classification pour fallback
            )
            
            # Déplacer sur le device approprié
            self.model.to(self.device)
            self.model.eval()
            
            # Initialiser le pipeline de classification
            self.classification_pipeline = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            # Initialiser le modèle d'embeddings
            self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
            
            logger.info("LLM léger initialisé avec succès!")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du LLM léger: {e}")
            return False
    
    def generate_fallback_response(self, query: str, context: List[str] = None) -> str:
        """Génère une réponse de fallback rapide"""
        try:
            start_time = time.time()
            
            # Vérifier le cache
            cache_key = f"fallback:{hash(query)}"
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                    logger.info("Cache hit pour la réponse de fallback")
                    return cache_entry['response']
            
            # Générer la réponse
            if context and len(context) > 0:
                response = self._generate_contextual_response(query, context)
            else:
                response = self._generate_generic_response(query)
            
            # Mettre en cache
            self.response_cache[cache_key] = {
                'response': response,
                'timestamp': time.time()
            }
            
            processing_time = time.time() - start_time
            logger.info(f"Réponse de fallback générée en {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse de fallback: {e}")
            return self._get_emergency_fallback_response(query)
    
    def generate_response(self, query: str, context: List[str] = None) -> str:
        """Génère une réponse (alias pour generate_fallback_response)"""
        return self.generate_fallback_response(query, context)
    
    def _generate_contextual_response(self, query: str, context: List[str]) -> str:
        """Génère une réponse basée sur le contexte"""
        try:
            # Analyser la requête pour déterminer le type de réponse
            query_lower = query.lower()
            
            if any(word in query_lower for word in ['fournisseur', 'supplier']):
                return self._generate_supplier_response(query, context)
            elif any(word in query_lower for word in ['matériel', 'material', 'équipement']):
                return self._generate_material_response(query, context)
            elif any(word in query_lower for word in ['commande', 'order']):
                return self._generate_order_response(query, context)
            elif any(word in query_lower for word in ['livraison', 'delivery']):
                return self._generate_delivery_response(query, context)
            elif any(word in query_lower for word in ['utilisateur', 'user']):
                return self._generate_user_response(query, context)
            else:
                return self._generate_generic_response(query)
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération contextuelle: {e}")
            return self._generate_generic_response(query)
    
    def _generate_supplier_response(self, query: str, context: List[str]) -> str:
        """Génère une réponse spécifique aux fournisseurs"""
        try:
            # Extraire les informations pertinentes du contexte
            supplier_info = []
            for ctx in context:
                if 'fournisseur' in ctx.lower() or 'supplier' in ctx.lower():
                    supplier_info.append(ctx)
            
            if supplier_info:
                response = f"**🏢 Informations sur les Fournisseurs**\n\n"
                response += "Basé sur les données disponibles :\n\n"
                
                for info in supplier_info[:3]:  # Limiter à 3 informations
                    response += f"• {info}\n"
                
                response += "\n*Note : Ces informations sont extraites de la base de données.*"
            else:
                response = "Je n'ai pas trouvé d'informations spécifiques sur les fournisseurs dans le contexte fourni."
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse fournisseur: {e}")
            return "Je n'ai pas pu récupérer les informations sur les fournisseurs."
    
    def _generate_material_response(self, query: str, context: List[str]) -> str:
        """Génère une réponse spécifique aux matériels"""
        try:
            # Extraire les informations pertinentes du contexte
            material_info = []
            for ctx in context:
                if any(word in ctx.lower() for word in ['matériel', 'material', 'équipement', 'inventaire']):
                    material_info.append(ctx)
            
            if material_info:
                response = f"**🖥️ Informations sur les Matériels**\n\n"
                response += "Basé sur les données disponibles :\n\n"
                
                for info in material_info[:3]:  # Limiter à 3 informations
                    response += f"• {info}\n"
                
                response += "\n*Note : Ces informations sont extraites de la base de données.*"
            else:
                response = "Je n'ai pas trouvé d'informations spécifiques sur les matériels dans le contexte fourni."
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse matériel: {e}")
            return "Je n'ai pas pu récupérer les informations sur les matériels."
    
    def _generate_order_response(self, query: str, context: List[str]) -> str:
        """Génère une réponse spécifique aux commandes"""
        try:
            # Extraire les informations pertinentes du contexte
            order_info = []
            for ctx in context:
                if any(word in ctx.lower() for word in ['commande', 'order', 'bc23', 'bc24']):
                    order_info.append(ctx)
            
            if order_info:
                response = f"**📋 Informations sur les Commandes**\n\n"
                response += "Basé sur les données disponibles :\n\n"
                
                for info in order_info[:3]:  # Limiter à 3 informations
                    response += f"• {info}\n"
                
                response += "\n*Note : Ces informations sont extraites de la base de données.*"
            else:
                response = "Je n'ai pas trouvé d'informations spécifiques sur les commandes dans le contexte fourni."
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse commande: {e}")
            return "Je n'ai pas pu récupérer les informations sur les commandes."
    
    def _generate_delivery_response(self, query: str, context: List[str]) -> str:
        """Génère une réponse spécifique aux livraisons"""
        try:
            # Extraire les informations pertinentes du contexte
            delivery_info = []
            for ctx in context:
                if any(word in ctx.lower() for word in ['livraison', 'delivery', 'livré', 'arrivé']):
                    delivery_info.append(ctx)
            
            if delivery_info:
                response = f"**🚚 Informations sur les Livraisons**\n\n"
                response += "Basé sur les données disponibles :\n\n"
                
                for info in delivery_info[:3]:  # Limiter à 3 informations
                    response += f"• {info}\n"
                
                response += "\n*Note : Ces informations sont extraites de la base de données.*"
            else:
                response = "Je n'ai pas trouvé d'informations spécifiques sur les livraisons dans le contexte fourni."
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse livraison: {e}")
            return "Je n'ai pas pu récupérer les informations sur les livraisons."
    
    def _generate_user_response(self, query: str, context: List[str]) -> str:
        """Génère une réponse spécifique aux utilisateurs"""
        try:
            # Extraire les informations pertinentes du contexte
            user_info = []
            for ctx in context:
                if any(word in ctx.lower() for word in ['utilisateur', 'user', 'gestionnaire', 'employé']):
                    user_info.append(ctx)
            
            if user_info:
                response = f"**👤 Informations sur les Utilisateurs**\n\n"
                response += "Basé sur les données disponibles :\n\n"
                
                for info in user_info[:3]:  # Limiter à 3 informations
                    response += f"• {info}\n"
                
                response += "\n*Note : Ces informations sont extraites de la base de données.*"
            else:
                response = "Je n'ai pas trouvé d'informations spécifiques sur les utilisateurs dans le contexte fourni."
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse utilisateur: {e}")
            return "Je n'ai pas pu récupérer les informations sur les utilisateurs."
    
    def _generate_generic_response(self, query: str) -> str:
        """Génère une réponse générique de fallback"""
        try:
            query_lower = query.lower()
            
            # Réponses spécifiques selon le type de requête
            if any(word in query_lower for word in ['prix', 'coût', 'montant']):
                return ("Je n'ai pas pu récupérer les informations de prix demandées. "
                        "Les prix sont généralement associés aux commandes et non aux matériels individuels. "
                        "Voulez-vous que je recherche les commandes correspondantes ?")
            
            elif any(word in query_lower for word in ['log', 'historique', 'activité']):
                return ("Les logs d'activité et l'historique détaillé ne sont pas disponibles "
                        "dans la base de données actuelle. Ces informations ne sont pas stockées dans le système.")
            
            elif any(word in query_lower for word in ['statut', 'état']):
                return ("Je n'ai pas pu récupérer le statut demandé. "
                        "Vérifiez que l'élément existe bien dans la base de données "
                        "ou reformulez votre demande.")
            
            else:
                return ("Je n'ai pas pu traiter votre demande avec précision. "
                        "Essayez de reformuler votre question ou contactez l'administrateur "
                        "pour obtenir de l'aide.")
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse générique: {e}")
            return "Je n'ai pas pu traiter votre demande. Veuillez réessayer."
    
    def _get_emergency_fallback_response(self, query: str) -> str:
        """Réponse d'urgence en cas d'erreur"""
        return ("Je rencontre des difficultés techniques pour traiter votre demande. "
                "Veuillez réessayer dans quelques instants ou contacter l'administrateur.")
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """Classifie l'intent d'un texte"""
        try:
            if not self.classification_pipeline:
                return {"intent": "unknown", "confidence": 0.0}
            
            # Classification binaire (fallback vs non-fallback)
            result = self.classification_pipeline(text)
            
            # Interpréter le résultat
            if result[0]['label'] == 'LABEL_0':
                intent = "fallback"
                confidence = 1.0 - result[0]['score']
            else:
                intent = "non_fallback"
                confidence = result[0]['score']
            
            return {
                "intent": intent,
                "confidence": confidence,
                "method": "lightweight_llm"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la classification: {e}")
            return {"intent": "fallback", "confidence": 0.0, "method": "error"}
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Génère les embeddings pour une liste de textes"""
        try:
            if not self.embedding_model:
                return np.array([])
            
            embeddings = self.embedding_model.encode(texts, batch_size=self.batch_size)
            return embeddings
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération d'embeddings: {e}")
            return np.array([])
    
    def cleanup(self):
        """Nettoie les ressources"""
        try:
            if self.model:
                del self.model
            if self.tokenizer:
                del self.tokenizer
            if self.embedding_model:
                del self.embedding_model
            
            # Vider le cache
            self.response_cache.clear()
            
            # Forcer le garbage collection
            import gc
            gc.collect()
            
            logger.info("Ressources du LLM léger nettoyées")
            
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {e}")

def main():
    """Fonction principale pour tester le LLM léger"""
    logging.basicConfig(level=logging.INFO)
    
    # Initialiser le LLM léger
    llm = LightweightLLM()
    
    if llm.initialize():
        print("✅ LLM léger initialisé avec succès!")
        
        # Tester la génération de réponses
        test_queries = [
            "Code inventaire de la Baie",
            "Fournisseur de la commande BC23",
            "Quels sont les prix des matériels informatiques ?"
        ]
        
        for query in test_queries:
            print(f"\n--- Test: {query} ---")
            response = llm.generate_fallback_response(query)
            print(f"Réponse: {response}")
        
        # Nettoyer
        llm.cleanup()
    else:
        print("❌ Échec de l'initialisation du LLM léger")

if __name__ == "__main__":
    main()
