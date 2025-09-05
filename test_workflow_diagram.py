#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du Générateur de Diagrammes ParcInfo
=========================================

Script de test pour vérifier le bon fonctionnement du générateur de diagrammes.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test des imports nécessaires."""
    print("🔍 Test des imports...")
    
    try:
        from graphviz import Digraph
        print("✅ Import graphviz réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur import graphviz: {e}")
        return False

def test_graphviz_system():
    """Test de l'installation système de Graphviz."""
    print("🔍 Test de Graphviz système...")
    
    try:
        import subprocess
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Graphviz système disponible")
            return True
        else:
            print("⚠️  Graphviz système non disponible")
            return False
    except FileNotFoundError:
        print("⚠️  Graphviz système non installé")
        return False

def test_directory_structure():
    """Test de la structure des répertoires."""
    print("🔍 Test de la structure des répertoires...")
    
    required_files = [
        'generate_workflow_diagram.py',
        'requirements_graphviz.txt',
        'launch_workflow_diagram.sh'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False
    else:
        print("✅ Tous les fichiers requis présents")
        return True

def test_generation():
    """Test de la génération de diagrammes."""
    print("🔍 Test de génération de diagrammes...")
    
    try:
        # Importer et tester la génération
        from generate_workflow_diagram import create_workflow_diagram, create_roles_diagram
        
        # Créer les diagrammes
        workflow_dot = create_workflow_diagram()
        roles_dot = create_roles_diagram()
        
        print("✅ Création des diagrammes réussie")
        
        # Vérifier les propriétés des diagrammes
        if workflow_dot.name == 'Workflow_ParcInfo_Complet':
            print("✅ Nom du workflow correct")
        else:
            print("❌ Nom du workflow incorrect")
            return False
            
        if roles_dot.name == 'Roles_ParcInfo':
            print("✅ Nom des rôles correct")
        else:
            print("❌ Nom des rôles incorrect")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return False

def test_output_directory():
    """Test du répertoire de sortie."""
    print("🔍 Test du répertoire de sortie...")
    
    output_dir = 'diagrammes_generes'
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        print("✅ Répertoire de sortie disponible")
        return True
    else:
        print("❌ Impossible de créer le répertoire de sortie")
        return False

def main():
    """Fonction principale de test."""
    print("🧪 Test du Générateur de Diagrammes ParcInfo")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Graphviz système", test_graphviz_system),
        ("Structure répertoires", test_directory_structure),
        ("Répertoire de sortie", test_output_directory),
        ("Génération diagrammes", test_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! Le générateur est prêt.")
        return True
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les prérequis.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
