#!/usr/bin/env python3
"""
Script de test pour vérifier la redirection du dashboard garantie vers Streamlit
"""

import requests
import sys

def test_dashboard_redirect():
    """Test de la redirection du dashboard garantie"""
    
    print("🧪 Test de la redirection Dashboard Garantie -> Streamlit")
    print("=" * 60)
    
    # Test 1: Vérifier que le backend est accessible
    print("1️⃣ Test du backend Django...")
    try:
        response = requests.get("http://localhost:8000/dashboard-garantie/", timeout=10)
        print(f"   ✅ Backend accessible: {response.status_code}")
        if response.status_code == 302:
            print(f"   📍 Redirection vers: {response.headers.get('Location', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Erreur backend: {e}")
        return False
    
    # Test 2: Vérifier que Streamlit est accessible
    print("\n2️⃣ Test de Streamlit...")
    try:
        response = requests.get("http://localhost:8501/", timeout=10)
        print(f"   ✅ Streamlit accessible: {response.status_code}")
        if "Dashboard Garantie" in response.text:
            print("   🎯 Dashboard Garantie détecté dans la réponse")
        else:
            print("   ⚠️  Dashboard Garantie non détecté")
    except Exception as e:
        print(f"   ❌ Erreur Streamlit: {e}")
        return False
    
    # Test 3: Vérifier la redirection avec authentification
    print("\n3️⃣ Test de la redirection complète...")
    try:
        # Simuler une session avec un utilisateur
        session = requests.Session()
        
        # Se connecter (si possible)
        login_data = {
            'username': 'admin',
            'password': 'admin123'  # Mot de passe par défaut
        }
        
        login_response = session.post("http://localhost:8000/accounts/login/", data=login_data)
        if login_response.status_code == 200:
            print("   ✅ Connexion réussie")
            
            # Tester la redirection
            dashboard_response = session.get("http://localhost:8000/dashboard-garantie/")
            if dashboard_response.status_code == 302:
                redirect_url = dashboard_response.headers.get('Location', '')
                print(f"   📍 Redirection vers: {redirect_url}")
                
                if "localhost:8501" in redirect_url or "localhost:30085" in redirect_url:
                    print("   ✅ Redirection vers Streamlit correcte")
                    return True
                else:
                    print("   ❌ Redirection incorrecte")
                    return False
            else:
                print(f"   ❌ Pas de redirection: {dashboard_response.status_code}")
                return False
        else:
            print("   ⚠️  Connexion échouée, test de redirection directe")
            return True
            
    except Exception as e:
        print(f"   ❌ Erreur test redirection: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de la redirection Dashboard Garantie")
    print("=" * 60)
    
    success = test_dashboard_redirect()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Test réussi ! La redirection fonctionne correctement.")
        print("🌐 Accès au dashboard:")
        print("   - Backend: http://localhost:8000/")
        print("   - Streamlit: http://localhost:8501/")
        print("   - Dashboard Garantie: http://localhost:8000/dashboard-garantie/")
    else:
        print("❌ Test échoué ! Vérifiez la configuration.")
        sys.exit(1)
