"""Module de recherche structurée SQL pour requêtes exactes"""

import re
import unicodedata
from typing import Dict, Optional, List
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class StructuredSearch:
    """Recherches SQL exactes prioritaires avant RAG/LLM"""
    
    def _normalize_text(self, text: str) -> str:
        """Normalise le texte"""
        if not text:
            return ""
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        return ' '.join(text.strip().lower().split())
    
    def _clean_ice(self, ice: str) -> str:
        """Nettoie ICE - garde seulement chiffres"""
        return ''.join(c for c in (ice or '') if c.isdigit())
    
    def route_query(self, query: str) -> Optional[Dict]:
        """Enhanced routing to appropriate exact search"""
        if not query or not query.strip():
            return None
            
        try:
            query_lower = query.lower()
            query_clean = self._normalize_text(query)
            
            # Enhanced ICE patterns (15 chiffres)
            ice_patterns = [
                r'ice[\s:]*([0-9]{15})',
                r'identifiant[\s\w]*entreprise[\s:]*([0-9]{15})',
                r'\b([0-9]{15})\b',
                r'ice\s*[:\s]*([0-9]{3}\s*[0-9]{3}\s*[0-9]{3}\s*[0-9]{3}\s*[0-9]{3})'
            ]
            
            for pattern in ice_patterns:
                match = re.search(pattern, query_clean)
                if match:
                    ice_clean = re.sub(r'\s+', '', match.group(1))
                    if len(ice_clean) == 15:
                        result = self.get_fournisseur_by_ice(ice_clean)
                        if result:
                            return {'type': 'fournisseur', 'data': result, 'method': 'ice_exact', 'found': True}
            
            # Enhanced command number patterns
            cmd_patterns = [
                r'commande[\s\w]*[:\s]*([A-Z0-9/\-]+)',
                r'numero[\s\w]*commande[\s:]*([A-Z0-9/\-]+)',
                r'\b([A-Z]+/[A-Z]+/[0-9/\-]+)\b',
                r'\b(?:BC|BL|FA|CMD)[-_\/]?(\d+(?:[-_\/]\d+)*)\b',
                r'bon[\s\w]*commande[\s:]*([A-Z0-9/\-]+)',
                r'facture[\s:]*([A-Z0-9/\-]+)'
            ]
            
            for pattern in cmd_patterns:
                match = re.search(pattern, query_clean, re.IGNORECASE)
                if match:
                    result = self.get_commande_by_numero(match.group(1))
                    if result:
                        return {'type': 'commande', 'data': result, 'method': 'numero_exact', 'found': True}
            
            # Enhanced material code patterns
            code_patterns = [
                r'\b(cd\d+)\b',
                r'\b(add/info/\d+)\b',
                r'code[\s:]*([a-z0-9/\-]+)',
                r'serie[\s:]*([a-z0-9\-]+)',
                r'materiel[\s\w]*([a-z0-9]+)',
                r'\b(?:INFO|PC|BUREAU|BAIE|SRV|EQ|ARM|SW)[A-Z0-9/\-]*(\d+[A-Z0-9/\-]*)\b',
                r'\b([A-Z]{2,6}/[A-Z0-9/\-]+/\d+[A-Z0-9/\-]*)\b',
                r'num[eé]ro[\s\w]*s[eé]rie[\s:]*([A-Z0-9\-]+)',
                r'n[°o][\s\w]*s[eé]rie[\s:]*([A-Z0-9\-]+)'
            ]
            
            for pattern in code_patterns:
                match = re.search(pattern, query_clean, re.IGNORECASE)
                if match:
                    result = self.get_materiel_by_code(match.group(1))
                    if result:
                        return {'type': 'materiel', 'data': result, 'method': 'code_exact', 'found': True}
            
            # Enhanced supplier name patterns
            supplier_patterns = [
                r'fournisseur[\s:]*([A-Za-z0-9\s\-&]+)',
                r'soci[eé]t[eé][\s:]*([A-Za-z0-9\s\-&]+)',
                r'entreprise[\s:]*([A-Za-z0-9\s\-&]+)',
                r'vendeur[\s:]*([A-Za-z0-9\s\-&]+)'
            ]
            
            for pattern in supplier_patterns:
                match = re.search(pattern, query_clean, re.IGNORECASE)
                if match:
                    supplier_name = match.group(1).strip()
                    if len(supplier_name) > 2:  # Minimum length check
                        result = self.get_fournisseur_by_name(supplier_name)
                        if result:
                            return {'type': 'fournisseur', 'data': result, 'method': 'name_exact', 'found': True}
            
            return None
            
        except Exception as e:
            logger.error(f"Error in route_query: {e}")
            return None
    
    def get_fournisseur_by_ice(self, ice: str) -> Optional[Dict]:
        """Recherche fournisseur par ICE"""
        if not ice:
            return None
            
        ice_clean = self._clean_ice(ice)
        if len(ice_clean) != 15:
            return None
            
        try:
            with connection.cursor() as c:
                c.execute("""
                    SELECT id, nom, ice, adresse, if_fiscal
                    FROM fournisseurs_fournisseur 
                    WHERE REPLACE(ice, ' ', '') = %s
                """, [ice_clean])
                row = c.fetchone()
                if row:
                    return {'id': row[0], 'nom': row[1], 'ice': row[2], 
                           'adresse': row[3], 'if_fiscal': row[4]}
        except Exception as e:
            logger.error(f"Database error in get_fournisseur_by_ice: {e}")
        return None
    
    def get_commande_by_numero(self, numero: str) -> Optional[Dict]:
        """Recherche commande par numéro"""
        if not numero:
            return None
            
        num_clean = numero.upper().strip()
        
        try:
            with connection.cursor() as c:
                c.execute("""
                    SELECT c.id, c.numero_commande, c.date_commande, 
                           c.mode_passation, f.nom, 'informatique' as type
                    FROM commande_informatique_commande c
                    LEFT JOIN fournisseurs_fournisseur f ON c.fournisseur_id = f.id
                    WHERE UPPER(c.numero_commande) = %s
                    
                    UNION ALL
                    
                    SELECT c.id, c.numero_commande, c.date_commande,
                           c.mode_passation, f.nom, 'bureau' as type
                    FROM commande_bureau_commandebureau c
                    LEFT JOIN fournisseurs_fournisseur f ON c.fournisseur_id = f.id
                    WHERE UPPER(c.numero_commande) = %s
                """, [num_clean, num_clean])
                row = c.fetchone()
                if row:
                    return {'id': row[0], 'numero': row[1], 'date': row[2],
                           'mode_passation': row[3], 'fournisseur': row[4], 'type': row[5]}
        except Exception as e:
            logger.error(f"Database error in get_commande_by_numero: {e}")
        return None
    
    def get_materiel_by_code(self, code: str) -> Optional[Dict]:
        """Recherche matériel par code/série"""
        if not code:
            return None
            
        code_clean = code.upper().strip()
        
        try:
            with connection.cursor() as c:
                c.execute("""
                    SELECT id, code_inventaire, numero_serie, observation, 
                           statut, lieu_stockage, 'informatique' as category
                    FROM materiel_informatique_materielinformatique
                    WHERE UPPER(code_inventaire) = %s OR UPPER(numero_serie) = %s
                    
                    UNION ALL
                    
                    SELECT id, code_inventaire, NULL as numero_serie, observation,
                           statut, lieu_stockage, 'bureau' as category
                    FROM materiel_bureautique_materielbureau  
                    WHERE UPPER(code_inventaire) = %s
                """, [code_clean, code_clean, code_clean])
                row = c.fetchone()
                if row:
                    return {'id': row[0], 'code': row[1], 'serie': row[2],
                           'observation': row[3], 'statut': row[4], 'lieu': row[5], 'category': row[6]}
        except Exception as e:
            logger.error(f"Database error in get_materiel_by_code: {e}")
        return None
    
    def get_fournisseur_by_name(self, name: str) -> Optional[Dict]:
        """Recherche fournisseur par nom"""
        if not name:
            return None
            
        try:
            with connection.cursor() as c:
                c.execute("""
                    SELECT id, nom, ice, adresse, if_fiscal
                    FROM fournisseurs_fournisseur 
                    WHERE LOWER(nom) = LOWER(%s)
                """, [name.strip()])
                row = c.fetchone()
                if row:
                    return {'id': row[0], 'nom': row[1], 'ice': row[2], 
                           'adresse': row[3], 'if_fiscal': row[4]}
        except Exception as e:
            logger.error(f"Database error in get_fournisseur_by_name: {e}")
        return None
    
    def format_response(self, result: Dict) -> str:
        """Formate la réponse pour affichage"""
        if not result or 'data' not in result:
            return "Aucune information trouvée."
        
        try:
            data = result['data']
            rtype = result.get('type', '')
            
            if rtype == 'fournisseur':
                return f"""**Fournisseur trouvé :**
• **Nom :** {data.get('nom', 'N/A')}
• **ICE :** {data.get('ice', 'N/A')}
• **Adresse :** {data.get('adresse', 'N/A')}
• **IF Fiscal :** {data.get('if_fiscal', 'N/A')}

"""
                
            elif rtype == 'commande':
                return f"""**Commande trouvée :**
• **Numéro :** {data.get('numero', 'N/A')}
• **Date :** {data.get('date', 'N/A')}
• **Mode passation :** {data.get('mode_passation', 'N/A')}
• **Fournisseur :** {data.get('fournisseur', 'N/A')}
• **Type :** {data.get('type', 'N/A')}

"""
                
            elif rtype == 'materiel':
                return f"""**Matériel trouvé :**
• **Code :** {data.get('code', 'N/A')}
• **Série :** {data.get('serie', 'N/A')}
• **Observation :** {data.get('observation', 'N/A')}
• **Statut :** {data.get('statut', 'N/A')}
• **Lieu :** {data.get('lieu', 'N/A')}
• **Catégorie :** {data.get('category', 'N/A')}

"""
            
            return str(data)
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "Erreur lors du formatage de la réponse."
