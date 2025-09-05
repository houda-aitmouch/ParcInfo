#!/usr/bin/env python3
"""
Module de cache Redis pour le chatbot ParcInfo
Optimise les performances avec un cache distribué et intelligent
"""

import os
import json
import logging
import time
import hashlib
from typing import Dict, List, Any, Optional, Union
from functools import wraps
import redis
from django.conf import settings

logger = logging.getLogger(__name__)

class RedisCacheManager:
    """Gestionnaire de cache Redis pour le chatbot ParcInfo"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis_client = None
        self.host = host
        self.port = port
        self.db = db
        self.connection_pool = None
        self.default_ttl = 1800  # 30 minutes par défaut
        
        # Configuration des TTL par type de données
        self.ttl_config = {
            "response": 1800,        # 30 minutes pour les réponses
            "embedding": 3600,       # 1 heure pour les embeddings
            "intent": 7200,          # 2 heures pour les intents
            "pattern": 14400,        # 4 heures pour les patterns
            "user_session": 900,     # 15 minutes pour les sessions utilisateur
            "query_result": 3600,    # 1 heure pour les résultats de requêtes
            "database_query": 1800,  # 30 minutes pour les requêtes DB
        }
        
        # Statistiques du cache
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "errors": 0
        }
        
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialise la connexion Redis"""
        try:
            # Créer le pool de connexions
            self.connection_pool = redis.ConnectionPool(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
                max_connections=20,
                retry_on_timeout=True,
                socket_keepalive=True
            )
            
            # Créer le client Redis
            self.redis_client = redis.Redis(
                connection_pool=self.connection_pool,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            # Tester la connexion
            self.redis_client.ping()
            logger.info(f"✅ Connexion Redis établie sur {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"❌ Erreur de connexion Redis: {e}")
            self.redis_client = None
    
    def is_available(self) -> bool:
        """Vérifie si Redis est disponible"""
        try:
            if self.redis_client:
                self.redis_client.ping()
                return True
            return False
        except:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur du cache"""
        try:
            if not self.is_available():
                self.stats["misses"] += 1
                return default
            
            value = self.redis_client.get(key)
            
            if value is not None:
                self.stats["hits"] += 1
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            else:
                self.stats["misses"] += 1
                return default
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du cache: {e}")
            self.stats["errors"] += 1
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, data_type: str = "response") -> bool:
        """Stocke une valeur dans le cache"""
        try:
            if not self.is_available():
                return False
            
            # Déterminer le TTL
            if ttl is None:
                ttl = self.ttl_config.get(data_type, self.default_ttl)
            
            # Sérialiser la valeur
            if isinstance(value, (dict, list, tuple)):
                serialized_value = json.dumps(value, ensure_ascii=False)
            else:
                serialized_value = str(value)
            
            # Stocker avec TTL
            success = self.redis_client.setex(key, ttl, serialized_value)
            
            if success:
                self.stats["sets"] += 1
                logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
            
            return success
            
        except Exception as e:
            logger.error(f"Erreur lors du stockage en cache: {e}")
            self.stats["errors"] += 1
            return False
    
    def delete(self, key: str) -> bool:
        """Supprime une clé du cache"""
        try:
            if not self.is_available():
                return False
            
            success = self.redis_client.delete(key) > 0
            
            if success:
                self.stats["deletes"] += 1
                logger.debug(f"Cache DELETE: {key}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du cache: {e}")
            self.stats["errors"] += 1
            return False
    
    def exists(self, key: str) -> bool:
        """Vérifie si une clé existe dans le cache"""
        try:
            if not self.is_available():
                return False
            
            return self.redis_client.exists(key) > 0
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification d'existence: {e}")
            return False
    
    def expire(self, key: str, ttl: int) -> bool:
        """Définit le TTL d'une clé existante"""
        try:
            if not self.is_available():
                return False
            
            return self.redis_client.expire(key, ttl)
            
        except Exception as e:
            logger.error(f"Erreur lors de la définition du TTL: {e}")
            return False
    
    def ttl(self, key: str) -> int:
        """Récupère le TTL restant d'une clé"""
        try:
            if not self.is_available():
                return -1
            
            return self.redis_client.ttl(key)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du TTL: {e}")
            return -1
    
    def clear_pattern(self, pattern: str) -> int:
        """Supprime toutes les clés correspondant à un pattern"""
        try:
            if not self.is_available():
                return 0
            
            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Suppression de {deleted} clés correspondant au pattern: {pattern}")
                return deleted
            return 0
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression par pattern: {e}")
            return 0
    
    def get_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Génère une clé de cache unique"""
        # Créer une chaîne de caractères à partir des arguments
        key_parts = [prefix]
        
        # Ajouter les arguments positionnels
        for arg in args:
            key_parts.append(str(arg))
        
        # Ajouter les arguments nommés (triés pour la cohérence)
        for key, value in sorted(kwargs.items()):
            key_parts.append(f"{key}:{value}")
        
        # Joindre et hasher
        key_string = "|".join(key_parts)
        return f"parcinfo:{prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def cache_response(self, query: str, response: Dict[str, Any], ttl: Optional[int] = None) -> str:
        """Cache une réponse de chatbot"""
        cache_key = self.get_cache_key("response", query)
        self.set(cache_key, response, ttl, "response")
        return cache_key
    
    def get_cached_response(self, query: str) -> Optional[Dict[str, Any]]:
        """Récupère une réponse mise en cache"""
        cache_key = self.get_cache_key("response", query)
        return self.get(cache_key)
    
    def cache_embedding(self, text: str, embedding: List[float], ttl: Optional[int] = None) -> str:
        """Cache un embedding"""
        cache_key = self.get_cache_key("embedding", text)
        self.set(cache_key, embedding, ttl, "embedding")
        return cache_key
    
    def get_cached_embedding(self, text: str) -> Optional[List[float]]:
        """Récupère un embedding mis en cache"""
        cache_key = self.get_cache_key("embedding", text)
        return self.get(cache_key)
    
    def cache_intent(self, query: str, intent: str, confidence: float, ttl: Optional[int] = None) -> str:
        """Cache un résultat de classification d'intent"""
        cache_key = self.get_cache_key("intent", query)
        intent_data = {"intent": intent, "confidence": confidence, "timestamp": time.time()}
        self.set(cache_key, intent_data, ttl, "intent")
        return cache_key
    
    def get_cached_intent(self, query: str) -> Optional[Dict[str, Any]]:
        """Récupère un intent mis en cache"""
        cache_key = self.get_cache_key("intent", query)
        return self.get(cache_key)
    
    def cache_user_session(self, user_id: str, session_data: Dict[str, Any], ttl: Optional[int] = None) -> str:
        """Cache les données de session utilisateur"""
        cache_key = self.get_cache_key("user_session", user_id)
        self.set(cache_key, session_data, ttl, "user_session")
        return cache_key
    
    def get_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Récupère la session utilisateur mise en cache"""
        cache_key = self.get_cache_key("user_session", user_id)
        return self.get(cache_key)
    
    def cache_database_query(self, query_hash: str, result: Any, ttl: Optional[int] = None) -> str:
        """Cache le résultat d'une requête de base de données"""
        cache_key = self.get_cache_key("db_query", query_hash)
        self.set(cache_key, result, ttl, "database_query")
        return cache_key
    
    def get_cached_database_query(self, query_hash: str) -> Optional[Any]:
        """Récupère le résultat d'une requête DB mise en cache"""
        cache_key = self.get_cache_key("db_query", query_hash)
        return self.get(cache_key)
    
    def invalidate_user_cache(self, user_id: str) -> int:
        """Invalide le cache d'un utilisateur spécifique"""
        pattern = f"parcinfo:*:{hashlib.md5(user_id.encode()).hexdigest()}"
        return self.clear_pattern(pattern)
    
    def invalidate_response_cache(self) -> int:
        """Invalide tout le cache des réponses"""
        pattern = "parcinfo:response:*"
        return self.clear_pattern(pattern)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques du cache"""
        try:
            if not self.is_available():
                return {"status": "unavailable", "stats": self.stats}
            
            # Statistiques Redis
            info = self.redis_client.info()
            redis_stats = {
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
            
            # Calculer le hit rate
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "status": "available",
                "redis_stats": redis_stats,
                "cache_stats": self.stats,
                "hit_rate": f"{hit_rate:.1f}%",
                "total_requests": total_requests
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {"status": "error", "error": str(e), "stats": self.stats}
    
    def health_check(self) -> Dict[str, Any]:
        """Vérifie la santé du cache Redis"""
        try:
            if not self.is_available():
                return {"status": "unhealthy", "reason": "Redis non disponible"}
            
            # Test de performance
            start_time = time.time()
            test_key = "health_check_test"
            test_value = {"test": "value", "timestamp": time.time()}
            
            # Test SET
            set_success = self.set(test_key, test_value, 10)
            if not set_success:
                return {"status": "unhealthy", "reason": "Échec du test SET"}
            
            # Test GET
            retrieved_value = self.get(test_key)
            if retrieved_value != test_value:
                return {"status": "unhealthy", "reason": "Échec du test GET"}
            
            # Test DELETE
            delete_success = self.delete(test_key)
            if not delete_success:
                return {"status": "unhealthy", "reason": "Échec du test DELETE"}
            
            performance_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "performance_ms": round(performance_time * 1000, 2),
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"status": "unhealthy", "reason": f"Exception: {str(e)}"}
    
    def cleanup(self):
        """Nettoie les ressources Redis"""
        try:
            if self.redis_client:
                self.redis_client.close()
            if self.connection_pool:
                self.connection_pool.disconnect()
            logger.info("Ressources Redis nettoyées")
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage Redis: {e}")

# Décorateur pour mettre en cache automatiquement
def cached_response(ttl: Optional[int] = None, data_type: str = "response"):
    """Décorateur pour mettre en cache automatiquement les réponses"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Créer une instance du cache manager
            cache_manager = RedisCacheManager()
            
            # Générer la clé de cache
            cache_key = cache_manager.get_cache_key(func.__name__, *args, **kwargs)
            
            # Essayer de récupérer du cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache HIT pour {func.__name__}")
                return cached_result
            
            # Exécuter la fonction
            result = func(*args, **kwargs)
            
            # Mettre en cache le résultat
            cache_manager.set(cache_key, result, ttl, data_type)
            logger.debug(f"Cache SET pour {func.__name__}")
            
            return result
        return wrapper
    return decorator

# Instance globale du cache manager
_cache_manager = None

def get_cache_manager() -> RedisCacheManager:
    """Retourne l'instance globale du cache manager"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = RedisCacheManager()
    return _cache_manager

def main():
    """Fonction principale pour tester le cache Redis"""
    logging.basicConfig(level=logging.INFO)
    
    # Créer le cache manager
    cache_manager = RedisCacheManager()
    
    if not cache_manager.is_available():
        print("❌ Redis non disponible. Vérifiez que Redis est démarré.")
        return
    
    print("✅ Redis disponible!")
    
    # Test des fonctionnalités de base
    print("\n🧪 Test des fonctionnalités de base:")
    
    # Test SET/GET
    test_data = {"message": "Hello Redis!", "timestamp": time.time()}
    cache_key = cache_manager.set("test_key", test_data, 60)
    print(f"SET: {cache_key}")
    
    retrieved_data = cache_manager.get("test_key")
    print(f"GET: {retrieved_data}")
    
    # Test des clés de cache
    print("\n🔑 Test des clés de cache:")
    
    response_key = cache_manager.cache_response("Code inventaire de la Baie", {"intent": "codes_by_designation"})
    print(f"Clé de réponse: {response_key}")
    
    embedding_key = cache_manager.cache_embedding("test text", [0.1, 0.2, 0.3])
    print(f"Clé d'embedding: {embedding_key}")
    
    # Test des statistiques
    print("\n📊 Statistiques du cache:")
    stats = cache_manager.get_cache_stats()
    print(f"Statut: {stats['status']}")
    print(f"Hit rate: {stats['hit_rate']}")
    print(f"Requêtes totales: {stats['total_requests']}")
    
    # Test de santé
    print("\n🏥 Test de santé:")
    health = cache_manager.health_check()
    print(f"Statut: {health['status']}")
    if health['status'] == 'healthy':
        print(f"Performance: {health['performance_ms']}ms")
    
    # Nettoyer
    cache_manager.delete("test_key")
    cache_manager.cleanup()
    
    print("\n✅ Tests terminés avec succès!")

if __name__ == "__main__":
    main()
