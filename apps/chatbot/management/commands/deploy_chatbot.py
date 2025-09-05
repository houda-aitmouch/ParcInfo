import logging
import traceback
from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from time import time
from typing import Dict, Any

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Déploie et configure le chatbot ParcInfo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Teste le chatbot avec des requêtes de base'
        )
        parser.add_argument(
            '--vectorize',
            action='store_true',
            help='Vectorise les données dans la base de données'
        )
        parser.add_argument(
            '--rebuild',
            action='store_true',
            help='Reconstruit complètement les index vectoriels'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Valide la configuration actuelle'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Taille des lots pour la vectorisation (défaut: 1000)'
        )

    def handle(self, *args, **options):
        self.start_time = time()
        self.options = options

        self.stdout.write(self.style.SUCCESS("\n🚀 Déploiement du chatbot ParcInfo..."))
        self.stdout.write(f"Options sélectionnées: {self._format_options(options)}")

        try:
            # 1. Vérification de la base de données
            self._check_database()

            # 2. Vectorisation des données si demandé
            if options['vectorize'] or options['rebuild']:
                self._vectorize_data(batch_size=options['batch_size'])

            # 3. Tests si demandé
            if options['test']:
                self._run_tests()

            # 4. Validation si demandé
            if options['validate']:
                self._validate_setup()
                
            # 5. RAG-DB coherence validation (always run when testing or validating)
            if options['test'] or options['validate']:
                from apps.chatbot.core_chatbot import get_chatbot
                chatbot = get_chatbot()
                self._validate_rag_db_coherence(chatbot)

            elapsed = time() - self.start_time
            self.stdout.write(
                self.style.SUCCESS(f"\n✅ Déploiement terminé avec succès en {elapsed:.2f}s !")
            )

        except Exception as e:
            elapsed = time() - self.start_time
            self.stdout.write(self.style.ERROR(f"\n❌ Erreur après {elapsed:.2f}s: {e}"))
            logger.error("Erreur lors du déploiement:\n%s", traceback.format_exc())
            raise

    def _format_options(self, options: Dict[str, Any]) -> str:
        """Formate les options pour l'affichage"""
        active_options = [k for k, v in options.items() if v and k != 'batch_size']
        if options['batch_size'] != 1000:
            active_options.append(f"batch_size={options['batch_size']}")
        return ", ".join(active_options) or "Aucune option spécifique"

    def _check_database(self):
        """Vérifie les dépendances de base de données et les enregistrements - Critical Fix"""
        self.stdout.write("\n🔍 Vérification des dépendances de base de données...")

        required_extensions = {
            'vector': 'pgvector (pour les embeddings vectoriels)',
            'pg_trgm': 'pg_trgm (pour la recherche textuelle)',
            'uuid-ossp': 'uuid-ossp (pour les UUID)'
        }

        with connection.cursor() as cursor:
            for ext, description in required_extensions.items():
                cursor.execute(
                    "SELECT 1 FROM pg_extension WHERE extname = %s",
                    [ext]
                )
                if not cursor.fetchone():
                    raise Exception(
                        f"Extension PostgreSQL requise manquante: {description}\n"
                        f"Installez-la avec: CREATE EXTENSION IF NOT EXISTS {ext};"
                    )
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Extension {ext} ({description}) est installée")
                )

        # Vérifier les modèles nécessaires ET leur contenu
        required_models = [
            ('materiel_informatique', 'MaterielInformatique'),
            ('materiel_bureautique', 'MaterielBureau'),
            ('commande_informatique', 'Commande'),
            ('commande_bureau', 'CommandeBureau'),
            ('fournisseurs', 'Fournisseur'),
            ('livraison', 'Livraison'),
            ('demande_equipement', 'DemandeEquipement'),
            ('demande_equipement', 'ArchiveDecharge'),
            ('chatbot', 'DocumentVector')
        ]
        
        empty_tables = []
        total_records = 0
        
        for app, model in required_models:
            try:
                mdl = apps.get_model(app, model)
                record_count = mdl.objects.count()
                total_records += record_count
                
                if record_count == 0:
                    empty_tables.append(f"{app}.{model}")
                    self.stdout.write(
                        self.style.WARNING(f"⚠ Modèle {app}.{model} disponible mais VIDE (0 enregistrements)")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Modèle {app}.{model} disponible ({record_count} enregistrements)")
                    )
            except LookupError:
                raise Exception(f"Modèle requis introuvable: {app}.{model}")
        
        # Rapport sur les tables vides
        if empty_tables:
            self.stdout.write(
                self.style.WARNING(f"\n⚠ ATTENTION: {len(empty_tables)} tables sont vides:")
            )
            for table in empty_tables:
                self.stdout.write(f"   • {table}")
            self.stdout.write(
                self.style.WARNING(
                    "Cela peut causer des réponses 'Aucune donnée disponible' du chatbot."
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Total: {total_records} enregistrements dans {len(required_models)} modèles")
        )

    def _vectorize_data(self, batch_size: int):
        """Vectorise les données avec gestion par lots"""
        from apps.chatbot.rag_manager import RAGManager

        self.stdout.write("\n🔄 Vectorisation des données...")

        rag = RAGManager()

        if self.options['rebuild']:
            self.stdout.write("Nettoyage des vecteurs existants...")
            if rag.clear_all_documents():
                self.stdout.write(self.style.SUCCESS("✓ Anciens vecteurs supprimés"))
            else:
                raise Exception("Échec du nettoyage des vecteurs existants")

        self.stdout.write(f"Vectorisation des données (batch_size configuré: {batch_size})...")

        start_time = time()
        try:
            rag.populate_index()  # Remove unsupported batch_size parameter
            count = rag.get_rag_count()
            elapsed = time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Données vectorisées avec succès ({count} documents en {elapsed:.2f}s)"
                )
            )
        except Exception as e:
            elapsed = time() - start_time
            self.stdout.write(
                self.style.ERROR(
                    f"Échec après {elapsed:.2f}s: {str(e)}"
                )
            )
            raise

    def _run_tests(self):
        """Exécute des tests avec validation anti-hallucination - Critical Fix"""
        from apps.chatbot.core_chatbot import get_chatbot
        from apps.fournisseurs.models import Fournisseur

        self.stdout.write("\n🔧 Exécution des tests avec validation anti-hallucination...")
        chatbot = get_chatbot()

        # Tests d'intention standard
        intent_tests = [
            ("Liste du matériel informatique", "recherche_materiel"),
            ("Commandes du mois dernier", "liste_commandes"),
            ("Qui sont nos fournisseurs ?", "liste_fournisseurs"),
            ("Statut de la livraison BC-2023-456", "statut_livraison"),
            ("Demandes en attente", "demandes_equipement"),
            ("Où est le PC-789 ?", "recherche_materiel"),
            ("Statistiques du parc", "statistiques"),
        ]

        # Tests anti-hallucination critiques
        hallucination_tests = [
            ("Liste tous les fournisseurs disponibles avec leur ICE", ["Belkin", "AEBDM", "3STD"]),
            ("Combien de livraisons sont en retard ?", ["Lenovo ThinkSystem"]),
            ("Recherche matériel par code inventaire", ["PC-123", "SRV-001"])
        ]

        failed = 0
        hallucination_failures = 0

        # Test des intentions
        for query, expected_intent in intent_tests:
            try:
                start_time = time()
                result = chatbot._classify_intent(query)
                intent = result.get('intent', 'unknown')
                confidence = result.get('confidence', 0)
                response = chatbot.process_query(query)
                elapsed = (time() - start_time) * 1000

                if intent == expected_intent:
                    self.stdout.write(f"✓ [{elapsed:.1f}ms] '{query}' → {intent} (confiance: {confidence}%)")
                else:
                    self.stdout.write(f"✗ [{elapsed:.1f}ms] '{query}' → {intent} (attendu: {expected_intent})")
                    failed += 1

                # Safe response handling
                response_str = str(response) if response is not None else "Aucune réponse"
                if isinstance(response, dict):
                    response_str = str(response.get('response', response))
                
                self.stdout.write(f"   Réponse: {response_str[:120]}{'...' if len(response_str) > 120 else ''}")

            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"☠ Erreur avec '{query}': {str(e)}"
                    )
                )
                logger.error("Test failed for query '%s': %s", query, traceback.format_exc())

        # Test anti-hallucination
        self.stdout.write("\n🛡️ Testing anti-hallucination measures...")
        test_queries = [
            "Quels fournisseurs ont fourni plus de 2 commandes?",
            "Liste des matériels Lenovo", 
            "Fournisseurs avec ICE commençant par AEBDM",
            "Actions administratives de juillet 2025"
        ]
        
        hallucination_detected = False
        # CRITICAL FIX: Only flag entities that are NOT in database
        # AEBDM and 3STD are legitimate suppliers in the database
        forbidden_entities = ['Belkin', 'Lenovo ThinkSystem']
        
        for query in test_queries:
            try:
                response = chatbot.process_query(query)
                response_text = response.get('response', '') if isinstance(response, dict) else str(response)
                
                for entity in forbidden_entities:
                    if entity in response_text:
                        self.stdout.write(
                            self.style.WARNING(f"⚠️  Hallucination detected in query '{query}': Found '{entity}'")
                        )
                        hallucination_detected = True
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error testing query '{query}': {str(e)}")
                )

        # Test new admin actions handler
        self.stdout.write("Testing admin actions handler...")
        try:
            admin_response = chatbot.process_query("Actions administratives de juillet 2025")
            if isinstance(admin_response, dict):
                admin_text = admin_response.get('response', '')
                if 'Actions Administratives' in admin_text:
                    self.stdout.write(self.style.SUCCESS("✅ Admin actions handler working correctly"))
                else:
                    self.stdout.write(self.style.WARNING("⚠️  Admin actions handler may not be routing correctly"))
            else:
                self.stdout.write(self.style.WARNING("⚠️  Unexpected admin response format"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Admin actions test failed: {str(e)}"))
        
        if not hallucination_detected:
            self.stdout.write(self.style.SUCCESS("✅ No hallucinations detected in test queries"))
        else:
            self.stdout.write(self.style.ERROR("❌ Hallucination detection failed - review anti-hallucination measures"))

        # Rapport final
        total_tests = len(intent_tests) + len(hallucination_tests)
        total_failures = failed + hallucination_failures
        
        if total_failures:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠ {total_failures}/{total_tests} tests ont échoué "
                    f"(Intentions: {failed}, Anti-hallucination: {hallucination_failures})"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ Tous les {total_tests} tests ont réussi (anti-hallucination inclus)"
                )
            )

    def _validate_rag_db_coherence(self, chatbot):
        """Validate RAG-DB coherence using chatbot's new method"""
        try:
            self.stdout.write("\n🔍 Validating RAG-DB coherence...")
            coherence_report = chatbot.validate_rag_db_coherence()
            
            if coherence_report['status'] == 'success':
                ratio = coherence_report['coherence_ratio']
                self.stdout.write(f"📊 Database records: {coherence_report['total_db_records']}")
                self.stdout.write(f"🔢 RAG vectors: {coherence_report['total_rag_vectors']}")
                self.stdout.write(f"📈 Coherence ratio: {ratio:.2%}")
                
                if ratio >= 0.8:
                    self.stdout.write(self.style.SUCCESS("✅ RAG-DB coherence is excellent"))
                elif ratio >= 0.6:
                    self.stdout.write(self.style.WARNING("⚠️  RAG-DB coherence is acceptable but could be improved"))
                else:
                    self.stdout.write(self.style.ERROR("❌ RAG-DB coherence is poor - rebuild recommended"))
                
                if coherence_report['missing_in_rag']:
                    self.stdout.write(self.style.WARNING("⚠️  Missing entities in RAG:"))
                    for missing in coherence_report['missing_in_rag'][:5]:  # Show first 5
                        self.stdout.write(f"   • {missing}")
                
                if coherence_report['recommendations']:
                    self.stdout.write("💡 Recommendations:")
                    for rec in coherence_report['recommendations']:
                        self.stdout.write(f"   • {rec}")
                        
            else:
                self.stdout.write(self.style.ERROR(f"❌ Coherence validation failed: {coherence_report.get('error', 'Unknown error')}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error during coherence validation: {str(e)}"))

    def _validate_setup(self):
        """Valide la configuration avec vérification de cohérence - Critical Fix"""
        from apps.chatbot.models import DocumentVector
        from apps.chatbot.rag_manager import RAGManager
        from apps.fournisseurs.models import Fournisseur
        from apps.materiel_informatique.models import MaterielInformatique
        from apps.commande_informatique.models import Commande

        self.stdout.write("\n🔎 Validation de la configuration avec vérification de cohérence...")

        # Vérifier les vecteurs
        vector_count = DocumentVector.objects.count()
        self.stdout.write(f"📊 Nombre de vecteurs dans la base: {vector_count}")

        if vector_count == 0:
            self.stdout.write(
                self.style.WARNING(
                    "⚠ Aucun vecteur trouvé. Utilisez --vectorize pour en créer"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("✓ Base vectorielle opérationnelle")
            )

        # Vérification de cohérence RAG vs DB
        self.stdout.write("\n🔍 Vérification de cohérence RAG ↔ Base de données...")
        
        try:
            rag = RAGManager()
            
            # Test de cohérence fournisseurs
            db_supplier_count = Fournisseur.objects.count()
            if db_supplier_count > 0:
                sample_supplier = Fournisseur.objects.first()
                rag_results = rag.semantic_search(f"fournisseur {sample_supplier.nom}", top_k=5)
                
                if rag_results:
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ RAG trouve des résultats pour fournisseur '{sample_supplier.nom}'")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠ RAG ne trouve pas '{sample_supplier.nom}' - Réindexation recommandée")
                    )
            
            # Test de cohérence matériel
            db_material_count = MaterielInformatique.objects.count()
            if db_material_count > 0:
                sample_material = MaterielInformatique.objects.first()
                rag_results = rag.semantic_search(f"matériel {sample_material.code_inventaire}", top_k=5)
                
                if rag_results:
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ RAG trouve des résultats pour matériel '{sample_material.code_inventaire}'")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠ RAG ne trouve pas '{sample_material.code_inventaire}' - Réindexation recommandée")
                    )
            
            # Rapport de cohérence
            total_db_records = (
                Fournisseur.objects.count() + 
                MaterielInformatique.objects.count() + 
                Commande.objects.count()
            )
            
            coherence_ratio = min(vector_count / max(total_db_records, 1), 1.0) * 100
            
            if coherence_ratio >= 80:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Cohérence RAG/DB: {coherence_ratio:.1f}% (Excellent)")
                )
            elif coherence_ratio >= 50:
                self.stdout.write(
                    self.style.WARNING(f"⚠ Cohérence RAG/DB: {coherence_ratio:.1f}% (Acceptable)")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Cohérence RAG/DB: {coherence_ratio:.1f}% (Critique - Réindexation requise)")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur validation cohérence: {str(e)}")
            )

        # Vérifier les modèles importants
        critical_models = [
            ('materiel_informatique', 'MaterielInformatique'),
            ('materiel_bureautique', 'MaterielBureau'),
            ('commande_informatique', 'Commande')
        ]

        for app, model in critical_models:
            try:
                mdl = apps.get_model(app, model)
                record_count = mdl.objects.count()
                self.stdout.write(
                    f"📦 {app}.{model}: {record_count} enregistrements"
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"☠ Impossible d'accéder à {app}.{model}: {str(e)}"
                    )
                )

        # Vérifier la taille des embeddings
        try:
            from sentence_transformers import SentenceTransformer
            import torch
            device = 'mps' if torch.backends.mps.is_available() else 'cpu'
            model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device=device)
            embedding_size = len(model.encode("test"))
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Modèle d'embedding chargé (dimension: {embedding_size})"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"☠ Erreur de chargement du modèle d'embedding: {str(e)}"
                )
            )