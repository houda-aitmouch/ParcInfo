#!/usr/bin/env python3
"""
Script de test de performance pour vérifier les performances du projet
"""

import os
import sys
import time
import django
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

class PerformanceTest:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8001"
        self.results = []
        
    def test_single_request(self, url, description):
        """Test une requête unique"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}{url}", timeout=10)
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'url': url,
                'description': description,
                'status_code': response.status_code,
                'duration': duration,
                'success': response.status_code in [200, 302, 403]
            }
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            return {
                'url': url,
                'description': description,
                'status_code': 'ERROR',
                'duration': duration,
                'success': False,
                'error': str(e)
            }
    
    def test_concurrent_requests(self, urls, max_workers=5):
        """Test des requêtes concurrentes"""
        print(f"🧪 Test de {len(urls)} requêtes concurrentes (max {max_workers} workers)...")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.test_single_request, url, desc): (url, desc)
                for url, desc in urls
            }
            
            for future in as_completed(future_to_url):
                result = future.result()
                self.results.append(result)
                
        end_time = time.time()
        total_duration = end_time - start_time
        
        return total_duration
    
    def test_database_performance(self):
        """Test des performances de la base de données"""
        print("🧪 Test des performances de la base de données...")
        
        from django.db import connection
        from apps.users.models import CustomUser
        from apps.materiel_informatique.models import MaterielInformatique
        from apps.materiel_bureautique.models import MaterielBureau
        from apps.livraison.models import Livraison
        
        start_time = time.time()
        
        # Test requêtes simples
        user_count = CustomUser.objects.count()
        materiel_it_count = MaterielInformatique.objects.count()
        materiel_bureau_count = MaterielBureau.objects.count()
        livraison_count = Livraison.objects.count()
        
        # Test requêtes avec filtres
        users_with_groups = CustomUser.objects.filter(groups__isnull=False).count()
        materiels_operatifs = MaterielInformatique.objects.filter(statut='Opérationnel').count()
        
        # Test requêtes avec relations
        materiels_with_users = MaterielInformatique.objects.select_related('utilisateur').count()
        
        end_time = time.time()
        db_duration = end_time - start_time
        
        print(f"✅ Requêtes DB: {db_duration:.3f}s")
        print(f"   - Users: {user_count}")
        print(f"   - Matériels IT: {materiel_it_count}")
        print(f"   - Matériels Bureau: {materiel_bureau_count}")
        print(f"   - Livraisons: {livraison_count}")
        
        return db_duration
    
    def run_performance_tests(self):
        """Exécuter tous les tests de performance"""
        print("🚀 Test de performance du projet ParcInfo")
        print("=" * 60)
        
        # URLs à tester
        test_urls = [
            ("/", "Page d'accueil"),
            ("/admin/", "Admin Django"),
            ("/gestionnaire_info/", "Dashboard gestionnaire info"),
            ("/materiels/mes-equipements/", "Mes équipements IT"),
            ("/materiels-bureau/mes-equipements/", "Mes équipements Bureau"),
            ("/livraisons/gestionnaire-info/liste/", "Liste livraisons"),
            ("/fournisseurs/", "Liste fournisseurs"),
        ]
        
        # Test requêtes séquentielles
        print("🧪 Test requêtes séquentielles...")
        sequential_start = time.time()
        for url, desc in test_urls:
            result = self.test_single_request(url, desc)
            self.results.append(result)
            print(f"   {desc}: {result['duration']:.3f}s ({result['status_code']})")
        
        sequential_duration = time.time() - sequential_start
        print(f"✅ Durée totale séquentielle: {sequential_duration:.3f}s")
        
        # Test requêtes concurrentes
        concurrent_duration = self.test_concurrent_requests(test_urls, max_workers=3)
        print(f"✅ Durée totale concurrente: {concurrent_duration:.3f}s")
        
        # Test base de données
        db_duration = self.test_database_performance()
        
        # Résumé
        print("\n" + "=" * 60)
        print("📊 Résumé des performances:")
        
        successful_requests = sum(1 for r in self.results if r['success'])
        total_requests = len(self.results)
        avg_duration = sum(r['duration'] for r in self.results) / len(self.results)
        
        print(f"✅ Requêtes réussies: {successful_requests}/{total_requests}")
        print(f"⏱️ Durée moyenne par requête: {avg_duration:.3f}s")
        print(f"🚀 Amélioration concurrentielle: {sequential_duration/concurrent_duration:.1f}x")
        print(f"🗄️ Temps base de données: {db_duration:.3f}s")
        
        # Évaluation
        if avg_duration < 1.0 and successful_requests == total_requests:
            print("\n🎉 EXCELLENT: Performances optimales !")
            return True
        elif avg_duration < 2.0 and successful_requests >= total_requests * 0.9:
            print("\n✅ BON: Performances satisfaisantes")
            return True
        else:
            print("\n⚠️ ATTENTION: Performances à améliorer")
            return False

def main():
    """Fonction principale"""
    test = PerformanceTest()
    success = test.run_performance_tests()
    
    if not success:
        print("\n💡 Conseils d'optimisation:")
        print("1. Vérifiez la configuration de la base de données")
        print("2. Optimisez les requêtes avec select_related/prefetch_related")
        print("3. Utilisez le cache pour les données statiques")
        print("4. Vérifiez la configuration du serveur web")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
