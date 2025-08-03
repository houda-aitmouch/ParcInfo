import os
import json
import warnings
warnings.filterwarnings("ignore", message="Please see the migration guide at: https://python.langchain.com/docs/versions/migrating_memory/")
from typing import List, Dict, Any

# Core LangChain
import langchain
import warnings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# Modules communautaires
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import Chroma

# Import recommandé pour HuggingFacePipeline et HuggingFaceEmbeddings directement depuis langchain_huggingface
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings

# Transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from django.db import connection
from django.contrib.auth import get_user_model

import pandas as pd
User = get_user_model()

class ParcInfoChatbot:
    """Chatbot IA avancé pour le système ParcInfo avec apprentissage continu"""

    def __init__(self):
        self.llm = None
        self.vectorstore = None
        self.chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )
        self.conversation_history = []
        self.initialize_llm()
        self.initialize_vectorstore()
        self.initialize_chain()

    def initialize_llm(self):
        """Initialiser le modèle LLaMA 3"""
        try:
            model_path = os.getenv('LLAMA_MODEL_PATH', 'models/llama-3-8b-instruct.gguf')

            if os.path.exists(model_path):
                self.llm = LlamaCpp(
                    model_path=model_path,
                    temperature=0.7,
                    max_tokens=2048,
                    top_p=1,
                    verbose=True,
                    n_ctx=4096,
                    repeat_penalty=1.1
                )
                print(f"✅ LLaMA 3 initialisé: {model_path}")
            else:
                model_name = "microsoft/DialoGPT-medium"
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)

                pipe = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_length=2048,
                    temperature=0.7,
                    do_sample=True
                )

                self.llm = HuggingFacePipeline(pipeline=pipe)
                print(f"✅ HuggingFace Pipeline: {model_name}")

        except Exception as e:
            print(f"❌ Erreur LLM: {e}")
            self.llm = None

    def get_comprehensive_database_context(self) -> str:
        """Récupérer le contexte complet et détaillé de la base de données"""
        context_parts = []

        try:
            with connection.cursor() as cursor:
                # Statistiques globales
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_users,
                        COUNT(CASE WHEN is_superuser THEN 1 END) as superusers,
                        COUNT(CASE WHEN is_staff THEN 1 END) as staff,
                        COUNT(CASE WHEN NOT is_superuser AND NOT is_staff THEN 1 END) as employees
                    FROM users_customuser
                """)
                user_stats = cursor.fetchone()
                context_parts.append(f"Utilisateurs: {user_stats[0]} total ({user_stats[1]} superadmin, {user_stats[2]} staff, {user_stats[3]} employés)")

                # Demandes d'équipement détaillées
                cursor.execute("""
                    SELECT statut, categorie, type_demande, COUNT(*) as count
                    FROM demande_equipement_demandeequipement
                    GROUP BY statut, categorie, type_demande
                    ORDER BY count DESC
                """)
                demandes = cursor.fetchall()
                if demandes:
                    context_parts.append("Demandes d'équipement:")
                    for statut, categorie, type_demande, count in demandes:
                        context_parts.append(f"- {categorie} {type_demande}: {count} ({statut})")

                # Matériel informatique
                cursor.execute("""
                    SELECT statut, lieu_stockage, COUNT(*) as count
                    FROM materiel_informatique_materielinformatique
                    GROUP BY statut, lieu_stockage
                    ORDER BY count DESC
                """)
                materiel_info = cursor.fetchall()
                if materiel_info:
                    context_parts.append("Matériel informatique:")
                    for statut, lieu, count in materiel_info:
                        context_parts.append(f"- {statut}: {count} ({lieu})")

                # Matériel bureautique
                cursor.execute("""
                    SELECT statut, lieu_stockage, COUNT(*) as count
                    FROM materiel_bureautique_materielbureau
                    GROUP BY statut, lieu_stockage
                    ORDER BY count DESC
                """)
                materiel_bureau = cursor.fetchall()
                if materiel_bureau:
                    context_parts.append("Matériel bureautique:")
                    for statut, lieu, count in materiel_bureau:
                        context_parts.append(f"- {statut}: {count} ({lieu})")

                # Livraisons
                cursor.execute("""
                    SELECT statut_livraison, type_commande, COUNT(*) as count
                    FROM livraison_livraison
                    GROUP BY statut_livraison, type_commande
                    ORDER BY count DESC
                """)
                livraisons = cursor.fetchall()
                if livraisons:
                    context_parts.append("Livraisons:")
                    for statut, type_commande, count in livraisons:
                        context_parts.append(f"- {type_commande}: {count} ({statut})")

                # Fournisseurs
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM fournisseurs_fournisseur
                """)
                fournisseurs_count = cursor.fetchone()[0]
                context_parts.append(f"Fournisseurs: {fournisseurs_count}")

        except Exception as e:
            context_parts.append(f"Erreur base de données: {e}")

        return "\n".join(context_parts)

    def get_user_context(self, user: User) -> str:
        """Récupérer le contexte spécifique à l'utilisateur"""
        user_context = []

        try:
            with connection.cursor() as cursor:
                # Rôle de l'utilisateur
                role = "Super Admin" if user.is_superuser else "Gestionnaire" if user.is_staff else "Employé"
                user_context.append(f"Rôle: {role}")

                # Demandes gérées par l'utilisateur
                cursor.execute("""
                    SELECT statut, categorie, type_demande, COUNT(*) as count
                    FROM demande_equipement_demandeequipement
                    WHERE demandeur_id = %s
                    GROUP BY statut, categorie, type_demande
                    ORDER BY count DESC
                """, [user.id])
                user_demandes = cursor.fetchall()
                if user_demandes:
                    user_context.append("Demandes personnelles:")
                    for statut, categorie, type_demande, count in user_demandes:
                        user_context.append(f"- {categorie} {type_demande}: {count} ({statut})")

                # Matériel géré par l'utilisateur
                cursor.execute("""
                    SELECT statut, COUNT(*) as count
                    FROM materiel_informatique_materielinformatique
                    WHERE utilisateur_id = %s
                    GROUP BY statut
                """, [user.id])
                user_materiel_info = cursor.fetchall()
                if user_materiel_info:
                    user_context.append("Matériel informatique géré:")
                    for statut, count in user_materiel_info:
                        user_context.append(f"- {statut}: {count}")

                cursor.execute("""
                    SELECT statut, COUNT(*) as count
                    FROM materiel_bureautique_materielbureau
                    WHERE utilisateur_id = %s
                    GROUP BY statut
                """, [user.id])
                user_materiel_bureau = cursor.fetchall()
                if user_materiel_bureau:
                    user_context.append("Matériel bureautique géré:")
                    for statut, count in user_materiel_bureau:
                        user_context.append(f"- {statut}: {count}")

        except Exception as e:
            user_context.append(f"Erreur contexte utilisateur: {e}")

        return "\n".join(user_context) if user_context else "Aucune donnée personnelle"

    def get_system_analytics(self) -> str:
        """Récupérer des analyses système avancées"""
        analytics = []

        try:
            with connection.cursor() as cursor:
                # Tendances des demandes
                cursor.execute("""
                    SELECT 
                        DATE(date_demande) as date,
                        COUNT(*) as count,
                        AVG(CASE WHEN statut = 'approuvee' THEN 1 ELSE 0 END) as approval_rate
                    FROM demande_equipement_demandeequipement
                    WHERE date_demande >= CURRENT_DATE - INTERVAL '30 days'
                    GROUP BY DATE(date_demande)
                    ORDER BY date DESC
                    LIMIT 10
                """)
                trends = cursor.fetchall()
                if trends:
                    analytics.append("Tendances récentes (30 jours):")
                    for date, count, approval_rate in trends:
                        analytics.append(f"- {date}: {count} demandes ({approval_rate*100:.1f}% approuvées)")

                # Performance du système
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_demandes,
                        COUNT(CASE WHEN statut = 'approuvee' THEN 1 END) as approuvees,
                        COUNT(CASE WHEN statut = 'refusee' THEN 1 END) as refusees,
                        COUNT(CASE WHEN statut = 'en_attente' THEN 1 END) as en_attente
                    FROM demande_equipement_demandeequipement
                """)
                perf = cursor.fetchone()
                if perf:
                    total, approuvees, refusees, en_attente = perf
                    if total > 0:
                        analytics.append(f"Performance: {approuvees}/{total} approuvées ({approuvees/total*100:.1f}%)")
                        analytics.append(f"En attente: {en_attente}, Refusées: {refusees}")

        except Exception as e:
            analytics.append(f"Erreur analytics: {e}")

        return "\n".join(analytics)

    def initialize_vectorstore(self):
        """Initialiser le vectorstore avec contexte enrichi"""
        try:
            documents = []

            # Documentation système complète
            system_doc = """
            Système ParcInfo - Gestion Avancée de Parc Informatique et Bureautique
            
            ARCHITECTURE DU SYSTÈME:
            - Gestion centralisée des équipements informatiques et bureautiques
            - Workflow de demandes automatisé avec approbation hiérarchique
            - Suivi complet du cycle de vie des équipements
            - Intégration fournisseurs et livraisons
            - Reporting et analytics en temps réel
            
            RÔLES UTILISATEURS:
            - Super Admin: Accès complet, gestion utilisateurs, configuration système
            - Gestionnaire Informatique: Gestion matériel informatique, approbation demandes
            - Gestionnaire Bureau: Gestion matériel bureautique, approbation demandes
            - Employé: Soumission demandes, consultation matériel assigné
            
            WORKFLOW DE DEMANDE:
            1. Soumission par l'employé (categorie, type_demande, designation)
            2. Validation automatique des règles métier
            3. Notification aux gestionnaires concernés
            4. Approbation/refus avec justifications
            5. Affectation matériel si approuvée
            6. Signature décharge électronique
            7. Livraison et installation
            8. Suivi maintenance et garantie
            
            STATUTS ET TRANSITIONS:
            Demandes: en_attente → approuvee/refusee → affectee → livree
            Matériel: nouveau → affecte → operationnel → maintenance → reforme
            Livraisons: en_attente → en_cours → livree → validee
            
            MÉTRIQUES CLÉS:
            - Taux d'approbation des demandes
            - Temps de traitement moyen
            - Taux d'utilisation du matériel
            - Coûts par catégorie d'équipement
            - Satisfaction utilisateur
            """

            documents.append(Document(page_content=system_doc, metadata={"source": "system_architecture"}))

            # Contexte base de données
            db_context = self.get_comprehensive_database_context()
            if db_context:
                documents.append(Document(page_content=f"État système actuel:\n{db_context}", metadata={"source": "database_state"}))

            # Analytics système
            analytics = self.get_system_analytics()
            if analytics:
                documents.append(Document(page_content=f"Analytics système:\n{analytics}", metadata={"source": "system_analytics"}))

            # Initialiser embeddings et vectorstore
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )

            if documents:
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=embeddings,
                    persist_directory="./chroma_db"
                )
                print("✅ Vectorstore enrichi initialisé")

        except Exception as e:
            print(f"❌ Erreur vectorstore: {e}")
            self.vectorstore = None

    def initialize_chain(self):
        """Initialiser la chaîne de conversation avec apprentissage"""
        if not self.llm or not self.vectorstore:
            print("❌ Impossible d'initialiser la chaîne")
            return

        try:
            # Prompt optimisé pour apprentissage continu
            template = """
            Tu es l'assistant IA ParcInfo, un expert en gestion de parc informatique et bureautique.
            
            CONTEXTE SYSTÈME:
            {context}
            
            HISTORIQUE CONVERSATION:
            {chat_history}
            
            QUESTION UTILISATEUR: {question}
            
            DIRECTIVES:
            1. Réponds en français professionnel et technique
            2. Utilise les données du contexte pour des réponses précises
            3. Fournis des insights basés sur les analytics
            4. Suggère des améliorations et optimisations
            5. Explique les processus et workflows
            6. Donne des recommandations d'action
            7. Adapte tes réponses au rôle de l'utilisateur
            8. Apprends des interactions précédentes pour améliorer tes réponses
            
            RÉPONSE:
            """

            prompt = PromptTemplate(
                input_variables=["context", "chat_history", "question"],
                template=template
            )

            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 7}),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": prompt},
                return_source_documents=True,
                verbose=True
            )

            print("✅ Chaîne avec apprentissage initialisée")

        except Exception as e:
            print(f"❌ Erreur chaîne: {e}")

    def get_response(self, question: str, user: User = None) -> str:
        """Générer une réponse IA avec apprentissage continu"""
        try:
            if not self.chain:
                return "Système IA temporairement indisponible. Contactez l'administrateur."

            # Construire le contexte enrichi
            user_context = ""
            if user:
                user_data = self.get_user_context(user)
                user_context = f"\n\nCONTEXTE UTILISATEUR ({user.username}):\n{user_data}"

            # Question enrichie avec contexte
            enriched_question = f"{question}{user_context}"

            # Générer réponse via LangChain
            response = self.chain({"question": enriched_question})
            answer = response.get('answer', '')

            # Validation et amélioration de la réponse
            if not answer or len(answer.strip()) < 20:
                # Tentative de reformulation
                reformulated_question = f"Question technique ParcInfo: {question}"
                response = self.chain({"question": reformulated_question})
                answer = response.get('answer', '')

            # Réponse de secours si nécessaire
            if not answer or len(answer.strip()) < 20:
                answer = f"Je traite votre question sur '{question}'. Pour une réponse optimale, pourriez-vous préciser votre demande ? Je peux analyser les données système, fournir des insights, et vous guider dans la gestion du parc."

            # Apprentissage: sauvegarder l'interaction
            self.learn_from_interaction(question, answer, user)

            return answer

        except Exception as e:
            print(f"❌ Erreur génération réponse: {e}")
            return "Erreur technique. Le système IA est en cours de récupération."

    def learn_from_interaction(self, question: str, answer: str, user: User = None):
        """Apprentissage continu basé sur les interactions"""
        try:
            # Sauvegarder l'interaction pour apprentissage
            interaction = {
                'question': question,
                'answer': answer,
                'user_role': 'Super Admin' if user and user.is_superuser else 'Gestionnaire' if user and user.is_staff else 'Employé',
                'timestamp': pd.Timestamp.now(),
                'context_length': len(answer)
            }

            self.conversation_history.append(interaction)

            # Limiter l'historique pour éviter la surcharge mémoire
            if len(self.conversation_history) > 1000:
                self.conversation_history = self.conversation_history[-500:]

            # Rafraîchir le contexte périodiquement
            if len(self.conversation_history) % 50 == 0:
                self.refresh_context()

        except Exception as e:
            print(f"❌ Erreur apprentissage: {e}")

    def refresh_context(self):
        """Rafraîchir le contexte avec nouvelles données"""
        try:
            print("🔄 Rafraîchissement contexte IA...")
            self.initialize_vectorstore()
            self.initialize_chain()
            print("✅ Contexte rafraîchi")
        except Exception as e:
            print(f"❌ Erreur rafraîchissement: {e}")

    def get_learning_insights(self) -> Dict[str, Any]:
        """Obtenir des insights sur l'apprentissage du chatbot"""
        if not self.conversation_history:
            return {"message": "Aucune donnée d'apprentissage disponible"}

        try:
            df = pd.DataFrame(self.conversation_history)

            insights = {
                'total_interactions': len(df),
                'avg_response_length': df['context_length'].mean(),
                'user_role_distribution': df['user_role'].value_counts().to_dict(),
                'recent_activity': len(df[df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(days=7)]),
                'learning_progress': "Actif" if len(df) > 10 else "En cours d'initialisation"
            }

            return insights

        except Exception as e:
            return {"error": f"Erreur insights: {e}"}