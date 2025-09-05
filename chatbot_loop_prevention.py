#!/usr/bin/env python3
"""
Script pour prévenir les boucles infinies dans le chatbot ParcInfo
"""

import os
import sys
import time
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
from collections import deque

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChatbotLoopPrevention:
    """Classe pour prévenir les boucles infinies dans le chatbot"""
    
    def __init__(self, max_history: int = 10, max_repetitions: int = 3):
        self.max_history = max_history
        self.max_repetitions = max_repetitions
        self.conversation_history = deque(maxlen=max_history)
        self.response_cache = {}
        self.loop_detection_file = Path("/app/.cache/chatbot_loop_detection.json")
        self.loop_detection_file.parent.mkdir(parents=True, exist_ok=True)
        
    def _load_loop_detection_data(self) -> Dict:
        """Charge les données de détection de boucles"""
        if self.loop_detection_file.exists():
            try:
                with open(self.loop_detection_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Impossible de charger les données de détection de boucles: {e}")
        return {"loops_detected": 0, "last_reset": time.time()}
    
    def _save_loop_detection_data(self, data: Dict):
        """Sauvegarde les données de détection de boucles"""
        try:
            with open(self.loop_detection_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Impossible de sauvegarder les données de détection de boucles: {e}")
    
    def detect_loop(self, user_input: str, bot_response: str) -> bool:
        """Détecte si une boucle infinie est en cours"""
        # Ajouter à l'historique
        self.conversation_history.append({
            "user_input": user_input.lower().strip(),
            "bot_response": bot_response.lower().strip(),
            "timestamp": time.time()
        })
        
        # Vérifier les répétitions
        if len(self.conversation_history) >= self.max_repetitions:
            recent_responses = [item["bot_response"] for item in list(self.conversation_history)[-self.max_repetitions:]]
            
            # Vérifier si la même réponse se répète
            if len(set(recent_responses)) == 1:
                logger.warning(f"🔄 Boucle infinie détectée: réponse répétée '{recent_responses[0]}'")
                return True
            
            # Vérifier si l'utilisateur pose la même question
            recent_inputs = [item["user_input"] for item in list(self.conversation_history)[-self.max_repetitions:]]
            if len(set(recent_inputs)) == 1:
                logger.warning(f"🔄 Boucle infinie détectée: question répétée '{recent_inputs[0]}'")
                return True
        
        return False
    
    def get_loop_breaking_response(self) -> str:
        """Retourne une réponse pour briser la boucle"""
        responses = [
            "Je remarque que nous tournons en rond. Laissez-moi vous aider différemment. Pouvez-vous reformuler votre question ?",
            "Il semble que nous ayons un problème de communication. Essayons une approche différente. Que puis-je faire pour vous aider ?",
            "Je détecte une répétition dans notre conversation. Pouvez-vous me donner plus de détails sur ce que vous cherchez ?",
            "Nous semblons être dans une boucle. Laissez-moi vous proposer de l'aide alternative. Quel est votre besoin principal ?",
            "Je vais essayer de vous aider autrement. Pouvez-vous me donner un contexte plus spécifique ?"
        ]
        
        # Charger les données de détection
        data = self._load_loop_detection_data()
        data["loops_detected"] += 1
        data["last_reset"] = time.time()
        self._save_loop_detection_data(data)
        
        # Choisir une réponse basée sur le nombre de boucles détectées
        response_index = min(data["loops_detected"] - 1, len(responses) - 1)
        return responses[response_index]
    
    def reset_conversation(self):
        """Remet à zéro l'historique de conversation"""
        self.conversation_history.clear()
        logger.info("🔄 Historique de conversation remis à zéro")
    
    def get_conversation_stats(self) -> Dict:
        """Retourne les statistiques de la conversation"""
        data = self._load_loop_detection_data()
        return {
            "loops_detected": data.get("loops_detected", 0),
            "conversation_length": len(self.conversation_history),
            "last_reset": data.get("last_reset", 0)
        }

def test_loop_prevention():
    """Test de la prévention des boucles"""
    logger.info("🧪 Test de la prévention des boucles...")
    
    prevention = ChatbotLoopPrevention(max_history=5, max_repetitions=3)
    
    # Simuler une boucle
    test_cases = [
        ("Comment ça va ?", "Ça va bien, merci !"),
        ("Comment ça va ?", "Ça va bien, merci !"),
        ("Comment ça va ?", "Ça va bien, merci !"),
    ]
    
    for user_input, bot_response in test_cases:
        is_loop = prevention.detect_loop(user_input, bot_response)
        if is_loop:
            breaking_response = prevention.get_loop_breaking_response()
            logger.info(f"🛑 Boucle détectée ! Réponse de rupture: {breaking_response}")
            break
    
    # Afficher les statistiques
    stats = prevention.get_conversation_stats()
    logger.info(f"📊 Statistiques: {stats}")

def main():
    """Fonction principale"""
    logger.info("🚀 Initialisation de la prévention des boucles du chatbot...")
    
    # Test de la fonctionnalité
    test_loop_prevention()
    
    logger.info("✅ Prévention des boucles initialisée avec succès")

if __name__ == "__main__":
    main()
