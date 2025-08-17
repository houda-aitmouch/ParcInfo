# 🤖 Guide du Chatbot IA ParcInfo

## 🎯 **Vue d'ensemble**

Le chatbot ParcInfo est maintenant un **vrai assistant IA** qui :
- ✅ **Recherche directement dans la base de données PostgreSQL**
- ✅ **Comprend le langage naturel (NLP)**
- ✅ **Utilise LLaMA 3 quand disponible**
- ✅ **Mode fallback intelligent sans LLaMA 3**
- ✅ **Réponses contextuelles et précises**

## 🚀 **Fonctionnalités Principales**

### **1. Recherche Intelligente en Base de Données**
- **Matériel informatique** : Codes d'inventaire, numéros de série, statuts
- **Matériel bureautique** : Codes d'inventaire, lieux de stockage
- **Demandes d'équipement** : Statuts, catégories, types
- **Fournisseurs** : Informations de contact, spécialités
- **Livraisons** : Statuts, dates, lieux
- **Statistiques système** : Métriques en temps réel

### **2. Compréhension du Langage Naturel**
- Questions en français naturel
- Reconnaissance de mots-clés
- Adaptation au contexte
- Réponses personnalisées selon le rôle

### **3. Technologies IA**
- **LLaMA 3** : Modèle de langage avancé (optionnel)
- **LangChain** : Framework d'IA conversationnelle
- **PostgreSQL** : Base de données relationnelle
- **Mode Fallback** : Fonctionne même sans LLaMA 3

## 📋 **Exemples de Questions**

### **Codes d'Inventaire**
```
"Quel est le code inventaire de matériel baie ?"
"Code inventaire matériel"
"Montre-moi les codes d'inventaire"
"Codes inventaire informatique"
```

### **Matériel**
```
"Montre-moi le matériel informatique"
"Matériel bureautique disponible"
"Statut du matériel"
"Lieu de stockage du matériel"
```

### **Demandes**
```
"Demandes d'équipement en attente"
"Statut de mes demandes"
"Demandes approuvées"
"Historique des demandes"
```

### **Statistiques**
```
"Statistiques du système"
"Combien de matériel informatique ?"
"Nombre de demandes"
"Répartition par statut"
```

## 🔧 **Configuration**

### **1. Variables d'Environnement**
```bash
# .env
LLAMA_MODEL_PATH=models/llama-3-8b-instruct.gguf
DEBUG=True
SECRET_KEY=your-secret-key
```

### **2. Installation LLaMA 3 (Optionnel)**
```bash
# Créer le dossier models
mkdir models

# Télécharger LLaMA 3 depuis HuggingFace
# https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF

# Placer le fichier .gguf dans models/
# Le chatbot utilisera automatiquement LLaMA 3
```

### **3. Base de Données**
Le chatbot se connecte automatiquement à PostgreSQL et recherche dans :
- `materiel_informatique_materielinformatique`
- `materiel_bureautique_materielbureau`
- `demande_equipement_demandeequipement`
- `fournisseurs_fournisseur`
- `livraison_livraison`

## 🎮 **Utilisation**

### **1. Accès Web**
- **URL** : `http://localhost:8000/chatbot/`
- **Permissions** : Tous les utilisateurs connectés
- **Interface** : Chat en temps réel

### **2. Navigation**
- **Chat** : Interface principale
- **Historique** : Conversations précédentes
- **Aide** : Guide d'utilisation
- **Insights** : Métriques d'apprentissage

### **3. Exemples d'Interaction**

#### **Question** : "Quel est le code inventaire de matériel baie ?"

#### **Réponse** :
```
Voici les informations trouvées dans la base de données :

🏷️ **Codes d'Inventaire :**
• INFORMATIQUE: **ADD/INFO/010** - N° Série: 123456 (nouveau)
• INFORMATIQUE: **ADD/INFO/01000** - N° Série: 12345 (nouveau)
• BUREAUTIQUE: **ADD/INFO/01094** - N° Série: N/A (Opérationnel)

📊 **Statistiques Système :**
• Matériel informatique: 5
• Matériel bureautique: 1
• Demandes d'équipement: 10
• Fournisseurs: 44
```

## 🔍 **Recherche Intelligente**

### **Mots-clés Reconus**

#### **Matériel Informatique**
- `informatique`, `ordinateur`, `pc`, `laptop`, `serveur`, `baie`

#### **Matériel Bureautique**
- `bureau`, `bureautique`, `imprimante`, `scanner`, `chaise`, `table`

#### **Demandes**
- `demande`, `demandes`, `équipement`, `matériel`

#### **Codes d'Inventaire**
- `code`, `inventaire`, `matériel`

#### **Fournisseurs**
- `fournisseur`, `fournisseurs`, `commande`, `achat`

#### **Livraisons**
- `livraison`, `livrer`, `réception`, `livré`

## 🛠️ **Dépannage**

### **Problèmes Courants**

#### **1. "Système IA temporairement indisponible"**
- **Cause** : LLaMA 3 non configuré
- **Solution** : Le mode fallback fonctionne automatiquement

#### **2. "Erreur base de données"**
- **Cause** : Problème de connexion PostgreSQL
- **Solution** : Vérifier la configuration DB dans `.env`

#### **3. "Aucune donnée trouvée"**
- **Cause** : Base de données vide ou question trop spécifique
- **Solution** : Reformuler la question ou ajouter des données

### **Logs et Debug**
```bash
# Voir les logs du chatbot
tail -f logs/parcinfo.log

# Test en ligne de commande
python manage.py shell -c "from apps.chatbot.llm_engine import ParcInfoChatbot; c = ParcInfoChatbot(); print(c.get_response('test', None))"
```

## 📊 **Métriques et Insights**

### **Données Collectées**
- Nombre d'interactions
- Types de questions
- Réponses générées
- Temps de réponse
- Statut LLaMA 3

### **Accès aux Insights**
- **URL** : `/chatbot/insights/`
- **Métriques** : Temps réel
- **Historique** : Évolutions

## 🔒 **Sécurité**

### **Permissions**
- **Accès** : Utilisateurs connectés uniquement
- **Données** : Respect des rôles utilisateur
- **Logs** : Pas de données sensibles

### **Base de Données**
- **Connexion sécurisée** : Paramètres dans `.env`
- **Requêtes optimisées** : LIMIT et index
- **Gestion d'erreurs** : Fallback en cas de problème

## 🚀 **Améliorations Futures**

### **Fonctionnalités Prévues**
- [ ] Intégration d'autres modèles IA
- [ ] Analyse de sentiment
- [ ] Suggestions automatiques
- [ ] Export de rapports
- [ ] Notifications intelligentes

### **Optimisations**
- [ ] Cache des requêtes fréquentes
- [ ] Index de recherche avancés
- [ ] API REST pour intégrations
- [ ] Interface mobile

## 📞 **Support**

### **En Cas de Problème**
1. Vérifier les logs : `logs/parcinfo.log`
2. Tester la connexion DB
3. Vérifier la configuration LLaMA 3
4. Consulter ce guide

### **Contact**
- **Email** : support@votre-entreprise.com
- **Documentation** : `/docs/`
- **Issues** : Système de tickets

---

**Version** : 2.0.0  
**Dernière mise à jour** : 31/07/2025  
**Statut** : ✅ Fonctionnel et opérationnel

**Le chatbot ParcInfo est maintenant un vrai assistant IA ! 🤖✨** 