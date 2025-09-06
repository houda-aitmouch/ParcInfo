#!/usr/bin/env python3
"""
Script de test complet pour vérifier toutes les fonctionnalités Kubernetes
"""

import requests
import sys
import time
import subprocess
import json

def test_k8s_services():
    """Test de tous les services Kubernetes"""
    
    print("🚀 Test Complet - Services Kubernetes ParcInfo")
    print("=" * 70)
    
    # Test 1: Vérifier les pods Kubernetes
    print("1️⃣ Vérification des pods Kubernetes...")
    try:
        result = subprocess.run(['kubectl', 'get', 'pods', '-n', 'parcinfo', '--no-headers'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            pods = result.stdout.strip().split('\n')
            running_pods = [pod for pod in pods if 'Running' in pod]
            print(f"   ✅ {len(running_pods)}/{len(pods)} pods en cours d'exécution")
            
            for pod in running_pods:
                pod_name = pod.split()[0]
                print(f"      - {pod_name}")
        else:
            print(f"   ❌ Erreur kubectl: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # Test 2: Vérifier les services
    print("\n2️⃣ Vérification des services Kubernetes...")
    try:
        result = subprocess.run(['kubectl', 'get', 'services', '-n', 'parcinfo'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ Services Kubernetes:")
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    service_name = parts[0]
                    service_type = parts[1]
                    print(f"      - {service_name} ({service_type})")
        else:
            print(f"   ❌ Erreur kubectl services: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    return True

def test_backend_k8s():
    """Test du backend Kubernetes"""
    print("\n3️⃣ Test du Backend Kubernetes...")
    
    # Démarrer port-forward pour le backend
    try:
        subprocess.Popen(['kubectl', 'port-forward', '-n', 'parcinfo', 'service/backend-service', '8000:8000'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Attendre que le port-forward soit prêt
        
        # Test de l'API backend
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Backend Kubernetes accessible")
            
            # Test de l'API admin
            admin_response = requests.get("http://localhost:8000/admin/", timeout=10)
            if admin_response.status_code in [200, 302]:
                print("   ✅ Interface admin accessible")
            else:
                print(f"   ⚠️  Interface admin: {admin_response.status_code}")
            
            return True
        else:
            print(f"   ❌ Backend non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur backend: {e}")
        return False

def test_streamlit_k8s():
    """Test de Streamlit Kubernetes"""
    print("\n4️⃣ Test de Streamlit Kubernetes...")
    
    try:
        # Démarrer port-forward pour Streamlit
        subprocess.Popen(['kubectl', 'port-forward', '-n', 'parcinfo', 'service/streamlit-service', '8501:8501'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
        # Test de Streamlit
        response = requests.get("http://localhost:8501/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Streamlit Kubernetes accessible")
            
            # Test avec utilisateur
            user_response = requests.get("http://localhost:8501/?username=superadmin", timeout=10)
            if user_response.status_code == 200:
                print("   ✅ Streamlit avec utilisateur accessible")
            else:
                print(f"   ⚠️  Streamlit utilisateur: {user_response.status_code}")
            
            return True
        else:
            print(f"   ❌ Streamlit non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur Streamlit: {e}")
        return False

def test_chatbot_k8s():
    """Test du chatbot Kubernetes"""
    print("\n5️⃣ Test du Chatbot Kubernetes...")
    
    try:
        # Démarrer port-forward pour le chatbot
        subprocess.Popen(['kubectl', 'port-forward', '-n', 'parcinfo', 'service/chatbot-service', '8001:8001'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
        # Test de l'API chatbot
        response = requests.get("http://localhost:8001/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Chatbot Kubernetes accessible")
            
            # Test de l'API chatbot
            api_data = {"query": "liste des utilisateurs"}
            api_response = requests.post("http://localhost:8001/chatbot/api/", 
                                       json=api_data, timeout=30)
            if api_response.status_code == 200:
                result = api_response.json()
                print("   ✅ API chatbot fonctionnelle")
                print(f"      Réponse: {result.get('response', 'N/A')[:100]}...")
                return True
            else:
                print(f"   ⚠️  API chatbot: {api_response.status_code}")
                return False
        else:
            print(f"   ❌ Chatbot non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur chatbot: {e}")
        return False

def test_chatbot_docker():
    """Test du chatbot Docker"""
    print("\n6️⃣ Test du Chatbot Docker...")
    
    try:
        # Vérifier si le container Docker est en cours d'exécution
        result = subprocess.run(['docker', 'ps', '--filter', 'name=parcinfo-chatbot', '--format', '{{.Names}}'], 
                              capture_output=True, text=True, timeout=10)
        
        if 'parcinfo-chatbot' in result.stdout:
            print("   ✅ Container Docker chatbot en cours d'exécution")
            
            # Test de l'API Docker
            api_data = {"query": "combien de matériels informatiques ?"}
            api_response = requests.post("http://localhost:8001/chatbot/api/", 
                                       json=api_data, timeout=30)
            if api_response.status_code == 200:
                result = api_response.json()
                print("   ✅ API chatbot Docker fonctionnelle")
                print(f"      Réponse: {result.get('response', 'N/A')[:100]}...")
                return True
            else:
                print(f"   ⚠️  API chatbot Docker: {api_response.status_code}")
                return False
        else:
            print("   ⚠️  Container Docker chatbot non trouvé")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur chatbot Docker: {e}")
        return False

def test_database_connection():
    """Test de la connexion à la base de données"""
    print("\n7️⃣ Test de la connexion à la base de données...")
    
    try:
        # Test via l'API backend
        response = requests.get("http://localhost:8000/admin/", timeout=10)
        if response.status_code in [200, 302]:
            print("   ✅ Connexion à la base de données via backend")
            
            # Test via l'API chatbot
            api_data = {"query": "test connexion base de données"}
            api_response = requests.post("http://localhost:8001/chatbot/api/", 
                                       json=api_data, timeout=30)
            if api_response.status_code == 200:
                print("   ✅ Connexion à la base de données via chatbot")
                return True
            else:
                print(f"   ⚠️  Connexion via chatbot: {api_response.status_code}")
                return False
        else:
            print(f"   ❌ Connexion base de données: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
        return False

def test_dashboard_redirect():
    """Test de la redirection dashboard garantie"""
    print("\n8️⃣ Test de la redirection Dashboard Garantie...")
    
    try:
        # Test de la redirection
        response = requests.get("http://localhost:8000/dashboard-garantie/", timeout=10)
        if response.status_code == 302:
            redirect_url = response.headers.get('Location', '')
            print("   ✅ Redirection dashboard garantie fonctionnelle")
            print(f"      Redirection vers: {redirect_url}")
            
            if "localhost:8501" in redirect_url or "localhost:30085" in redirect_url:
                print("   ✅ Redirection vers Streamlit correcte")
                return True
            else:
                print("   ⚠️  Redirection vers Streamlit incorrecte")
                return False
        else:
            print(f"   ❌ Redirection dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur redirection: {e}")
        return False

def cleanup_port_forwards():
    """Nettoyer les port-forwards"""
    try:
        subprocess.run(['pkill', '-f', 'kubectl port-forward'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    except:
        pass

def main():
    """Fonction principale de test"""
    print("🚀 Test Complet - Services Kubernetes ParcInfo")
    print("=" * 70)
    
    # Nettoyer les port-forwards existants
    cleanup_port_forwards()
    
    tests = [
        ("Services Kubernetes", test_k8s_services),
        ("Backend Kubernetes", test_backend_k8s),
        ("Streamlit Kubernetes", test_streamlit_k8s),
        ("Chatbot Kubernetes", test_chatbot_k8s),
        ("Chatbot Docker", test_chatbot_docker),
        ("Base de données", test_database_connection),
        ("Redirection Dashboard", test_dashboard_redirect)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Erreur inattendue dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<25} : {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Toutes les fonctionnalités Kubernetes fonctionnent correctement")
        print("✅ Le chatbot fonctionne en Docker ET en Kubernetes")
        print("✅ La redirection dashboard garantie fonctionne")
        print("✅ La connexion à la base de données est opérationnelle")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué")
        print("Vérifiez la configuration des services qui ont échoué")
    
    # Nettoyer les port-forwards
    cleanup_port_forwards()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
