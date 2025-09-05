#!/usr/bin/env python3
"""
Module de filtrage anti-hallucinations pour le chatbot ParcInfo
Vérifie les réponses contre la base de données pour éliminer les informations fausses
"""

import os
import logging
import re
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from django.db import connection
from django.conf import settings
import numpy as np

logger = logging.getLogger(__name__)

class HallucinationFilter:
    """Filtre anti-hallucinations basé sur la vérification de la base de données"""
    
    def __init__(self):
        self.connection = connection
        self.verified_entities = {}
        self.patterns_to_filter = []
        self.load_verification_patterns()
        
    def load_verification_patterns(self):
        """Charge les patterns de vérification depuis la base de données"""
        try:
            # Patterns de détection d'hallucinations
            self.patterns_to_filter = [
                r'\[.*?\]',                    # Placeholders non remplis
                r'FOURNISSEUR_NON_VÉRIFIÉ',   # Fournisseurs non vérifiés
                r'CODE_INVALIDE',              # Codes invalides
                r'ICE_VÉRIFIÉ_REQUIS',        # ICE requis
                r'[A-Z]{2,}_[A-Z]{2,}',      # Patterns de codes génériques
                r'[A-Z]{3,}\s+[A-Z]{3,}',    # Noms de fournisseurs génériques
                r'\b[A-Z]{2,}\d{3,}\b',      # Codes de matériel génériques
                r'[A-Z]{2,}_[A-Z]{2,}_[A-Z]{2,}',  # Codes complexes génériques
            ]
            
            logger.info(f"Patterns de filtrage chargés: {len(self.patterns_to_filter)}")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des patterns: {e}")
    
    def verify_response_against_database(self, response_text: str, query_context: str = "") -> Dict[str, Any]:
        """Vérifie une réponse contre la base de données pour détecter les hallucinations"""
        try:
            start_time = time.time()
            
            # 1. Détection des patterns suspects
            suspicious_patterns = self._detect_suspicious_patterns(response_text)
            
            # 2. Extraction des entités à vérifier
            entities_to_verify = self._extract_entities_to_verify(response_text)
            
            # 3. Vérification contre la base de données
            verification_results = self._verify_entities_in_database(entities_to_verify)
            
            # 4. Analyse des incohérences
            inconsistencies = self._analyze_inconsistencies(response_text, verification_results)
            
            # 5. Score de confiance
            confidence_score = self._calculate_confidence_score(verification_results, inconsistencies)
            
            # 6. Réponse filtrée
            filtered_response = self._filter_hallucinations(response_text, verification_results)
            
            processing_time = time.time() - start_time
            
            result = {
                "original_response": response_text,
                "filtered_response": filtered_response,
                "suspicious_patterns": suspicious_patterns,
                "entities_verified": verification_results,
                "inconsistencies": inconsistencies,
                "confidence_score": confidence_score,
                "processing_time": processing_time,
                "hallucinations_detected": len(suspicious_patterns) > 0 or len(inconsistencies) > 0
            }
            
            logger.info(f"Vérification terminée en {processing_time:.3f}s - Score: {confidence_score:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification: {e}")
            return {
                "original_response": response_text,
                "filtered_response": response_text,
                "error": str(e),
                "confidence_score": 0.0,
                "hallucinations_detected": True
            }
    
    def check_hallucinations(self, response_text: str) -> float:
        """Vérifie les hallucinations et retourne un score de confiance (alias pour verify_response_against_database)"""
        try:
            result = self.verify_response_against_database(response_text)
            return result.get("confidence_score", 0.0)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des hallucinations: {e}")
            return 0.0
    
    def _detect_suspicious_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Détecte les patterns suspects dans le texte"""
        suspicious_items = []
        
        for pattern in self.patterns_to_filter:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                suspicious_items.append({
                    "pattern": pattern,
                    "matched_text": match.group(),
                    "start_pos": match.start(),
                    "end_pos": match.end(),
                    "severity": "high" if "NON_VÉRIFIÉ" in match.group() else "medium"
                })
        
        return suspicious_items
    
    def _extract_entities_to_verify(self, text: str) -> Dict[str, List[str]]:
        """Extrait les entités à vérifier dans la base de données"""
        entities = {
            "suppliers": [],
            "materials": [],
            "orders": [],
            "users": [],
            "codes": []
        }
        
        # Extraire les fournisseurs
        supplier_patterns = [
            r'\b[A-Z]{2,}\s+[A-Z]{2,}\b',  # Noms de fournisseurs
            r'\b[A-Z]{2,}_[A-Z]{2,}\b',     # Codes de fournisseurs
            r'\b[A-Z]{3,}\b'                 # Abréviations
        ]
        
        for pattern in supplier_patterns:
            matches = re.findall(pattern, text)
            entities["suppliers"].extend(matches)
        
        # Extraire les codes de matériel
        material_patterns = [
            r'\b[A-Z]{2,}\d{2,}\b',         # Codes comme cd12, cd13
            r'\b[A-Z]{2,}_[A-Z]{2,}\b',     # Codes avec underscore
            r'\b\d{2,}[A-Z]{2,}\b'          # Codes numériques + lettres
        ]
        
        for pattern in material_patterns:
            matches = re.findall(pattern, text)
            entities["codes"].extend(matches)
        
        # Extraire les numéros de commande
        order_patterns = [
            r'\bBC\d{2,}\b',                 # Commandes BC23, BC24
            r'\b[A-Z]{2,}\d{4}\b',          # Commandes AOO2025
        ]
        
        for pattern in order_patterns:
            matches = re.findall(pattern, text)
            entities["orders"].extend(matches)
        
        # Extraire les noms d'utilisateur
        user_patterns = [
            r'\bgestionnaire_[a-z]+\b',      # gestionnaire_bureau, gestionnaire_info
            r'\btest_[a-z]+\b',              # test_employe
            r'\bsuperadmin\b'                # superadmin
        ]
        
        for pattern in user_patterns:
            matches = re.findall(pattern, text)
            entities["users"].extend(matches)
        
        # Nettoyer et dédupliquer
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _verify_entities_in_database(self, entities: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        """Vérifie les entités extraites dans la base de données"""
        verification_results = {}
        
        try:
            with self.connection.cursor() as cursor:
                # Vérifier les fournisseurs
                if entities["suppliers"]:
                    verification_results["suppliers"] = self._verify_suppliers(cursor, entities["suppliers"])
                
                # Vérifier les codes de matériel
                if entities["codes"]:
                    verification_results["materials"] = self._verify_materials(cursor, entities["codes"])
                
                # Vérifier les commandes
                if entities["orders"]:
                    verification_results["orders"] = self._verify_orders(cursor, entities["orders"])
                
                # Vérifier les utilisateurs
                if entities["users"]:
                    verification_results["users"] = self._verify_users(cursor, entities["users"])
                
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des entités: {e}")
            verification_results["error"] = str(e)
        
        return verification_results
    
    def _verify_suppliers(self, cursor, supplier_names: List[str]) -> Dict[str, Any]:
        """Vérifie les fournisseurs dans la base de données"""
        results = {}
        
        for supplier in supplier_names:
            try:
                # Rechercher par nom
                cursor.execute("""
                    SELECT id, nom, ice, ville 
                    FROM fournisseurs 
                    WHERE nom ILIKE %s OR nom ILIKE %s
                """, (f"%{supplier}%", supplier))
                
                matches = cursor.fetchall()
                
                if matches:
                    results[supplier] = {
                        "verified": True,
                        "matches": [{"id": m[0], "nom": m[1], "ice": m[2], "ville": m[3]} for m in matches],
                        "source": "database"
                    }
                else:
                    results[supplier] = {
                        "verified": False,
                        "matches": [],
                        "source": "not_found"
                    }
                    
            except Exception as e:
                results[supplier] = {
                    "verified": False,
                    "error": str(e),
                    "source": "error"
                }
        
        return results
    
    def _verify_materials(self, cursor, material_codes: List[str]) -> Dict[str, Any]:
        """Vérifie les codes de matériel dans la base de données"""
        results = {}
        
        for code in material_codes:
            try:
                # Rechercher dans materiel_informatique
                cursor.execute("""
                    SELECT id, code_inventaire, designation, marque, modele
                    FROM materiel_informatique 
                    WHERE code_inventaire = %s
                """, (code,))
                
                matches_it = cursor.fetchall()
                
                # Rechercher dans materiel_bureautique
                cursor.execute("""
                    SELECT id, code_inventaire, designation, marque, modele
                    FROM materiel_bureautique 
                    WHERE code_inventaire = %s
                """, (code,))
                
                matches_bureau = cursor.fetchall()
                
                all_matches = matches_it + matches_bureau
                
                if all_matches:
                    results[code] = {
                        "verified": True,
                        "matches": [{"id": m[0], "code": m[1], "designation": m[2], "marque": m[3], "modele": m[4]} for m in all_matches],
                        "source": "database"
                    }
                else:
                    results[code] = {
                        "verified": False,
                        "matches": [],
                        "source": "not_found"
                    }
                    
            except Exception as e:
                results[code] = {
                    "verified": False,
                    "error": str(e),
                    "source": "error"
                }
        
        return results
    
    def _verify_orders(self, cursor, order_numbers: List[str]) -> Dict[str, Any]:
        """Vérifie les numéros de commande dans la base de données"""
        results = {}
        
        for order in order_numbers:
            try:
                # Rechercher dans commande_informatique
                cursor.execute("""
                    SELECT id, numero_commande, date_commande, montant, fournisseur_id
                    FROM commande_informatique 
                    WHERE numero_commande = %s
                """, (order,))
                
                matches_it = cursor.fetchall()
                
                # Rechercher dans commande_bureau
                cursor.execute("""
                    SELECT id, numero_commande, date_commande, montant, fournisseur_id
                    FROM commande_bureau 
                    WHERE numero_commande = %s
                """, (order,))
                
                matches_bureau = cursor.fetchall()
                
                all_matches = matches_it + matches_bureau
                
                if all_matches:
                    results[order] = {
                        "verified": True,
                        "matches": [{"id": m[0], "numero": m[1], "date": m[2], "montant": m[3], "fournisseur_id": m[4]} for m in all_matches],
                        "source": "database"
                    }
                else:
                    results[order] = {
                        "verified": False,
                        "matches": [],
                        "source": "not_found"
                    }
                    
            except Exception as e:
                results[order] = {
                    "verified": False,
                    "error": str(e),
                    "source": "error"
                }
        
        return results
    
    def _verify_users(self, cursor, usernames: List[str]) -> Dict[str, Any]:
        """Vérifie les noms d'utilisateur dans la base de données"""
        results = {}
        
        for username in usernames:
            try:
                cursor.execute("""
                    SELECT id, username, email, role, is_active
                    FROM users_customuser 
                    WHERE username = %s
                """, (username,))
                
                matches = cursor.fetchall()
                
                if matches:
                    results[username] = {
                        "verified": True,
                        "matches": [{"id": m[0], "username": m[1], "email": m[2], "role": m[3], "active": m[4]} for m in matches],
                        "source": "database"
                    }
                else:
                    results[username] = {
                        "verified": False,
                        "matches": [],
                        "source": "not_found"
                    }
                    
            except Exception as e:
                results[username] = {
                    "verified": False,
                    "error": str(e),
                    "source": "error"
                }
        
        return results
    
    def _analyze_inconsistencies(self, response_text: str, verification_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyse les incohérences dans la réponse"""
        inconsistencies = []
        
        # Vérifier les incohérences de dates
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # Dates ISO
            r'(\d{2}/\d{2}/\d{4})',  # Dates françaises
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, response_text)
            if len(dates) > 1:
                # Vérifier la cohérence des dates
                for i, date1 in enumerate(dates):
                    for j, date2 in enumerate(dates[i+1:], i+1):
                        try:
                            from datetime import datetime
                            dt1 = datetime.strptime(date1, "%Y-%m-%d")
                            dt2 = datetime.strptime(date2, "%Y-%m-%d")
                            
                            if dt1 > dt2:
                                inconsistencies.append({
                                    "type": "date_inconsistency",
                                    "description": f"Date {date1} est après {date2}",
                                    "severity": "medium",
                                    "positions": [i, j]
                                })
                        except:
                            pass
        
        # Vérifier les incohérences de montants
        amount_patterns = [
            r'(\d+(?:\.\d{2})?)\s*(?:DH|€|\$)',  # Montants avec devise
            r'(\d+(?:\.\d{2})?)\s*(?:mille|k)',  # Montants en milliers
        ]
        
        for pattern in amount_patterns:
            amounts = re.findall(pattern, response_text)
            if len(amounts) > 1:
                # Vérifier la cohérence des montants
                amounts_numeric = []
                for amount in amounts:
                    try:
                        if 'k' in amount or 'mille' in amount:
                            amounts_numeric.append(float(amount.replace('k', '').replace('mille', '')) * 1000)
                        else:
                            amounts_numeric.append(float(amount))
                    except:
                        pass
                
                if len(amounts_numeric) > 1:
                    total_calculated = sum(amounts_numeric)
                    if "total" in response_text.lower() or "somme" in response_text.lower():
                        # Vérifier si le total mentionné correspond
                        total_pattern = r'total[:\s]*(\d+(?:\.\d{2})?)'
                        total_match = re.search(total_pattern, response_text, re.IGNORECASE)
                        if total_match:
                            total_mentioned = float(total_match.group(1))
                            if abs(total_calculated - total_mentioned) > 0.01:
                                inconsistencies.append({
                                    "type": "amount_inconsistency",
                                    "description": f"Total calculé ({total_calculated}) ≠ total mentionné ({total_mentioned})",
                                    "severity": "high",
                                    "calculated": total_calculated,
                                    "mentioned": total_mentioned
                                })
        
        # Vérifier les incohérences d'entités
        for entity_type, entity_results in verification_results.items():
            if entity_type == "error":
                continue
                
            for entity_name, entity_result in entity_results.items():
                if not entity_result.get("verified", False):
                    inconsistencies.append({
                        "type": "unverified_entity",
                        "description": f"Entité '{entity_name}' non vérifiée dans la base",
                        "severity": "high",
                        "entity_type": entity_type,
                        "entity_name": entity_name
                    })
        
        return inconsistencies
    
    def _calculate_confidence_score(self, verification_results: Dict[str, Any], inconsistencies: List[Dict[str, Any]]) -> float:
        """Calcule un score de confiance basé sur la vérification"""
        try:
            base_score = 1.0
            
            # Réduire le score pour chaque entité non vérifiée
            for entity_type, entity_results in verification_results.items():
                if entity_type == "error":
                    base_score -= 0.3
                    continue
                    
                for entity_name, entity_result in entity_results.items():
                    if not entity_result.get("verified", False):
                        base_score -= 0.1
            
            # Réduire le score pour chaque incohérence
            for inconsistency in inconsistencies:
                if inconsistency["severity"] == "high":
                    base_score -= 0.2
                elif inconsistency["severity"] == "medium":
                    base_score -= 0.1
                else:
                    base_score -= 0.05
            
            # Score minimum de 0.0
            confidence_score = max(0.0, base_score)
            
            return round(confidence_score, 2)
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul du score de confiance: {e}")
            return 0.0
    
    def _filter_hallucinations(self, response_text: str, verification_results: Dict[str, Any]) -> str:
        """Filtre les hallucinations de la réponse"""
        filtered_text = response_text
        
        try:
            # Remplacer les entités non vérifiées
            for entity_type, entity_results in verification_results.items():
                if entity_type == "error":
                    continue
                    
                for entity_name, entity_result in entity_results.items():
                    if not entity_result.get("verified", False):
                        # Remplacer par une indication de non-vérification
                        replacement = f"[{entity_name} - Non vérifié]"
                        filtered_text = filtered_text.replace(entity_name, replacement)
            
            # Supprimer les patterns suspects
            for pattern in self.patterns_to_filter:
                filtered_text = re.sub(pattern, "[Information non vérifiée]", filtered_text)
            
            # Nettoyer les espaces multiples
            filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()
            
            return filtered_text
            
        except Exception as e:
            logger.error(f"Erreur lors du filtrage: {e}")
            return response_text
    
    def get_filtering_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de filtrage"""
        return {
            "patterns_loaded": len(self.patterns_to_filter),
            "verification_cache_size": len(self.verified_entities),
            "last_verification": time.time()
        }

def main():
    """Fonction principale pour tester le filtre anti-hallucinations"""
    logging.basicConfig(level=logging.INFO)
    
    # Créer le filtre
    filter_instance = HallucinationFilter()
    
    # Test avec une réponse contenant des hallucinations
    test_response = """
    Le fournisseur COHESIUM ICE a livré le matériel cd99 le 2025-08-15.
    La commande BC25 a été passée pour un montant de 5000 DH.
    L'utilisateur test_user a demandé l'équipement.
    Le total des commandes est de 15000 DH.
    """
    
    print("🧪 Test du filtre anti-hallucinations")
    print("=" * 50)
    print(f"Réponse originale:\n{test_response}")
    
    # Vérifier la réponse
    result = filter_instance.verify_response_against_database(test_response)
    
    print(f"\n📊 Résultats de la vérification:")
    print(f"Score de confiance: {result['confidence_score']}")
    print(f"Hallucinations détectées: {result['hallucinations_detected']}")
    print(f"Patterns suspects: {len(result['suspicious_patterns'])}")
    print(f"Incohérences: {len(result['inconsistencies'])}")
    
    print(f"\n🔍 Réponse filtrée:\n{result['filtered_response']}")
    
    # Afficher les détails
    if result['suspicious_patterns']:
        print(f"\n⚠️ Patterns suspects détectés:")
        for pattern in result['suspicious_patterns']:
            print(f"  - {pattern['matched_text']} (sévérité: {pattern['severity']})")
    
    if result['inconsistencies']:
        print(f"\n❌ Incohérences détectées:")
        for inconsistency in result['inconsistencies']:
            print(f"  - {inconsistency['description']} (sévérité: {inconsistency['severity']})")

if __name__ == "__main__":
    main()
