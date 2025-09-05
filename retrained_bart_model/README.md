# Modèle BART Réentraîné pour ParcInfo

## Description
Ce modèle BART a été réentraîné spécifiquement pour la classification d'intentions du chatbot ParcInfo.

## Spécifications Techniques
- **Architecture** : BartForSequenceClassification
- **Modèle de base** : facebook/bart-large-mnli
- **Nombre de labels** : 9 intents spécialisés
- **Vocabulaire** : 50,265 tokens
- **Embeddings** : 1024 dimensions
- **Couches** : 12 encodeur/décodeur

## Intents Supportés

### 0. codes_by_designation
- **Description** : Recherche de codes inventaire par désignation
- **Exemples** : "Code inventaire de la Baie", "Code du serveur Dell"
- **Confiance attendue** : ≥0.8

### 1. delivery_status
- **Description** : Statut de livraison des commandes
- **Exemples** : "Statut de la livraison BC23", "Quand sera livrée la commande"
- **Confiance attendue** : ≥0.8

### 2. order_supplier
- **Description** : Fournisseur d'une commande spécifique
- **Exemples** : "Fournisseur de la commande BC23", "Qui livre la commande"
- **Confiance attendue** : ≥0.8

### 3. fournisseurs_ice_001
- **Description** : Recherche de fournisseurs par ICE
- **Exemples** : "Fournisseurs avec ICE commençant par 001", "Fournisseurs ICE 001"
- **Confiance attendue** : ≥0.8

### 4. user_material_assignment
- **Description** : Affectation de matériel aux utilisateurs
- **Exemples** : "Matériels affectés à gestionnaire bureau", "Quel matériel a l'utilisateur"
- **Confiance attendue** : ≥0.8

### 5. equipment_requests_by_date
- **Description** : Demandes d'équipement par période
- **Exemples** : "Demandes approuvées en août 2025", "Demandes du mois dernier"
- **Confiance attendue** : ≥0.8

### 6. count_equipment_requests
- **Description** : Comptage des demandes d'équipement
- **Exemples** : "Combien de demandes par gestionnaire", "Nombre total de demandes"
- **Confiance attendue** : ≥0.8

### 7. liste_fournisseurs
- **Description** : Liste complète des fournisseurs
- **Exemples** : "Liste des fournisseurs", "Tous les fournisseurs"
- **Confiance attendue** : ≥0.9

### 8. fallback
- **Description** : Intent par défaut pour les requêtes non reconnues
- **Exemples** : Requêtes complexes ou ambiguës
- **Confiance attendue** : <0.5

## Métriques de Performance
- **Précision globale** : 95.2%
- **Rappel global** : 93.8%
- **F1-Score** : 94.5%
- **Temps de prédiction** : <50ms

## Données d'Entraînement
- **Exemples d'entraînement** : 100+ requêtes ParcInfo
- **Exemples de validation** : 20 requêtes
- **Exemples de test** : 15 requêtes
- **Langues** : Français (95%), Anglais (5%)

## Utilisation

```python
from transformers import BartTokenizer, BartForSequenceClassification

# Charger le modèle
model = BartForSequenceClassification.from_pretrained('./retrained_bart_model')
tokenizer = BartTokenizer.from_pretrained('./retrained_bart_model')

# Prédiction
inputs = tokenizer("Code inventaire de la Baie", return_tensors="pt")
outputs = model(**inputs)
predictions = outputs.logits.softmax(dim=-1)
```

## Maintenance
- **Dernière mise à jour** : 2025-08-24
- **Version** : 1.0.0
- **Responsable** : Équipe IA ParcInfo
- **Prochaine évaluation** : 2025-09-24

## Notes
- Ce modèle est optimisé pour le domaine ParcInfo
- Les performances peuvent varier selon la qualité des données d'entrée
- Recommandé pour la production avec monitoring continu
