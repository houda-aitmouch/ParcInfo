#!/usr/bin/env python3
"""
Système de correction automatique des fautes de frappe pour le chatbot
"""

import re
from typing import Dict, List, Tuple
from rapidfuzz import fuzz

class TypoCorrector:
    """Corrige automatiquement les fautes de frappe courantes"""
    
    def __init__(self):
        # Dictionnaire de corrections courantes
        self.common_typos = {
            # Fournisseurs
            'fournisuers': 'fournisseurs',
            'fourniseurs': 'fournisseurs',
            'fournissuers': 'fournisseurs',
            
            # Utilisateurs
            'utilistaeurs': 'utilisateurs',
            'utilisateus': 'utilisateurs',
            'utilisaturs': 'utilisateurs',
            
            # Matériels
            'materiels': 'matériels',
            'materiel': 'matériel',
            'materiaux': 'matériaux',
            
            # Bureautique
            'bureautique': 'bureautique',
            'bureautik': 'bureautique',
            
            # Informatique
            'informatik': 'informatique',
            'informatik': 'informatique',
            
            # Garantie
            'garanty': 'garantie',
            'garantie': 'garantie',
            'garanties': 'garanties',
            
            # Commandes
            'comandes': 'commandes',
            'comande': 'commande',
            
            # Livraisons
            'livraison': 'livraison',
            'livraisons': 'livraisons',
            
            # Général
            'liste': 'liste',
            'list': 'liste',
            'nombre': 'nombre',
            'total': 'total',
            'statut': 'statut',
            'statuts': 'statuts'
        }
        
        # Patterns de fautes de frappe courantes
        self.typo_patterns = [
            (r'\b(\w*)(u|n)(\w*)\b', r'\1\3'),  # Supprime les 'u' ou 'n' isolés
            (r'\b(\w*)(e|é)(\w*)\b', r'\1e\3'),  # Normalise les 'e' et 'é'
            (r'\b(\w*)(a|à)(\w*)\b', r'\1a\3'),  # Normalise les 'a' et 'à'
            (r'\b(\w*)(i|î)(\w*)\b', r'\1i\3'),  # Normalise les 'i' et 'î'
            (r'\b(\w*)(o|ô)(\w*)\b', r'\1o\3'),  # Normalise les 'o' et 'ô'
        ]
    
    def correct_typo(self, text: str) -> Tuple[str, bool]:
        """
        Corrige les fautes de frappe dans le texte
        Returns: (texte_corrigé, correction_effectuée)
        """
        original = text.lower()
        corrected = text
        
        # Vérifier les corrections courantes
        for typo, correction in self.common_typos.items():
            if typo in original:
                corrected = re.sub(rf'\b{typo}\b', correction, corrected, flags=re.IGNORECASE)
                return corrected, True
        
        # Appliquer les patterns de correction
        for pattern, replacement in self.typo_patterns:
            if re.search(pattern, original):
                corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
                return corrected, True
        
        return corrected, False
    
    def suggest_corrections(self, query: str) -> List[str]:
        """Suggère des corrections possibles pour une requête"""
        suggestions = []
        words = query.lower().split()
        
        for word in words:
            if len(word) > 3:  # Ignorer les mots trop courts
                for correct_word in self.common_typos.values():
                    similarity = fuzz.ratio(word, correct_word)
                    if similarity > 70:  # Seuil de similarité
                        suggestions.append(f"'{word}' → '{correct_word}'")
        
        return suggestions
    
    def enhance_query(self, query: str) -> Dict[str, str]:
        """
        Améliore une requête en corrigeant les fautes de frappe
        Returns: {
            'original': 'requête_originale',
            'corrected': 'requête_corrigée',
            'corrections': ['correction1', 'correction2'],
            'was_corrected': True/False
        }
        """
        original = query
        corrected, was_corrected = self.correct_typo(query)
        suggestions = self.suggest_corrections(query) if was_corrected else []
        
        return {
            'original': original,
            'corrected': corrected,
            'corrections': suggestions,
            'was_corrected': was_corrected
        }
