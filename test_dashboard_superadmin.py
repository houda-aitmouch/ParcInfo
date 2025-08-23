#!/usr/bin/env python3
"""
Script de test pour vérifier que le dashboard superadmin fonctionne correctement
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.users.views import superadmin_dashboard
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from apps.users.models import CustomUser

def test_superadmin_dashboard():
    """Test du dashboard superadmin"""
    print("=== Test du Dashboard Super Admin ===\n")
    
    # Créer une requête factice
    factory = RequestFactory()
    
    # Créer un utilisateur superadmin pour le test
    User = get_user_model()
    try:
        superadmin = User.objects.get(username='superadmin')
    except User.DoesNotExist:
        print("❌ Utilisateur superadmin non trouvé")
        return
    
    # Créer une requête avec l'utilisateur connecté
    request = factory.get('/')
    request.user = superadmin
    
    try:
        # Appeler la vue
        response = superadmin_dashboard(request)
        
        if response.status_code == 200:
            print("✅ Dashboard superadmin accessible")
            
            # Vérifier le contexte
            context = response.context_data if hasattr(response, 'context_data') else {}
            
            print("\n📊 Statistiques du dashboard:")
            print(f"• Total matériels: {context.get('total_materials', 'N/A')}")
            print(f"• Total utilisateurs: {context.get('total_users', 'N/A')}")
            print(f"• Garanties actives: {context.get('active_warranties', 'N/A')}")
            print(f"• Demandes en attente: {context.get('pending_requests', 'N/A')}")
            print(f"• Notifications garantie: {context.get('alerts_garantie_count', 'N/A')}")
            
            # Vérifier les données des graphiques
            commandes_par_mois = context.get('commandes_par_mois', [])
            print(f"\n📈 Données graphiques:")
            print(f"• Commandes par mois: {len(commandes_par_mois)} mois de données")
            
            activite_recente = context.get('activite_recente', [])
            print(f"• Activité récente: {len(activite_recente)} activités")
            
            print("\n✅ Dashboard superadmin fonctionne correctement !")
            
        else:
            print(f"❌ Erreur: Status code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_superadmin_dashboard()
