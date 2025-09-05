#!/usr/bin/env python3
"""
Module de réentraînement du modèle BART pour ParcInfo
Améliore la détection d'intention avec des exemples spécifiques au domaine
"""

import os
import json
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import torch
from transformers import (
    BartForSequenceClassification, 
    BartTokenizer, 
    TrainingArguments, 
    Trainer,
    DataCollatorWithPadding
)
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

logger = logging.getLogger(__name__)

class ParcInfoBartRetrainer:
    """Classe pour réentraîner le modèle BART sur le domaine ParcInfo"""
    
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.label2id = {}
        self.id2label = {}
        
        # Corpus d'entraînement spécifique à ParcInfo
        self.parcinfo_training_data = [
            # Codes et inventaire
            ("Code inventaire de la Baie", "codes_by_designation"),
            ("Numéro d'inventaire du serveur", "codes_by_designation"),
            ("Code de la station de travail", "codes_by_designation"),
            ("Référence du matériel informatique", "codes_by_designation"),
            ("Code inventaire du PC", "codes_by_designation"),
            
            # Statut de livraison
            ("Statut de la livraison BC23", "delivery_status"),
            ("État de la livraison BC24", "delivery_status"),
            ("Livraison BC23 est-elle arrivée", "delivery_status"),
            ("Quand arrive la livraison BC24", "delivery_status"),
            ("Statut livraison commande", "delivery_status"),
            
            # Fournisseurs de commandes
            ("Fournisseur de la commande BC23", "order_supplier"),
            ("Qui fournit la commande BC24", "order_supplier"),
            ("Fournisseur commande informatique", "order_supplier"),
            ("Fournisseur de la commande", "order_supplier"),
            ("Quel fournisseur pour BC23", "order_supplier"),
            
            # Fournisseurs ICE
            ("Fournisseurs avec ICE commençant par 001", "fournisseurs_ice_001"),
            ("ICE commençant par 001", "fournisseurs_ice_001"),
            ("Fournisseurs ICE 001", "fournisseurs_ice_001"),
            ("ICE 001 fournisseurs", "fournisseurs_ice_001"),
            ("Fournisseurs commençant par ICE 001", "fournisseurs_ice_001"),
            
            # Comptage de demandes
            ("Combien de demandes d'équipement ont été faites par gestionnaire bureau", "count_equipment_requests"),
            ("Nombre de demandes gestionnaire bureau", "count_equipment_requests"),
            ("Compte des demandes équipement", "count_equipment_requests"),
            ("Combien de demandes par utilisateur", "count_equipment_requests"),
            ("Total des demandes d'équipement", "count_equipment_requests"),
            
            # Affectation de matériels
            ("Matériels bureautiques affectés à gestionnaire bureau", "user_material_assignment"),
            ("Matériels affectés à l'utilisateur", "user_material_assignment"),
            ("Affectation matériels bureautiques", "user_material_assignment"),
            ("Quels matériels pour l'utilisateur", "user_material_assignment"),
            ("Matériels assignés à", "user_material_assignment"),
            
            # Demandes par date
            ("Demandes d'équipement approuvées en août 2025", "equipment_requests_by_date"),
            ("Demandes approuvées août 2025", "equipment_requests_by_date"),
            ("Demandes équipement août", "equipment_requests_by_date"),
            ("Demandes approuvées en juillet", "equipment_requests_by_date"),
            ("Demandes par mois", "equipment_requests_by_date"),
            
            # Montants totaux
            ("Coût total des commandes juillet 2025", "total_it_orders_amount"),
            ("Montant total commandes informatiques", "total_it_orders_amount"),
            ("Prix total des commandes", "total_it_orders_amount"),
            ("Coût total juillet 2025", "total_it_orders_amount"),
            ("Total des montants commandes", "total_it_orders_amount"),
            
            # Données manquantes (fallback)
            ("Quels sont les prix des matériels informatiques", "fallback"),
            ("Prix du matériel informatique", "fallback"),
            ("Coût des équipements", "fallback"),
            ("Historique des logs admin pour l'utilisateur superadmin", "fallback"),
            ("Logs d'activité admin", "fallback"),
            ("Historique des actions admin", "fallback"),
            
            # Intents existants pour maintenir la compatibilité
            ("Liste des fournisseurs", "liste_fournisseurs"),
            ("Tous les fournisseurs", "liste_fournisseurs"),
            ("Fournisseurs disponibles", "liste_fournisseurs"),
            ("Comparer les garanties", "compare_garanties"),
            ("Garantie des matériels", "compare_garanties"),
            ("Vérifier les garanties", "compare_garanties"),
            ("Matériels expirant bientôt", "check_expiring_soon"),
            ("Équipements qui expirent", "check_expiring_soon"),
            ("Garanties qui expirent", "check_expiring_soon")
        ]
        
        # Données de validation
        self.validation_data = [
            ("Code inventaire du serveur Lenovo", "codes_by_designation"),
            ("Statut livraison commande BC25", "delivery_status"),
            ("Fournisseur commande BC26", "order_supplier"),
            ("ICE 002 fournisseurs", "fournisseurs_ice_001"),
            ("Demandes équipement par mois", "count_equipment_requests"),
            ("Matériels affectés à test_employe", "user_material_assignment"),
            ("Demandes approuvées septembre", "equipment_requests_by_date"),
            ("Total coût commandes août", "total_it_orders_amount"),
            ("Prix matériel bureautique", "fallback"),
            ("Logs admin superadmin", "fallback")
        ]
    
    def prepare_training_data(self) -> Dataset:
        """Prépare les données d'entraînement pour le modèle BART"""
        try:
            # Créer le mapping des labels
            unique_labels = list(set([label for _, label in self.parcinfo_training_data]))
            self.label2id = {label: idx for idx, label in enumerate(unique_labels)}
            self.id2label = {idx: label for label, idx in self.label2id.items()}
            
            logger.info(f"Labels uniques: {unique_labels}")
            logger.info(f"Mapping label2id: {self.label2id}")
            
            # Préparer les données d'entraînement
            train_texts = []
            train_labels = []
            
            for text, label in self.parcinfo_training_data:
                train_texts.append(text)
                train_labels.append(self.label2id[label])
            
            # Créer le dataset
            train_dataset = Dataset.from_dict({
                'text': train_texts,
                'label': train_labels
            })
            
            logger.info(f"Dataset d'entraînement créé: {len(train_texts)} exemples")
            return train_dataset
            
        except Exception as e:
            logger.error(f"Erreur lors de la préparation des données: {e}")
            raise
    
    def prepare_validation_data(self) -> Dataset:
        """Prépare les données de validation"""
        try:
            val_texts = []
            val_labels = []
            
            for text, label in self.validation_data:
                if label in self.label2id:
                    val_texts.append(text)
                    val_labels.append(self.label2id[label])
            
            val_dataset = Dataset.from_dict({
                'text': val_texts,
                'label': val_labels
            })
            
            logger.info(f"Dataset de validation créé: {len(val_texts)} exemples")
            return val_dataset
            
        except Exception as e:
            logger.error(f"Erreur lors de la préparation de la validation: {e}")
            raise
    
    def tokenize_function(self, examples):
        """Fonction de tokenisation pour le dataset"""
        return self.tokenizer(
            examples['text'],
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
    
    def compute_metrics(self, pred):
        """Calcule les métriques de performance"""
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    def retrain_model(self, output_dir: str = "models/parcinfo_bart", 
                     num_epochs: int = 5, batch_size: int = 8) -> bool:
        """Réentraîne le modèle BART sur les données ParcInfo"""
        try:
            logger.info("Début du réentraînement du modèle BART pour ParcInfo")
            
            # Charger le tokenizer et le modèle
            logger.info(f"Chargement du modèle: {self.model_name}")
            self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
            self.model = BartForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=len(self.label2id),
                id2label=self.id2label,
                label2id=self.label2id
            )
            
            # Préparer les données
            train_dataset = self.prepare_training_data()
            val_dataset = self.prepare_validation_data()
            
            # Tokeniser les datasets
            train_dataset = train_dataset.map(self.tokenize_function, batched=True)
            val_dataset = val_dataset.map(self.tokenize_function, batched=True)
            
            # Configuration d'entraînement
            training_args = TrainingArguments(
                output_dir=output_dir,
                num_train_epochs=num_epochs,
                per_device_train_batch_size=batch_size,
                per_device_eval_batch_size=batch_size,
                warmup_steps=100,
                weight_decay=0.01,
                logging_dir=f"{output_dir}/logs",
                logging_steps=10,
                evaluation_strategy="epoch",
                save_strategy="epoch",
                load_best_model_at_end=True,
                metric_for_best_model="f1",
                greater_is_better=True,
                save_total_limit=3,
                dataloader_num_workers=2,
                dataloader_pin_memory=True,
                fp16=torch.cuda.is_available(),
                report_to=None  # Désactiver wandb
            )
            
            # Data collator
            data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
            
            # Trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                tokenizer=self.tokenizer,
                data_collator=data_collator,
                compute_metrics=self.compute_metrics
            )
            
            # Entraînement
            logger.info("Début de l'entraînement...")
            trainer.train()
            
            # Évaluation
            logger.info("Évaluation du modèle...")
            eval_results = trainer.evaluate()
            logger.info(f"Résultats d'évaluation: {eval_results}")
            
            # Sauvegarde
            logger.info(f"Sauvegarde du modèle dans: {output_dir}")
            trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            # Sauvegarder la configuration
            config = {
                "model_name": self.model_name,
                "label2id": self.label2id,
                "id2label": self.id2label,
                "training_data_size": len(self.parcinfo_training_data),
                "validation_data_size": len(self.validation_data),
                "training_date": datetime.now().isoformat(),
                "evaluation_results": eval_results
            }
            
            config_file = os.path.join(output_dir, "parcinfo_config.json")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            logger.info("Réentraînement terminé avec succès!")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du réentraînement: {e}")
            return False
    
    def load_retrained_model(self, model_path: str) -> bool:
        """Charge le modèle réentraîné"""
        try:
            logger.info(f"Chargement du modèle réentraîné: {model_path}")
            
            # Charger la configuration
            config_file = os.path.join(model_path, "parcinfo_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.label2id = config["label2id"]
                self.id2label = config["id2label"]
                logger.info(f"Configuration chargée: {len(self.label2id)} labels")
            
            # Charger le modèle et le tokenizer
            self.tokenizer = BartTokenizer.from_pretrained(model_path)
            self.model = BartForSequenceClassification.from_pretrained(model_path)
            
            logger.info("Modèle réentraîné chargé avec succès!")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            return False
    
    def load_training_data(self) -> Dataset:
        """Charge les données d'entraînement (alias pour prepare_training_data)"""
        return self.prepare_training_data()
    
    def predict_intent(self, text: str) -> Tuple[str, float]:
        """Prédit l'intent avec le modèle réentraîné"""
        try:
            if self.model is None or self.tokenizer is None:
                raise ValueError("Modèle non chargé. Utilisez load_retrained_model() d'abord.")
            
            # Tokenisation
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128
            )
            
            # Prédiction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=-1)
                predicted_id = torch.argmax(probabilities, dim=-1).item()
                confidence = probabilities[0][predicted_id].item()
            
            predicted_label = self.id2label[predicted_id]
            
            return predicted_label, confidence
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            return "fallback", 0.0

def main():
    """Fonction principale pour tester le réentraînement"""
    logging.basicConfig(level=logging.INFO)
    
    # Créer le réentraîneur
    retrainer = ParcInfoBartRetrainer()
    
    # Réentraîner le modèle
    success = retrainer.retrain_model(
        output_dir="models/parcinfo_bart",
        num_epochs=3,
        batch_size=4
    )
    
    if success:
        print("✅ Réentraînement réussi!")
        
        # Tester le modèle
        test_texts = [
            "Code inventaire de la Baie",
            "Statut de la livraison BC23",
            "Fournisseur de la commande BC23"
        ]
        
        for text in test_texts:
            intent, confidence = retrainer.predict_intent(text)
            print(f"'{text}' -> {intent} (confiance: {confidence:.3f})")
    else:
        print("❌ Échec du réentraînement")

if __name__ == "__main__":
    main()
