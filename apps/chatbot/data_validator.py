"""
Système de validation des données pour éviter les hallucinations
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from django.db.models import Q, Count, Exists, OuterRef
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class DataValidator:
    """Classe pour valider les données avant de les retourner au chatbot"""
    
    def __init__(self):
        self.validation_cache = {}
    
    def validate_material_exists(self, code_inventaire: str) -> bool:
        """Vérifie si un matériel existe réellement"""
        try:
            from apps.materiel_informatique.models import MaterielInformatique
            from apps.materiel_bureautique.models import MaterielBureau
            
            # Vérifier dans les deux tables
            exists_it = MaterielInformatique.objects.filter(
                code_inventaire__iexact=code_inventaire
            ).exists()
            
            exists_bureau = MaterielBureau.objects.filter(
                code_inventaire__iexact=code_inventaire
            ).exists()
            
            return exists_it or exists_bureau
            
        except Exception as e:
            logger.error(f"Erreur lors de la validation du matériel {code_inventaire}: {e}")
            return False
    
    def validate_user_exists(self, username: str) -> bool:
        """Vérifie si un utilisateur existe réellement"""
        try:
            from apps.users.models import CustomUser
            return CustomUser.objects.filter(username__iexact=username).exists()
        except Exception as e:
            logger.error(f"Erreur lors de la validation de l'utilisateur {username}: {e}")
            return False
    
    def validate_supplier_exists(self, nom_fournisseur: str) -> bool:
        """Vérifie si un fournisseur existe réellement"""
        try:
            from apps.fournisseurs.models import Fournisseur
            return Fournisseur.objects.filter(nom__iexact=nom_fournisseur).exists()
        except Exception as e:
            logger.error(f"Erreur lors de la validation du fournisseur {nom_fournisseur}: {e}")
            return False
    
    def validate_order_exists(self, code_commande: str) -> bool:
        """Vérifie si une commande existe réellement"""
        try:
            from apps.commande_informatique.models import Commande
            from apps.commande_bureau.models import CommandeBureau
            
            exists_it = Commande.objects.filter(
                code_commande__iexact=code_commande
            ).exists()
            
            exists_bureau = CommandeBureau.objects.filter(
                code_commande__iexact=code_commande
            ).exists()
            
            return exists_it or exists_bureau
            
        except Exception as e:
            logger.error(f"Erreur lors de la validation de la commande {code_commande}: {e}")
            return False
    
    def validate_delivery_exists(self, code_livraison: str) -> bool:
        """Vérifie si une livraison existe réellement"""
        try:
            from apps.livraison.models import Livraison
            return Livraison.objects.filter(code_livraison__iexact=code_livraison).exists()
        except Exception as e:
            logger.error(f"Erreur lors de la validation de la livraison {code_livraison}: {e}")
            return False
    
    def filter_valid_materials(self, materials_list: List[Dict]) -> List[Dict]:
        """Filtre une liste de matériels pour ne garder que ceux qui existent"""
        valid_materials = []
        
        for material in materials_list:
            code = material.get('code_inventaire', '')
            if code and self.validate_material_exists(code):
                valid_materials.append(material)
            else:
                logger.warning(f"Matériel invalide filtré: {code}")
        
        return valid_materials
    
    def filter_valid_users(self, users_list: List[Dict]) -> List[Dict]:
        """Filtre une liste d'utilisateurs pour ne garder que ceux qui existent"""
        valid_users = []
        
        for user in users_list:
            username = user.get('username', '')
            if username and self.validate_user_exists(username):
                valid_users.append(user)
            else:
                logger.warning(f"Utilisateur invalide filtré: {username}")
        
        return valid_users
    
    def validate_response_coherence(self, response_data: Dict) -> Tuple[bool, str]:
        """Valide la cohérence d'une réponse complète"""
        try:
            # Vérifier les références croisées
            if 'materials' in response_data:
                for material in response_data['materials']:
                    if 'code_inventaire' in material:
                        if not self.validate_material_exists(material['code_inventaire']):
                            return False, f"Matériel inexistant: {material['code_inventaire']}"
            
            if 'users' in response_data:
                for user in response_data['users']:
                    if 'username' in user:
                        if not self.validate_user_exists(user['username']):
                            return False, f"Utilisateur inexistant: {user['username']}"
            
            if 'orders' in response_data:
                for order in response_data['orders']:
                    if 'code_commande' in order:
                        if not self.validate_order_exists(order['code_commande']):
                            return False, f"Commande inexistante: {order['code_commande']}"
            
            return True, "Réponse cohérente"
            
        except Exception as e:
            logger.error(f"Erreur lors de la validation de cohérence: {e}")
            return False, f"Erreur de validation: {str(e)}"
    
    def get_real_data_counts(self) -> Dict[str, int]:
        """Récupère les vrais comptages de la base de données"""
        try:
            from apps.materiel_informatique.models import MaterielInformatique
            from apps.materiel_bureautique.models import MaterielBureau
            from apps.users.models import CustomUser
            from apps.fournisseurs.models import Fournisseur
            from apps.commande_informatique.models import Commande
            from apps.commande_bureau.models import CommandeBureau
            from apps.livraison.models import Livraison
            
            counts = {
                'materiels_informatique': MaterielInformatique.objects.count(),
                'materiels_bureautique': MaterielBureau.objects.count(),
                'utilisateurs': CustomUser.objects.count(),
                'fournisseurs': Fournisseur.objects.count(),
                'commandes_informatique': Commande.objects.count(),
                'commandes_bureautique': CommandeBureau.objects.count(),
                'livraisons': Livraison.objects.count(),
            }
            
            return counts
            
        except Exception as e:
            logger.error(f"Erreur lors du comptage des données: {e}")
            return {}
    
    def validate_statistics(self, claimed_stats: Dict[str, int]) -> Dict[str, bool]:
        """Valide les statistiques revendiquées contre les vraies données"""
        real_counts = self.get_real_data_counts()
        validation_results = {}
        
        for stat_name, claimed_count in claimed_stats.items():
            if stat_name in real_counts:
                real_count = real_counts[stat_name]
                validation_results[stat_name] = claimed_count == real_count
                
                if not validation_results[stat_name]:
                    logger.warning(f"Statistique incorrecte pour {stat_name}: "
                                 f"revendiqué {claimed_count}, réel {real_count}")
            else:
                validation_results[stat_name] = False
                logger.warning(f"Statistique inconnue: {stat_name}")
        
        return validation_results
    
    def sanitize_response(self, response_text: str) -> str:
        """Nettoie une réponse pour éviter les hallucinations évidentes"""
        # Détecter et remplacer les patterns d'hallucination courants
        hallucination_patterns = [
            r'\[FOURNISSEUR_NON_VÉRIFIÉ\]',
            r'\[CODE_INVENTAIRE_INCONNU\]',
            r'\[UTILISATEUR_INCONNU\]',
            r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}',  # Dates inventées
        ]
        
        import re
        for pattern in hallucination_patterns:
            if re.search(pattern, response_text):
                logger.warning(f"Pattern d'hallucination détecté: {pattern}")
                response_text = re.sub(pattern, '[DONNÉE NON DISPONIBLE]', response_text)
        
        # Vérifier les réponses vides ou trop courtes
        if len(response_text.strip()) <= 1:
            return "Aucune donnée trouvée pour cette requête."
        
        return response_text
    
    def create_safe_response(self, data: Dict, response_type: str) -> str:
        """Crée une réponse sécurisée basée sur des données validées"""
        try:
            if not data or not data.get('items'):
                return "Aucune donnée trouvée pour cette requête."
            
            items = data['items']
            if not items:
                return "Aucune donnée trouvée pour cette requête."
            
            # Valider chaque élément
            valid_items = []
            for item in items:
                if self.validate_item(item, response_type):
                    valid_items.append(item)
            
            if not valid_items:
                return "Aucune donnée valide trouvée pour cette requête."
            
            # Créer la réponse
            response_lines = [f"**{response_type} :**\n"]
            
            for item in valid_items:
                response_lines.append(f"• {self.format_item(item, response_type)}")
            
            # Ajouter les statistiques si disponibles
            if 'statistics' in data:
                stats = data['statistics']
                response_lines.append(f"\n**Statistiques :**")
                for stat_name, stat_value in stats.items():
                    response_lines.append(f"• {stat_name}: {stat_value}")
            
            return "\n".join(response_lines)
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la réponse sécurisée: {e}")
            return "Erreur lors de la récupération des données."
    
    def validate_item(self, item: Dict, item_type: str) -> bool:
        """Valide un élément selon son type"""
        try:
            if item_type == 'materials':
                return self.validate_material_exists(item.get('code_inventaire', ''))
            elif item_type == 'users':
                return self.validate_user_exists(item.get('username', ''))
            elif item_type == 'suppliers':
                return self.validate_supplier_exists(item.get('nom', ''))
            elif item_type == 'orders':
                return self.validate_order_exists(item.get('code_commande', ''))
            elif item_type == 'deliveries':
                return self.validate_delivery_exists(item.get('code_livraison', ''))
            else:
                return True  # Type inconnu, on fait confiance
        except Exception as e:
            logger.error(f"Erreur lors de la validation d'élément {item_type}: {e}")
            return False
    
    def format_item(self, item: Dict, item_type: str) -> str:
        """Formate un élément pour l'affichage"""
        try:
            if item_type == 'materials':
                return f"{item.get('code_inventaire', 'N/A')} — {item.get('statut', 'N/A')} — {item.get('utilisateur', 'N/A')}"
            elif item_type == 'users':
                return f"{item.get('username', 'N/A')} — {item.get('email', 'N/A')} — {item.get('role', 'N/A')}"
            elif item_type == 'suppliers':
                return f"{item.get('nom', 'N/A')} — {item.get('ice', 'N/A')}"
            elif item_type == 'orders':
                return f"{item.get('code_commande', 'N/A')} — {item.get('fournisseur', 'N/A')} — {item.get('date', 'N/A')}"
            elif item_type == 'deliveries':
                return f"{item.get('code_livraison', 'N/A')} — {item.get('statut', 'N/A')} — {item.get('date', 'N/A')}"
            else:
                return str(item)
        except Exception as e:
            logger.error(f"Erreur lors du formatage d'élément {item_type}: {e}")
            return "Erreur de formatage"
