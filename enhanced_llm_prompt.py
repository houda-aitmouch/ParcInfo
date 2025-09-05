#!/usr/bin/env python3
"""
Module de prompt LLM renforcé pour éliminer les hallucinations
Intègre des instructions strictes et des vérifications de sécurité
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedLLMPrompt:
    """Gestionnaire de prompts LLM renforcés pour éliminer les hallucinations"""
    
    def __init__(self):
        self.base_prompt = self._get_base_prompt()
        self.safety_instructions = self._get_safety_instructions()
        self.verification_patterns = self._get_verification_patterns()
        self.response_templates = self._get_response_templates()
        
    def _get_base_prompt(self) -> str:
        """Prompt de base pour le LLM"""
        return """
Tu es un assistant IA spécialisé dans la gestion de parc informatique (ParcInfo).
Tu dois répondre UNIQUEMENT aux questions sur la base des informations fournies dans le contexte.

RÈGLES STRICTES:
1. NE JAMAIS inventer d'informations
2. NE JAMAIS mentionner de fournisseurs, codes, ou données non présents dans le contexte
3. Si une information n'est pas dans le contexte, dire "Je n'ai pas cette information dans ma base de données"
4. Utiliser UNIQUEMENT les données fournies
5. Répondre de manière factuelle et précise

CONTEXTE FOURNI:
{context}

QUESTION UTILISATEUR:
{query}

RÉPONSE (basée UNIQUEMENT sur le contexte):
"""
    
    def _get_safety_instructions(self) -> str:
        """Instructions de sécurité pour éviter les hallucinations"""
        return """
VÉRIFICATIONS DE SÉCURITÉ:
- Vérifier que tous les noms de fournisseurs mentionnés sont dans le contexte
- Vérifier que tous les codes inventaire mentionnés sont dans le contexte
- Vérifier que toutes les dates mentionnées sont cohérentes
- Vérifier que tous les montants mentionnés sont dans le contexte
- Si une vérification échoue, ne pas mentionner cette information

FORMAT DE RÉPONSE SÉCURISÉ:
1. Informations vérifiées dans le contexte
2. Limites des informations disponibles
3. Suggestions d'actions si nécessaire
"""
    
    def _get_verification_patterns(self) -> Dict[str, str]:
        """Patterns de vérification pour détecter les hallucinations"""
        return {
            "supplier_names": r"\b[A-Z][A-Z\s]+\s+(?:ICE|SARL|SA|SAS)\b",
            "inventory_codes": r"\b[A-Z]{2,3}\d{2,4}\b",
            "dates": r"\b\d{4}-\d{2}-\d{2}\b",
            "amounts": r"\b\d+(?:\.\d{2})?\s*(?:€|EUR|DH|MAD)\b",
            "generic_placeholders": r"\[.*?\]|\(.*?\)|\{.*?\}",
            "unverified_entities": r"\b(?:ID|CODE|NOM|DATE|MONTANT)\b"
        }
    
    def _get_response_templates(self) -> Dict[str, str]:
        """Templates de réponses sécurisées"""
        return {
            "no_information": "Je n'ai pas cette information dans ma base de données. Veuillez vérifier votre demande ou contacter l'administrateur.",
            "partial_information": "Voici les informations disponibles dans ma base de données : {verified_info}. Notez que certaines informations demandées ne sont pas disponibles.",
            "verification_needed": "Cette information nécessite une vérification supplémentaire. Je recommande de contacter l'équipe technique.",
            "context_limited": "Le contexte fourni est limité pour cette requête. Voici ce que je peux confirmer : {limited_info}"
        }
    
    def generate_secure_prompt(self, query: str, context: List[str], 
                              response_type: str = "general") -> str:
        """Génère un prompt sécurisé pour le LLM"""
        
        # Nettoyer et formater le contexte
        clean_context = self._clean_context(context)
        
        # Ajouter des instructions spécifiques selon le type de réponse
        specific_instructions = self._get_specific_instructions(response_type)
        
        # Construire le prompt complet
        full_prompt = f"""
{self.base_prompt}

{self.safety_instructions}

{specific_instructions}

CONTEXTE FOURNI:
{clean_context}

QUESTION UTILISATEUR:
{query}

INSTRUCTIONS SPÉCIFIQUES:
- Analyser le contexte fourni
- Identifier les informations vérifiables
- Répondre UNIQUEMENT avec des informations du contexte
- Marquer clairement les limitations

RÉPONSE SÉCURISÉE:
"""
        
        return full_prompt.strip()
    
    def _clean_context(self, context: List[str]) -> str:
        """Nettoie et formate le contexte"""
        if not context:
            return "Aucun contexte fourni"
        
        # Filtrer les éléments vides ou trop courts
        filtered_context = [item.strip() for item in context if item.strip() and len(item.strip()) > 10]
        
        if not filtered_context:
            return "Contexte insuffisant pour fournir une réponse fiable"
        
        # Formater le contexte
        formatted_context = "\n\n".join([
            f"Source {i+1}: {item}" 
            for i, item in enumerate(filtered_context[:5])  # Limiter à 5 sources
        ])
        
        return formatted_context
    
    def _get_specific_instructions(self, response_type: str) -> str:
        """Instructions spécifiques selon le type de réponse"""
        instructions = {
            "supplier_info": """
INSTRUCTIONS SPÉCIFIQUES - INFORMATIONS FOURNISSEUR:
- Vérifier que le nom du fournisseur est exactement dans le contexte
- Ne pas mentionner de fournisseurs non présents
- Si le fournisseur n'est pas trouvé, l'indiquer clairement
""",
            "inventory_code": """
