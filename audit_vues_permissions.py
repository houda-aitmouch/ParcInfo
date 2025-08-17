#!/usr/bin/env python
"""
Script d'audit des vues et permissions du projet ParcInfo
Vérifie que toutes les vues sont protégées par les bonnes permissions
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from django.urls import get_resolver
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.functional import cached_property
import inspect

def audit_vues_permissions():
    """Audit complet des vues et leurs permissions"""
    
    print("🔍 AUDIT COMPLET DES VUES ET PERMISSIONS PARCINFO")
    print("=" * 70)
    
    # 1. Récupérer toutes les URLs du projet
    resolver = get_resolver()
    urls_patterns = []
    
    def collect_urls(patterns, base=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                collect_urls(pattern.url_patterns, base + str(pattern.pattern))
            else:
                urls_patterns.append({
                    'pattern': base + str(pattern.pattern),
                    'callback': pattern.callback,
                    'name': pattern.name
                })
    
    collect_urls(resolver.url_patterns)
    
    print(f"📊 Total des URLs trouvées: {len(urls_patterns)}")
    
    # 2. Analyser chaque vue
    print("\n📱 ANALYSE DES VUES PAR APPLICATION:")
    print("-" * 50)
    
    vues_par_app = {}
    vues_protegees = 0
    vues_non_protegees = []
    
    for url_info in urls_patterns:
        if url_info['callback']:
            callback = url_info['callback']
            
            # Déterminer l'application
            app_name = 'unknown'
            if hasattr(callback, '__module__'):
                module_parts = callback.__module__.split('.')
                if len(module_parts) >= 2:
                    app_name = module_parts[1]
            
            if app_name not in vues_par_app:
                vues_par_app[app_name] = []
            
            # Analyser la protection de la vue
            protection_info = analyser_protection_vue(callback)
            
            vue_info = {
                'url': url_info['pattern'],
                'name': url_info['name'] or 'Sans nom',
                'callback': callback.__name__,
                'protection': protection_info
            }
            
            vues_par_app[app_name].append(vue_info)
            
            if protection_info['protegee']:
                vues_protegees += 1
            else:
                vues_non_protegees.append(vue_info)
    
    # 3. Afficher les résultats par application
    for app_name, vues in sorted(vues_par_app.items()):
        if app_name in ['unknown', 'admin', 'auth']:
            continue
            
        print(f"\n🔧 {app_name.upper()}: {len(vues)} vues")
        print("-" * 30)
        
        for vue in vues:
            status = "✅" if vue['protection']['protegee'] else "⚠️"
            print(f"  {status} {vue['name']} ({vue['callback']})")
            print(f"     URL: {vue['url']}")
            print(f"     Protection: {vue['protection']['type']}")
            if vue['protection']['permissions']:
                print(f"     Permissions: {', '.join(vue['protection']['permissions'])}")
            print()
    
    # 4. Vérifier les vues non protégées
    print("\n⚠️  VUES POTENTIELLEMENT NON PROTÉGÉES:")
    print("-" * 50)
    
    if vues_non_protegees:
        for vue in vues_non_protegees:
            print(f"❌ {vue['name']} ({vue['callback']})")
            print(f"   URL: {vue['url']}")
            print(f"   Application: {vue['callback'].__module__}")
            print()
    else:
        print("✅ Toutes les vues sont protégées !")
    
    # 5. Statistiques de sécurité
    print("\n📈 STATISTIQUES DE SÉCURITÉ:")
    print("-" * 50)
    
    total_vues = len(urls_patterns)
    taux_protection = (vues_protegees / total_vues * 100) if total_vues > 0 else 0
    
    print(f"📊 Total des vues: {total_vues}")
    print(f"✅ Vues protégées: {vues_protegees}")
    print(f"⚠️  Vues non protégées: {len(vues_non_protegees)}")
    print(f"🛡️  Taux de protection: {taux_protection:.1f}%")
    
    # 6. Recommandations
    print("\n💡 RECOMMANDATIONS:")
    print("-" * 50)
    
    if taux_protection >= 95:
        print("✅ Sécurité excellente !")
        print("✅ Toutes les vues critiques sont protégées")
        print("✅ Système de permissions robuste")
    elif taux_protection >= 80:
        print("✅ Sécurité bonne")
        print("⚠️  Quelques vues à vérifier")
    else:
        print("⚠️  Sécurité insuffisante")
        print("❌ Nombreuses vues non protégées")
        print("🔒 Ajouter des décorateurs de sécurité")
    
    print("\n✅ AUDIT TERMINÉ!")
    print("=" * 70)

def analyser_protection_vue(callback):
    """Analyse la protection d'une vue"""
    
    protection_info = {
        'protegee': False,
        'type': 'Aucune protection',
        'permissions': []
    }
    
    try:
        # Vérifier les décorateurs
        if hasattr(callback, '__wrapped__'):
            wrapped = callback.__wrapped__
            
            # Vérifier login_required
            if hasattr(wrapped, '__name__') and wrapped.__name__ == 'login_required':
                protection_info['protegee'] = True
                protection_info['type'] = 'Login requis'
            
            # Vérifier permission_required
            elif hasattr(wrapped, '__name__') and wrapped.__name__ == 'permission_required':
                protection_info['protegee'] = True
                protection_info['type'] = 'Permission requise'
                
                # Essayer de récupérer les permissions
                if hasattr(wrapped, 'permission_required'):
                    protection_info['permissions'] = wrapped.permission_required
                elif hasattr(wrapped, 'login_url'):
                    protection_info['permissions'] = ['Permission spécifique']
        
        # Vérifier les mixins (pour les vues basées sur les classes)
        elif hasattr(callback, 'view_class'):
            view_class = callback.view_class
            
            if hasattr(view_class, '__bases__'):
                for base in view_class.__bases__:
                    if 'LoginRequiredMixin' in str(base):
                        protection_info['protegee'] = True
                        protection_info['type'] = 'LoginRequiredMixin'
                    elif 'PermissionRequiredMixin' in str(base):
                        protection_info['protegee'] = True
                        protection_info['type'] = 'PermissionRequiredMixin'
                        
                        # Récupérer les permissions requises
                        if hasattr(view_class, 'permission_required'):
                            perms = view_class.permission_required
                            if isinstance(perms, (list, tuple)):
                                protection_info['permissions'] = perms
                            else:
                                protection_info['permissions'] = [perms]
        
        # Vérifier les vues d'authentification (login, logout, etc.)
        elif 'auth' in callback.__module__ or 'login' in callback.__name__.lower():
            protection_info['protegee'] = True
            protection_info['type'] = 'Vue d\'authentification'
        
        # Vérifier les vues d'admin
        elif 'admin' in callback.__module__:
            protection_info['protegee'] = True
            protection_info['type'] = 'Vue d\'administration'
            
    except Exception as e:
        protection_info['type'] = f'Erreur d\'analyse: {e}'
    
    return protection_info

if __name__ == "__main__":
    audit_vues_permissions()
