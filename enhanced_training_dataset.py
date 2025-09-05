#!/usr/bin/env python3
"""
Dataset étendu d'entraînement pour le modèle BART ParcInfo
100+ exemples pour améliorer la détection d'intentions
"""

import json
from datetime import datetime

def create_enhanced_training_dataset():
    """Crée un dataset étendu d'entraînement"""
    
    training_data = {
        "metadata": {
            "version": "2.0.0",
            "created_at": datetime.now().isoformat(),
            "total_examples": 0,
            "intents": {},
            "description": "Dataset étendu pour le modèle BART ParcInfo avec 100+ exemples"
        },
        "training_examples": [],
        "validation_examples": [],
        "test_examples": []
    }
    
    # 1. INTENT: codes_by_designation (20 exemples)
    codes_examples = [
        {"text": "Code inventaire de la Baie", "intent": "codes_by_designation", "confidence": 0.95},
        {"text": "Code du serveur Dell", "intent": "codes_by_designation", "confidence": 0.95},
        {"text": "Code inventaire PC001", "intent": "codes_by_designation", "confidence": 0.95},
        {"text": "Quel est le code de l'ordinateur portable", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code de l'imprimante HP", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Numéro d'inventaire du switch Cisco", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code du vidéoprojecteur", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Référence inventaire du scanner", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code du télécopieur Brother", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Numéro d'inventaire du serveur", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code de l'écran supplémentaire", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Référence du clavier ergonomique", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code de la webcam HD", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Numéro d'inventaire de l'imprimante couleur", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code du matériel bureautique", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Référence inventaire du matériel informatique", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code de l'équipement de bureau", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Numéro d'inventaire de l'équipement", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Code du matériel de l'utilisateur", "intent": "codes_by_designation", "confidence": 0.90},
        {"text": "Référence de l'équipement affecté", "intent": "codes_by_designation", "confidence": 0.90}
    ]
    
    # 2. INTENT: delivery_status (20 exemples)
    delivery_examples = [
        {"text": "Statut de la livraison BC23", "intent": "delivery_status", "confidence": 0.95},
        {"text": "Quand sera livrée la commande BC24", "intent": "delivery_status", "confidence": 0.95},
        {"text": "État de la livraison de la commande", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Livraison en retard ou à l'heure", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Date de livraison effective", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Statut du transport de la commande", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Suivi de livraison de la commande", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Livraison prévue vs effective", "intent": "delivery_status", "confidence": 0.90},
        {"text": "État du transport de l'équipement", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Statut de la livraison du matériel", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Quand arrivera la commande", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Livraison en cours ou terminée", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Statut de la commande en transit", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Livraison par quel transporteur", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Numéro de suivi de la livraison", "intent": "delivery_status", "confidence": 0.90},
        {"text": "État de la livraison urgente", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Livraison prévue pour quand", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Statut de la livraison express", "intent": "delivery_status", "confidence": 0.90},
        {"text": "Livraison en attente ou confirmée", "intent": "delivery_status", "confidence": 0.90},
        {"text": "État de la livraison du fournisseur", "intent": "delivery_status", "confidence": 0.90}
    ]
    
    # 3. INTENT: order_supplier (15 exemples)
    supplier_examples = [
        {"text": "Fournisseur de la commande BC23", "intent": "order_supplier", "confidence": 0.95},
        {"text": "Qui livre la commande BC24", "intent": "order_supplier", "confidence": 0.95},
        {"text": "Fournisseur de la commande en cours", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Quel fournisseur pour cette commande", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Fournisseur de la commande urgente", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Qui fournit la commande", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Fournisseur de la commande informatique", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Quel fournisseur livre la commande", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Fournisseur de la commande bureautique", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Qui est le fournisseur de la commande", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Fournisseur de la commande en attente", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Quel fournisseur pour l'équipement", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Fournisseur de la commande du mois", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Qui fournit le matériel commandé", "intent": "order_supplier", "confidence": 0.90},
        {"text": "Fournisseur de la commande récente", "intent": "order_supplier", "confidence": 0.90}
    ]
    
    # 4. INTENT: fournisseurs_ice_001 (15 exemples)
    ice_examples = [
        {"text": "Fournisseurs avec ICE commençant par 001", "intent": "fournisseurs_ice_001", "confidence": 0.95},
        {"text": "Fournisseurs ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.95},
        {"text": "Fournisseurs avec numéro ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Quels fournisseurs ont ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs ICE commençant par 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Liste des fournisseurs ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs avec ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Quels fournisseurs ont ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs ICE 001 disponibles", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs avec numéro ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Quels fournisseurs ont ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs ICE 001 actifs", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs avec ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Quels fournisseurs ont ICE 001", "intent": "fournisseurs_ice_001", "confidence": 0.90},
        {"text": "Fournisseurs ICE 001 enregistrés", "intent": "fournisseurs_ice_001", "confidence": 0.90}
    ]
    
    # 5. INTENT: user_material_assignment (15 exemples)
    assignment_examples = [
        {"text": "Matériels bureautiques affectés à gestionnaire bureau", "intent": "user_material_assignment", "confidence": 0.95},
        {"text": "Quel matériel a l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Matériels affectés à l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Quel équipement a l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Matériels de l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Affectation de matériel à l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Quel matériel est affecté à l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Matériels de l'utilisateur actif", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Quel équipement est affecté à l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Matériels de l'utilisateur enregistré", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Affectation de matériel à l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Quel matériel a l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Matériels de l'utilisateur connecté", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Quel équipement a l'utilisateur", "intent": "user_material_assignment", "confidence": 0.90},
        {"text": "Matériels de l'utilisateur actif", "intent": "user_material_assignment", "confidence": 0.90}
    ]
    
    # 6. INTENT: equipment_requests_by_date (15 exemples)
    date_examples = [
        {"text": "Demandes d'équipement approuvées en août 2025", "intent": "equipment_requests_by_date", "confidence": 0.95},
        {"text": "Demandes du mois dernier", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de cette semaine", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes du mois en cours", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de la période", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes par date", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de la semaine dernière", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes du trimestre", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de l'année", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes par période", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de la date", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes du jour", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de la période", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes par date", "intent": "equipment_requests_by_date", "confidence": 0.90},
        {"text": "Demandes de la période", "intent": "equipment_requests_by_date", "confidence": 0.90}
    ]
    
    # 7. INTENT: count_equipment_requests (15 exemples)
    count_examples = [
        {"text": "Combien de demandes d'équipement ont été faites par gestionnaire bureau", "intent": "count_equipment_requests", "confidence": 0.95},
        {"text": "Nombre total de demandes", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Nombre de demandes par utilisateur", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes approuvées", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Nombre de demandes en attente", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes rejetées", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Nombre de demandes par statut", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes par priorité", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Nombre de demandes par département", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes par type", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Nombre de demandes par fournisseur", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes par date", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Nombre de demandes par mois", "intent": "count_equipment_requests", "confidence": 0.90},
        {"text": "Comptage des demandes par année", "intent": "count_equipment_requests", "confidence": 0.90}
    ]
    
    # 8. INTENT: liste_fournisseurs (10 exemples)
    liste_examples = [
        {"text": "Liste des fournisseurs", "intent": "liste_fournisseurs", "confidence": 0.95},
        {"text": "Tous les fournisseurs", "intent": "liste_fournisseurs", "confidence": 0.95},
        {"text": "Fournisseurs disponibles", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Liste complète des fournisseurs", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Tous les fournisseurs actifs", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Fournisseurs enregistrés", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Liste des fournisseurs actifs", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Fournisseurs du système", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Tous les fournisseurs disponibles", "intent": "liste_fournisseurs", "confidence": 0.90},
        {"text": "Fournisseurs de la base", "intent": "liste_fournisseurs", "confidence": 0.90}
    ]
    
    # 9. INTENT: fallback (10 exemples)
    fallback_examples = [
        {"text": "Quels sont les prix des matériels informatiques", "intent": "fallback", "confidence": 0.30},
        {"text": "Historique des logs admin", "intent": "fallback", "confidence": 0.25},
        {"text": "Configuration du serveur", "intent": "fallback", "confidence": 0.20},
        {"text": "Maintenance préventive", "intent": "fallback", "confidence": 0.20},
        {"text": "Sauvegarde des données", "intent": "fallback", "confidence": 0.20},
        {"text": "Mise à jour du système", "intent": "fallback", "confidence": 0.20},
        {"text": "Sécurité informatique", "intent": "fallback", "confidence": 0.20},
        {"text": "Gestion des licences", "intent": "fallback", "confidence": 0.20},
        {"text": "Plan de reprise d'activité", "intent": "fallback", "confidence": 0.20},
        {"text": "Audit informatique", "intent": "fallback", "confidence": 0.20}
    ]
    
    # Assemblage du dataset complet
    all_examples = (
        codes_examples + delivery_examples + supplier_examples + 
        ice_examples + assignment_examples + date_examples + 
        count_examples + liste_examples + fallback_examples
    )
    
    # Répartition train/validation/test (80/10/10)
    total_examples = len(all_examples)
    train_size = int(total_examples * 0.8)
    val_size = int(total_examples * 0.1)
    
    training_data["training_examples"] = all_examples[:train_size]
    training_data["validation_examples"] = all_examples[train_size:train_size + val_size]
    training_data["test_examples"] = all_examples[train_size + val_size:]
    
    # Mise à jour des métadonnées
    training_data["metadata"]["total_examples"] = total_examples
    training_data["metadata"]["intents"] = {
        "codes_by_designation": len(codes_examples),
        "delivery_status": len(delivery_examples),
        "order_supplier": len(supplier_examples),
        "fournisseurs_ice_001": len(ice_examples),
        "user_material_assignment": len(assignment_examples),
        "equipment_requests_by_date": len(date_examples),
        "count_equipment_requests": len(count_examples),
        "liste_fournisseurs": len(liste_examples),
        "fallback": len(fallback_examples)
    }
    
    return training_data

def save_dataset(dataset, filename="enhanced_training_dataset.json"):
    """Sauvegarde le dataset au format JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dataset sauvegardé dans {filename}")
    print(f"📊 Total: {dataset['metadata']['total_examples']} exemples")
    print(f"🚀 Entraînement: {len(dataset['training_examples'])} exemples")
    print(f"🔍 Validation: {len(dataset['validation_examples'])} exemples")
    print(f"🧪 Test: {len(dataset['test_examples'])} exemples")

def main():
    """Fonction principale"""
    print("🚀 CRÉATION DU DATASET ÉTENDU D'ENTRAÎNEMENT")
    print("=" * 60)
    
    # Créer le dataset
    dataset = create_enhanced_training_dataset()
    
    # Sauvegarder le dataset
    save_dataset(dataset)
    
    # Afficher les statistiques par intent
    print("\n📋 Répartition par intent:")
    for intent, count in dataset["metadata"]["intents"].items():
        print(f"  - {intent}: {count} exemples")
    
    print("\n🎯 Objectif: Améliorer la détection d'intentions pour atteindre ≥60% de succès")
    print("✅ Dataset prêt pour l'entraînement du modèle BART")

if __name__ == "__main__":
    main()