INSTRUCTIONS SPÉCIFIQUES - CODES INVENTAIRE:
- Vérifier que le code est exactement dans le contexte
- Ne pas inventer de codes
- Si le code n'est pas trouvé, l'indiquer clairement
""",
            "delivery_status": """
INSTRUCTIONS SPÉCIFIQUES - STATUT LIVRAISON:
- Vérifier que la commande existe dans le contexte
- Ne pas inventer de statuts
- Si le statut n'est pas disponible, l'indiquer clairement
""",
            "general": """
INSTRUCTIONS SPÉCIFIQUES - RÉPONSE GÉNÉRALE:
- Analyser le contexte de manière critique
- Identifier les informations fiables
- Marquer les limitations et incertitudes
"""
        }
        
        return instructions.get(response_type, instructions["general"])
    
    def validate_response(self, response: str, context: List[str]) -> Dict[str, Any]:
        """Valide une réponse du LLM contre le contexte"""
        
        validation_result = {
            "is_valid": True,
            "hallucinations_detected": False,
            "unverified_entities": [],
            "confidence_score": 1.0,
            "warnings": [],
            "suggested_corrections": []
        }
        
        # Détecter les patterns suspects
        for pattern_name, pattern in self.verification_patterns.items():
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                # Vérifier si ces entités sont dans le contexte
                context_text = " ".join(context).lower()
                for match in matches:
                    if match.lower() not in context_text:
                        validation_result["unverified_entities"].append({
                            "type": pattern_name,
                            "value": match,
                            "context": "Non trouvé dans le contexte fourni"
                        })
                        validation_result["hallucinations_detected"] = True
        
        # Détecter les placeholders génériques
        generic_placeholders = re.findall(r"\[.*?\]|\(.*?\)|\{.*?\}", response)
        if generic_placeholders:
            validation_result["warnings"].append(f"Placeholders génériques détectés: {generic_placeholders}")
            validation_result["confidence_score"] *= 0.8
        
        # Calculer le score de confiance
        if validation_result["hallucinations_detected"]:
            validation_result["confidence_score"] *= 0.5
            validation_result["is_valid"] = False
        
        # Suggestions de correction
        if validation_result["unverified_entities"]:
            for entity in validation_result["unverified_entities"]:
                validation_result["suggested_corrections"].append(
                    f"Remplacer '{entity['value']}' par 'information non disponible'"
                )
        
        return validation_result
    
    def generate_safe_response(self, query: str, context: List[str], 
                             original_response: str = "") -> str:
        """Génère une réponse sécurisée basée sur le contexte"""
        
        if not context:
            return self.response_templates["no_information"]
        
        # Analyser le contexte pour extraire les informations vérifiables
        verified_info = self._extract_verified_information(context)
        
        if not verified_info:
            return self.response_templates["no_information"]
        
        # Construire une réponse sécurisée
        safe_response = f"""
Basé sur les informations disponibles dans ma base de données :

{verified_info}

Limitations :
- Je ne peux fournir que les informations présentes dans ma base
- Certaines données demandées peuvent ne pas être disponibles
- Pour des informations complémentaires, contactez l'équipe technique
"""
        
        return safe_response.strip()
    
    def _extract_verified_information(self, context: List[str]) -> str:
        """Extrait les informations vérifiables du contexte"""
        verified_info = []
        
        for item in context:
            item = item.strip()
            if len(item) > 20:  # Filtrer les éléments trop courts
                # Identifier le type d'information
                if "fournisseur" in item.lower() or "supplier" in item.lower():
                    verified_info.append(f"• Informations fournisseur : {item[:100]}...")
                elif "commande" in item.lower() or "order" in item.lower():
                    verified_info.append(f"• Informations commande : {item[:100]}...")
                elif "livraison" in item.lower() or "delivery" in item.lower():
                    verified_info.append(f"• Informations livraison : {item[:100]}...")
                elif "matériel" in item.lower() or "equipment" in item.lower():
                    verified_info.append(f"• Informations matériel : {item[:100]}...")
                else:
                    verified_info.append(f"• Information : {item[:100]}...")
        
        return "\n".join(verified_info) if verified_info else "Aucune information vérifiable trouvée"
    
    def get_prompt_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des prompts et instructions"""
        return {
            "base_prompt_length": len(self.base_prompt),
            "safety_instructions_length": len(self.safety_instructions),
            "verification_patterns_count": len(self.verification_patterns),
            "response_templates_count": len(self.response_templates),
            "timestamp": datetime.now().isoformat()
        }

def get_enhanced_prompt_manager() -> EnhancedLLMPrompt:
    """Retourne une instance du gestionnaire de prompts renforcé"""
    return EnhancedLLMPrompt()

if __name__ == "__main__":
    # Test du module
    prompt_manager = EnhancedLLMPrompt()
    
    # Test de génération de prompt
    test_context = [
        "Fournisseur: COHESIUM ICE, Adresse: Casablanca",
        "Commande BC23: Statut livrée, Date: 2025-08-20"
    ]
    
    test_query = "Quel est le statut de la commande BC23 ?"
    
    prompt = prompt_manager.generate_secure_prompt(test_query, test_context, "delivery_status")
    print("Prompt généré:")
    print(prompt)
    
    # Test de validation
    test_response = "La commande BC23 a été livrée le 2025-08-20 par le fournisseur COHESIUM ICE."
    validation = prompt_manager.validate_response(test_response, test_context)
    print("\nValidation de la réponse:")
    print(validation)
    
    # Test de réponse sécurisée
    safe_response = prompt_manager.generate_safe_response(test_query, test_context)
    print("\nRéponse sécurisée:")
    print(safe_response)
