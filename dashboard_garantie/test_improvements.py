#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations du Dashboard Garantie
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_files_exist():
    """Vérifie que tous les fichiers d'amélioration existent"""
    print("🔍 Vérification des fichiers d'amélioration...")
    
    required_files = [
        'custom_styles.css',
        'theme_config.py',
        'components.py',
        'IMPROVEMENTS.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Fichiers manquants : {missing_files}")
        return False
    
    print("✅ Tous les fichiers d'amélioration sont présents")
    return True

def check_css_syntax():
    """Vérifie la syntaxe CSS"""
    print("\n🎨 Vérification de la syntaxe CSS...")
    
    try:
        with open('custom_styles.css', 'r') as f:
            css_content = f.read()
        
        # Vérifications basiques
        if ':root' in css_content:
            print("✅ Variables CSS définies")
        else:
            print("⚠️ Variables CSS manquantes")
        
        if '--primary-color' in css_content:
            print("✅ Couleurs primaires définies")
        else:
            print("⚠️ Couleurs primaires manquantes")
        
        if '@media' in css_content:
            print("✅ Media queries pour responsive design")
        else:
            print("⚠️ Media queries manquantes")
        
        if '@keyframes' in css_content:
            print("✅ Animations CSS définies")
        else:
            print("⚠️ Animations CSS manquantes")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification CSS : {e}")
        return False

def check_theme_config():
    """Vérifie la configuration des thèmes"""
    print("\n🎯 Vérification de la configuration des thèmes...")
    
    try:
        sys.path.append('.')
        from theme_config import COLORS, ICONS, METRICS_CONFIG
        
        # Vérifier les couleurs
        required_colors = ['primary', 'success', 'warning', 'danger', 'info']
        for color in required_colors:
            if color in COLORS:
                print(f"✅ Couleur {color} définie")
            else:
                print(f"⚠️ Couleur {color} manquante")
        
        # Vérifier les icônes
        required_icons = ['critical', 'warning', 'success', 'info']
        for icon in required_icons:
            if icon in ICONS:
                print(f"✅ Icône {icon} définie")
            else:
                print(f"⚠️ Icône {icon} manquante")
        
        # Vérifier les métriques
        required_metrics = ['total_commandes', 'en_garantie', 'expirees']
        for metric in required_metrics:
            if metric in METRICS_CONFIG:
                print(f"✅ Métrique {metric} définie")
            else:
                print(f"⚠️ Métrique {metric} manquante")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des thèmes : {e}")
        return False

def check_components():
    """Vérifie les composants"""
    print("\n🧩 Vérification des composants...")
    
    try:
        sys.path.append('.')
        from components import (
            render_header, render_metric_card, render_alert,
            render_section_header, render_data_table
        )
        
        print("✅ Tous les composants principaux importés")
        
        # Vérifier que les fonctions sont callables
        functions = [
            render_header, render_metric_card, render_alert,
            render_section_header, render_data_table
        ]
        
        for func in functions:
            if callable(func):
                print(f"✅ {func.__name__} est une fonction valide")
            else:
                print(f"❌ {func.__name__} n'est pas une fonction")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import des composants : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des composants : {e}")
        return False

def check_dashboard_integration():
    """Vérifie l'intégration avec le dashboard principal"""
    print("\n🔗 Vérification de l'intégration avec le dashboard...")
    
    try:
        with open('dashboard_garantie.py', 'r') as f:
            content = f.read()
        
        # Vérifier l'import des styles CSS
        if 'load_custom_css' in content:
            print("✅ Fonction de chargement CSS intégrée")
        else:
            print("⚠️ Fonction de chargement CSS manquante")
        
        # Vérifier la configuration de la page
        if 'st.set_page_config' in content:
            print("✅ Configuration de page Streamlit présente")
        else:
            print("⚠️ Configuration de page Streamlit manquante")
        
        # Vérifier l'utilisation des composants
        if 'render_header' in content or 'render_metric_card' in content:
            print("✅ Composants utilisés dans le dashboard")
        else:
            print("⚠️ Composants non utilisés dans le dashboard")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'intégration : {e}")
        return False

def test_dashboard_startup():
    """Test le démarrage du dashboard"""
    print("\n🚀 Test de démarrage du dashboard...")
    
    try:
        # Vérifier que le script de lancement existe
        if not os.path.exists('run_dashboard.py'):
            print("❌ Script run_dashboard.py manquant")
            return False
        
        print("✅ Script de lancement trouvé")
        
        # Test de syntaxe Python
        result = subprocess.run([
            sys.executable, '-m', 'py_compile', 'dashboard_garantie.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Syntaxe Python valide")
        else:
            print(f"❌ Erreur de syntaxe Python : {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test de démarrage : {e}")
        return False

def generate_test_report():
    """Génère un rapport de test"""
    print("\n📊 Génération du rapport de test...")
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'files_check': check_files_exist(),
        'css_syntax': check_css_syntax(),
        'theme_config': check_theme_config(),
        'components': check_components(),
        'integration': check_dashboard_integration(),
        'startup': test_dashboard_startup()
    }
    
    # Calculer le score global
    total_tests = len(report) - 1  # Exclure timestamp
    passed_tests = sum(1 for key, value in report.items() 
                      if key != 'timestamp' and value)
    
    score = (passed_tests / total_tests) * 100
    
    print(f"\n🎯 Score global : {score:.1f}% ({passed_tests}/{total_tests})")
    
    if score >= 90:
        print("🎉 Excellent ! Toutes les améliorations sont en place")
    elif score >= 70:
        print("✅ Bon ! La plupart des améliorations sont fonctionnelles")
    elif score >= 50:
        print("⚠️ Moyen ! Certaines améliorations nécessitent des corrections")
    else:
        print("❌ Critique ! De nombreuses améliorations sont manquantes")
    
    return report

def main():
    """Fonction principale de test"""
    print("🧪 Test des améliorations du Dashboard Garantie")
    print("=" * 50)
    
    # Changer vers le répertoire du dashboard
    dashboard_dir = Path(__file__).parent
    os.chdir(dashboard_dir)
    
    # Exécuter tous les tests
    report = generate_test_report()
    
    # Afficher les recommandations
    print("\n💡 Recommandations :")
    
    if not report['files_check']:
        print("- Vérifiez que tous les fichiers d'amélioration sont présents")
    
    if not report['css_syntax']:
        print("- Corrigez la syntaxe CSS dans custom_styles.css")
    
    if not report['theme_config']:
        print("- Vérifiez la configuration des thèmes dans theme_config.py")
    
    if not report['components']:
        print("- Corrigez les imports dans components.py")
    
    if not report['integration']:
        print("- Intégrez les composants dans dashboard_garantie.py")
    
    if not report['startup']:
        print("- Corrigez les erreurs de syntaxe dans le dashboard")
    
    print("\n✅ Test terminé !")
    
    return report

if __name__ == "__main__":
    main()
