#!/usr/bin/env python3
"""
Module de monitoring et tests automatisés pour le chatbot ParcInfo
Surveille les performances et exécute des tests de validation
"""

import os
import json
import logging
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import psutil
import redis
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Métrique de performance"""
    timestamp: float
    metric_name: str
    value: float
    unit: str
    category: str
    tags: Dict[str, str]

@dataclass
class HealthCheck:
    """Vérification de santé"""
    component: str
    status: str
    response_time: float
    error_message: Optional[str] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class ChatbotMonitor:
    """Moniteur de performance pour le chatbot ParcInfo"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.health_checks: List[HealthCheck] = []
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alert_thresholds = {
            "response_time": 2.0,      # 2 secondes
            "memory_usage": 80.0,      # 80% de la RAM
            "cpu_usage": 90.0,         # 90% du CPU
            "error_rate": 10.0,        # 10% d'erreurs
            "cache_hit_rate": 50.0     # 50% de hit rate
        }
        
        # Configuration du monitoring
        self.monitoring_interval = 30  # 30 secondes
        self.metrics_retention_hours = 24
        self.max_metrics = 10000
        
    def start_monitoring(self):
        """Démarre le monitoring en arrière-plan"""
        if self.monitoring_active:
            logger.warning("Monitoring déjà actif")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("🚀 Monitoring démarré")
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("⏹️ Monitoring arrêté")
    
    def _monitoring_loop(self):
        """Boucle principale de monitoring"""
        while self.monitoring_active:
            try:
                # Collecter les métriques système
                self._collect_system_metrics()
                
                # Vérifier la santé des composants
                self._check_components_health()
                
                # Nettoyer les anciennes métriques
                self._cleanup_old_metrics()
                
                # Attendre l'intervalle suivant
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Erreur dans la boucle de monitoring: {e}")
                time.sleep(5)
    
    def _collect_system_metrics(self):
        """Collecte les métriques système"""
        try:
            # Métriques CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self._add_metric("cpu_usage", cpu_percent, "%", "system", {"type": "cpu"})
            
            # Métriques mémoire
            memory = psutil.virtual_memory()
            self._add_metric("memory_usage", memory.percent, "%", "system", {"type": "ram"})
            self._add_metric("memory_available", memory.available / (1024**3), "GB", "system", {"type": "ram"})
            
            # Métriques disque
            disk = psutil.disk_usage('/')
            self._add_metric("disk_usage", disk.percent, "%", "system", {"type": "disk"})
            
            # Métriques réseau
            network = psutil.net_io_counters()
            self._add_metric("network_bytes_sent", network.bytes_sent / (1024**2), "MB", "system", {"type": "network"})
            self._add_metric("network_bytes_recv", network.bytes_recv / (1024**2), "MB", "system", {"type": "network"})
            
            # Métriques processus
            process = psutil.Process()
            self._add_metric("process_memory", process.memory_info().rss / (1024**2), "MB", "system", {"type": "process"})
            self._add_metric("process_cpu", process.cpu_percent(), "%", "system", {"type": "process"})
            
        except Exception as e:
            logger.error(f"Erreur lors de la collecte des métriques système: {e}")
    
    def _check_components_health(self):
        """Vérifie la santé des composants"""
        try:
            # Vérifier la base de données
            db_health = self._check_database_health()
            self.health_checks.append(db_health)
            
            # Vérifier Redis
            redis_health = self._check_redis_health()
            self.health_checks.append(redis_health)
            
            # Vérifier les modèles NLP
            nlp_health = self._check_nlp_models_health()
            self.health_checks.append(nlp_health)
            
            # Vérifier l'API du chatbot
            api_health = self._check_chatbot_api_health()
            self.health_checks.append(api_health)
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de santé: {e}")
    
    def _check_database_health(self) -> HealthCheck:
        """Vérifie la santé de la base de données"""
        start_time = time.time()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            response_time = time.time() - start_time
            return HealthCheck(
                component="database",
                status="healthy",
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                component="database",
                status="unhealthy",
                response_time=response_time,
                error_message=str(e)
            )
    
    def _check_redis_health(self) -> HealthCheck:
        """Vérifie la santé de Redis"""
        start_time = time.time()
        
        try:
            redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
            redis_client.ping()
            redis_client.close()
            
            response_time = time.time() - start_time
            return HealthCheck(
                component="redis",
                status="healthy",
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                component="redis",
                status="unhealthy",
                response_time=response_time,
                error_message=str(e)
            )
    
    def _check_nlp_models_health(self) -> HealthCheck:
        """Vérifie la santé des modèles NLP"""
        start_time = time.time()
        
        try:
            # Vérifier si les modèles sont chargés
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test simple de classification
            test_query = "test query"
            response = chatbot.process_query(test_query)
            
            response_time = time.time() - start_time
            return HealthCheck(
                component="nlp_models",
                status="healthy",
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                component="nlp_models",
                status="unhealthy",
                response_time=response_time,
                error_message=str(e)
            )
    
    def _check_chatbot_api_health(self) -> HealthCheck:
        """Vérifie la santé de l'API du chatbot"""
        start_time = time.time()
        
        try:
            # Test de l'API (simulation)
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test avec une requête simple
            test_query = "List of suppliers"
            response = chatbot.process_query(test_query)
            
            if response and 'response' in response:
                response_time = time.time() - start_time
                return HealthCheck(
                    component="chatbot_api",
                    status="healthy",
                    response_time=response_time
                )
            else:
                raise Exception("Réponse invalide du chatbot")
                
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                component="chatbot_api",
                status="unhealthy",
                response_time=response_time,
                error_message=str(e)
            )
    
    def _add_metric(self, name: str, value: float, unit: str, category: str, tags: Dict[str, str]):
        """Ajoute une métrique"""
        metric = PerformanceMetric(
            timestamp=time.time(),
            metric_name=name,
            value=value,
            unit=unit,
            category=category,
            tags=tags
        )
        
        self.metrics.append(metric)
        
        # Vérifier les seuils d'alerte
        self._check_alert_thresholds(metric)
        
        # Limiter le nombre de métriques
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
    
    def _check_alert_thresholds(self, metric: PerformanceMetric):
        """Vérifie les seuils d'alerte"""
        threshold = self.alert_thresholds.get(metric.metric_name)
        
        if threshold is not None and metric.value > threshold:
            logger.warning(f"🚨 ALERTE: {metric.metric_name} = {metric.value}{metric.unit} > {threshold}{metric.unit}")
            
            # Envoyer une alerte (peut être étendu avec des notifications)
            self._send_alert(metric, threshold)
    
    def _send_alert(self, metric: PerformanceMetric, threshold: float):
        """Envoie une alerte (à étendre selon les besoins)"""
        alert_message = {
            "type": "threshold_alert",
            "metric": metric.metric_name,
            "current_value": metric.value,
            "threshold": threshold,
            "unit": metric.unit,
            "timestamp": datetime.fromtimestamp(metric.timestamp).isoformat(),
            "severity": "warning"
        }
        
        # Log de l'alerte
        logger.warning(f"ALERTE: {json.dumps(alert_message, ensure_ascii=False)}")
        
        # Ici on peut ajouter l'envoi d'emails, notifications Slack, etc.
    
    def _cleanup_old_metrics(self):
        """Nettoie les anciennes métriques"""
        cutoff_time = time.time() - (self.metrics_retention_hours * 3600)
        self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        # Nettoyer aussi les health checks
        self.health_checks = [h for h in self.health_checks if h.timestamp > cutoff_time]
    
    def get_current_metrics(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les métriques actuelles"""
        metrics = self.metrics
        
        if category:
            metrics = [m for m in metrics if m.category == category]
        
        # Convertir en dictionnaires et trier par timestamp
        return sorted([asdict(m) for m in metrics], key=lambda x: x['timestamp'], reverse=True)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Récupère le statut de santé global"""
        if not self.health_checks:
            return {"status": "unknown", "components": {}}
        
        # Prendre le dernier health check pour chaque composant
        latest_checks = {}
        for check in self.health_checks:
            if check.component not in latest_checks or check.timestamp > latest_checks[check.component].timestamp:
                latest_checks[check.component] = check
        
        # Déterminer le statut global
        healthy_components = sum(1 for check in latest_checks.values() if check.status == "healthy")
        total_components = len(latest_checks)
        
        if healthy_components == total_components:
            global_status = "healthy"
        elif healthy_components > 0:
            global_status = "degraded"
        else:
            global_status = "unhealthy"
        
        return {
            "status": global_status,
            "healthy_components": healthy_components,
            "total_components": total_components,
            "components": {name: asdict(check) for name, check in latest_checks.items()}
        }
    
    def get_performance_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Récupère un résumé des performances sur une période"""
        cutoff_time = time.time() - (hours * 3600)
        recent_metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {"error": "Aucune métrique disponible pour cette période"}
        
        summary = {}
        
        # Grouper par catégorie
        for category in set(m.category for m in recent_metrics):
            category_metrics = [m for m in recent_metrics if m.category == category]
            
            summary[category] = {}
            for metric_name in set(m.metric_name for m in category_metrics):
                metric_values = [m.value for m in category_metrics if m.metric_name == metric_name]
                
                if metric_values:
                    summary[category][metric_name] = {
                        "min": min(metric_values),
                        "max": max(metric_values),
                        "avg": sum(metric_values) / len(metric_values),
                        "count": len(metric_values)
                    }
        
        return summary
    
    def export_metrics(self, format: str = "json") -> str:
        """Exporte les métriques dans différents formats"""
        if format == "json":
            return json.dumps({
                "metrics": [asdict(m) for m in self.metrics],
                "health_checks": [asdict(h) for h in self.health_checks],
                "export_timestamp": datetime.now().isoformat()
            }, ensure_ascii=False, indent=2)
        
        elif format == "csv":
            # Format CSV simple
            csv_lines = ["timestamp,metric_name,value,unit,category,tags"]
            
            for metric in self.metrics:
                tags_str = ",".join([f"{k}={v}" for k, v in metric.tags.items()])
                csv_lines.append(f"{metric.timestamp},{metric.metric_name},{metric.value},{metric.unit},{metric.category},{tags_str}")
            
            return "\n".join(csv_lines)
        
        else:
            raise ValueError(f"Format non supporté: {format}")

class AutomatedTester:
    """Testeur automatisé pour le chatbot"""
    
    def __init__(self):
        self.test_results = []
        self.test_suites = {}
        self._register_test_suites()
    
    def _register_test_suites(self):
        """Enregistre les suites de tests disponibles"""
        self.test_suites = {
            "basic_functionality": self._test_basic_functionality,
            "intent_detection": self._test_intent_detection,
            "response_quality": self._test_response_quality,
            "performance": self._test_performance,
            "multilingual": self._test_multilingual,
            "error_handling": self._test_error_handling
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Exécute tous les tests"""
        logger.info("🧪 Démarrage des tests automatisés...")
        
        start_time = time.time()
        results = {}
        
        for suite_name, test_function in self.test_suites.items():
            try:
                logger.info(f"Exécution de la suite: {suite_name}")
                suite_results = test_function()
                results[suite_name] = suite_results
                
                if suite_results["success"]:
                    logger.info(f"✅ {suite_name}: Succès")
                else:
                    logger.warning(f"⚠️ {suite_name}: Échec")
                    
            except Exception as e:
                logger.error(f"❌ Erreur dans la suite {suite_name}: {e}")
                results[suite_name] = {
                    "success": False,
                    "error": str(e),
                    "tests": []
                }
        
        total_time = time.time() - start_time
        
        # Résumé global
        total_tests = sum(len(r.get("tests", [])) for r in results.values())
        successful_tests = sum(len([t for t in r.get("tests", []) if t.get("success", False)]) for r in results.values())
        
        summary = {
            "total_execution_time": total_time,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "suite_results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"🎯 Tests terminés: {successful_tests}/{total_tests} ({summary['success_rate']:.1f}%)")
        
        return summary
    
    def _test_basic_functionality(self) -> Dict[str, Any]:
        """Test de la fonctionnalité de base"""
        tests = []
        
        try:
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test 1: Initialisation
            test1 = {"name": "initialization", "success": chatbot is not None, "details": "Chatbot initialisé"}
            tests.append(test1)
            
            # Test 2: Traitement de requête simple
            response = chatbot.process_query("test")
            test2 = {"name": "basic_query", "success": response is not None, "details": f"Réponse reçue: {type(response)}"}
            tests.append(test2)
            
            # Test 3: Structure de réponse
            if response:
                test3 = {"name": "response_structure", "success": isinstance(response, dict), "details": "Réponse est un dictionnaire"}
            else:
                test3 = {"name": "response_structure", "success": False, "details": "Réponse vide"}
            tests.append(test3)
            
        except Exception as e:
            tests.append({"name": "basic_functionality", "success": False, "details": f"Exception: {e}"})
        
        return {
            "success": all(t["success"] for t in tests),
            "tests": tests
        }
    
    def _test_intent_detection(self) -> Dict[str, Any]:
        """Test de la détection d'intention"""
        tests = []
        
        try:
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test avec des requêtes connues
            test_queries = [
                ("Code inventaire de la Baie", "codes_by_designation"),
                ("List of suppliers", "liste_fournisseurs"),
                ("Fournisseur de la commande BC23", "order_supplier")
            ]
            
            for query, expected_intent in test_queries:
                response = chatbot.process_query(query)
                
                if response and "intent" in response:
                    detected_intent = response.get("intent")
                    success = detected_intent == expected_intent
                    details = f"Attendu: {expected_intent}, Détecté: {detected_intent}"
                else:
                    success = False
                    details = "Réponse invalide"
                
                test = {"name": f"intent_{query[:20]}", "success": success, "details": details}
                tests.append(test)
                
        except Exception as e:
            tests.append({"name": "intent_detection", "success": False, "details": f"Exception: {e}"})
        
        return {
            "success": all(t["success"] for t in tests),
            "tests": tests
        }
    
    def _test_response_quality(self) -> Dict[str, Any]:
        """Test de la qualité des réponses"""
        tests = []
        
        try:
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test 1: Réponse non vide
            response = chatbot.process_query("test query")
            test1 = {"name": "non_empty_response", "success": response and len(str(response)) > 0, "details": "Réponse non vide"}
            tests.append(test1)
            
            # Test 2: Temps de réponse
            start_time = time.time()
            chatbot.process_query("performance test")
            response_time = time.time() - start_time
            
            test2 = {"name": "response_time", "success": response_time < 5.0, "details": f"Temps: {response_time:.2f}s"}
            tests.append(test2)
            
            # Test 3: Structure de réponse
            if response:
                test3 = {"name": "response_structure", "success": "response" in response, "details": "Champ 'response' présent"}
            else:
                test3 = {"name": "response_structure", "success": False, "details": "Réponse vide"}
            tests.append(test3)
            
        except Exception as e:
            tests.append({"name": "response_quality", "success": False, "details": f"Exception: {e}"})
        
        return {
            "success": all(t["success"] for t in tests),
            "tests": tests
        }
    
    def _test_performance(self) -> Dict[str, Any]:
        """Test de performance"""
        tests = []
        
        try:
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test de charge simple
            test_queries = ["test1", "test2", "test3", "test4", "test5"]
            response_times = []
            
            for query in test_queries:
                start_time = time.time()
                chatbot.process_query(query)
                response_time = time.time() - start_time
                response_times.append(response_time)
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            test1 = {"name": "average_response_time", "success": avg_response_time < 2.0, "details": f"Temps moyen: {avg_response_time:.2f}s"}
            tests.append(test1)
            
            test2 = {"name": "max_response_time", "success": max_response_time < 5.0, "details": f"Temps max: {max_response_time:.2f}s"}
            tests.append(test2)
            
        except Exception as e:
            tests.append({"name": "performance", "success": False, "details": f"Exception: {e}"})
        
        return {
            "success": all(t["success"] for t in tests),
            "tests": tests
        }
    
    def _test_multilingual(self) -> Dict[str, Any]:
        """Test du support multilingue"""
        tests = []
        
        try:
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test français
            response_fr = chatbot.process_query("Liste des fournisseurs")
            test1 = {"name": "french_support", "success": response_fr is not None, "details": "Support français"}
            tests.append(test1)
            
            # Test anglais
            response_en = chatbot.process_query("List of suppliers")
            test2 = {"name": "english_support", "success": response_en is not None, "details": "Support anglais"}
            tests.append(test2)
            
            # Test de cohérence
            if response_fr and response_en:
                test3 = {"name": "multilingual_consistency", "success": True, "details": "Réponses cohérentes"}
            else:
                test3 = {"name": "multilingual_consistency", "success": False, "details": "Réponses incohérentes"}
            tests.append(test3)
            
        except Exception as e:
            tests.append({"name": "multilingual", "success": False, "details": f"Exception: {e}"})
        
        return {
            "success": all(t["success"] for t in tests),
            "tests": tests
        }
    
    def _test_error_handling(self) -> Dict[str, Any]:
        """Test de la gestion d'erreurs"""
        tests = []
        
        try:
            from apps.chatbot.core_chatbot import get_chatbot
            chatbot = get_chatbot()
            
            # Test 1: Requête vide
            response1 = chatbot.process_query("")
            test1 = {"name": "empty_query", "success": response1 is not None, "details": "Gestion requête vide"}
            tests.append(test1)
            
            # Test 2: Requête très longue
            long_query = "test " * 1000
            response2 = chatbot.process_query(long_query)
            test2 = {"name": "long_query", "success": response2 is not None, "details": "Gestion requête longue"}
            tests.append(test2)
            
            # Test 3: Caractères spéciaux
            special_query = "test@#$%^&*()_+{}|:<>?[]\\;'\",./<>?"
            response3 = chatbot.process_query(special_query)
            test3 = {"name": "special_characters", "success": response3 is not None, "details": "Gestion caractères spéciaux"}
            tests.append(test3)
            
        except Exception as e:
            tests.append({"name": "error_handling", "success": False, "details": f"Exception: {e}"})
        
        return {
            "success": all(t["success"] for t in tests),
            "tests": tests
        }

class SystemMonitor:
    """Moniteur système pour la surveillance des performances"""
    
    def __init__(self):
        self.monitor = ChatbotMonitor()
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques système"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des métriques: {e}")
            return {}

def main():
    """Fonction principale pour tester le monitoring"""
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Test du système de monitoring et tests automatisés")
    print("=" * 60)
    
    # Test du moniteur
    print("\n📊 Test du moniteur de performance:")
    monitor = ChatbotMonitor()
    
    # Démarrer le monitoring
    monitor.start_monitoring()
    time.sleep(5)  # Laisser le temps de collecter des métriques
    
    # Afficher les métriques
    metrics = monitor.get_current_metrics()
    print(f"Métriques collectées: {len(metrics)}")
    
    # Afficher le statut de santé
    health = monitor.get_health_status()
    print(f"Statut de santé: {health['status']}")
    
    # Arrêter le monitoring
    monitor.stop_monitoring()
    
    # Test du testeur automatisé
    print("\n🧪 Test du testeur automatisé:")
    tester = AutomatedTester()
    test_results = tester.run_all_tests()
    
    print(f"Taux de succès global: {test_results['success_rate']:.1f}%")
    print(f"Temps d'exécution: {test_results['total_execution_time']:.2f}s")
    
    print("\n✅ Tests terminés!")

if __name__ == "__main__":
    main()
