#!/usr/bin/env python3
"""
Script pour générer automatiquement les diagrammes UML du projet ParcInfo
à partir des fichiers PlantUML (.puml)
"""

import os
import subprocess
import sys
from pathlib import Path

def check_plantuml():
    """Vérifie si PlantUML est installé et accessible"""
    try:
        result = subprocess.run(['plantuml', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ PlantUML est installé et accessible")
            return True
        else:
            print("❌ PlantUML n'est pas accessible")
            return False
    except FileNotFoundError:
        print("❌ PlantUML n'est pas installé")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de la vérification de PlantUML")
        return False

def install_plantuml():
    """Tente d'installer PlantUML via différents moyens"""
    print("🔧 Tentative d'installation de PlantUML...")
    
    # Vérifier si Java est installé
    try:
        subprocess.run(['java', '-version'], capture_output=True, check=True)
        print("✅ Java est installé")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Java n'est pas installé. Veuillez installer Java d'abord.")
        return False
    
    # Essayer d'installer via pip
    try:
        print("📦 Installation via pip...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'plantuml'], check=True)
        print("✅ PlantUML installé via pip")
        return True
    except subprocess.CalledProcessError:
        print("❌ Échec de l'installation via pip")
    
    # Essayer d'installer via conda
    try:
        print("📦 Installation via conda...")
        subprocess.run(['conda', 'install', '-c', 'conda-forge', 'plantuml'], check=True)
        print("✅ PlantUML installé via conda")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Échec de l'installation via conda")
    
    print("❌ Impossible d'installer PlantUML automatiquement")
    print("💡 Veuillez l'installer manuellement:")
    print("   - Via Homebrew: brew install plantuml")
    print("   - Via le site officiel: https://plantuml.com/download")
    return False

def generate_diagrams():
    """Génère tous les diagrammes UML à partir des fichiers .puml"""
    current_dir = Path(__file__).parent
    puml_files = list(current_dir.glob("*.puml"))
    
    if not puml_files:
        print("❌ Aucun fichier .puml trouvé dans le répertoire courant")
        return
    
    print(f"📁 {len(puml_files)} fichier(s) .puml trouvé(s)")
    
    # Créer le répertoire de sortie
    output_dir = current_dir / "diagrammes_generes"
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    
    for puml_file in puml_files:
        print(f"\n🔄 Génération du diagramme: {puml_file.name}")
        
        try:
            # Générer le diagramme
            cmd = [
                'plantuml', 
                '-tpng',  # Format PNG
                '-o', str(output_dir),  # Répertoire de sortie
                str(puml_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Diagramme généré: {puml_file.stem}.png")
                success_count += 1
            else:
                print(f"❌ Erreur lors de la génération: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout lors de la génération de {puml_file.name}")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
    
    print(f"\n🎉 Génération terminée: {success_count}/{len(puml_files)} diagramme(s) généré(s)")
    print(f"📁 Les diagrammes sont disponibles dans: {output_dir}")

def generate_svg_diagrams():
    """Génère également les diagrammes en format SVG"""
    current_dir = Path(__file__).parent
    puml_files = list(current_dir.glob("*.puml"))
    
    if not puml_files:
        return
    
    output_dir = current_dir / "diagrammes_generes"
    output_dir.mkdir(exist_ok=True)
    
    print("\n🔄 Génération des diagrammes SVG...")
    
    for puml_file in puml_files:
        try:
            cmd = [
                'plantuml', 
                '-tsvg',  # Format SVG
                '-o', str(output_dir),
                str(puml_file)
            ]
            
            subprocess.run(cmd, capture_output=True, timeout=60)
            print(f"✅ SVG généré: {puml_file.stem}.svg")
            
        except Exception as e:
            print(f"❌ Erreur SVG pour {puml_file.name}: {e}")

def main():
    """Fonction principale"""
    print("🚀 Générateur de diagrammes UML pour ParcInfo")
    print("=" * 50)
    
    # Vérifier PlantUML
    if not check_plantuml():
        print("\n🔧 Tentative d'installation automatique...")
        if not install_plantuml():
            print("\n❌ Impossible de continuer sans PlantUML")
            sys.exit(1)
    
    # Générer les diagrammes
    generate_diagrams()
    
    # Générer aussi en SVG
    generate_svg_diagrams()
    
    print("\n🎯 Résumé des diagrammes générés:")
    print("📊 diagramme_classe_parcinfo_complet.png/svg")
    print("📊 diagramme_classe_parcinfo_simplifie.png/svg")
    
    print("\n💡 Vous pouvez maintenant:")
    print("   - Ouvrir les fichiers PNG/SVG générés")
    print("   - Les intégrer dans votre documentation")
    print("   - Les utiliser pour la présentation du projet")

if __name__ == "__main__":
    main()
