# apps/chatbot/management/commands/vectorize_all_models.py
import time
from django.core.management.base import BaseCommand
from django.db import connection
from apps.chatbot.auto_vectorization import vectorize_all_models
from apps.chatbot.models import DocumentVector


class Command(BaseCommand):
    help = 'Vectorisation complète et optimisée de tous les modèles du projet ParcInfo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Vectoriser uniquement les modèles d\'une application spécifique'
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Vectoriser un modèle spécifique (format: app.Model)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulation sans exécution réelle'
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Afficher uniquement les statistiques actuelles'
        )

    def handle(self, *args, **options):
        start_time = time.time()
        
        # Affichage des statistiques uniquement
        if options['stats']:
            self.show_statistics()
            return
        
        # Mode simulation
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('🔍 MODE SIMULATION - Aucune modification ne sera effectuée')
            )
            self.show_statistics()
            return
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Début de la vectorisation complète du projet ParcInfo...')
        )
        
        # Statistiques avant
        initial_count = DocumentVector.objects.count()
        self.stdout.write(f"📊 Vecteurs actuels: {initial_count}")
        
        try:
            # Exécution de la vectorisation
            final_count = vectorize_all_models()
            
            # Calcul du temps d'exécution
            execution_time = time.time() - start_time
            
            # Rapport final
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Vectorisation terminée avec succès!'
                )
            )
            self.stdout.write(f"⏱️  Temps d'exécution: {execution_time:.2f}s")
            self.stdout.write(f"📈 Vecteurs générés: {final_count}")
            self.stdout.write(f"🔄 Différence: +{final_count - initial_count}")
            
            # Validation de la cohérence
            self.validate_coherence()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de la vectorisation: {e}')
            )
            raise

    def show_statistics(self):
        """Affiche les statistiques actuelles des vecteurs"""
        self.stdout.write(self.style.SUCCESS('\n📊 STATISTIQUES ACTUELLES:'))
        
        # Comptage total
        total_vectors = DocumentVector.objects.count()
        self.stdout.write(f"📈 Total vecteurs: {total_vectors}")
        
        if total_vectors == 0:
            self.stdout.write(self.style.WARNING("⚠️  Aucun vecteur trouvé - Exécutez la vectorisation"))
            return
        
        # Répartition par modèle
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT app_label, model_name, COUNT(*) as count
                FROM chatbot_documentvector
                GROUP BY app_label, model_name
                ORDER BY count DESC
            """)
            
            self.stdout.write("\n📋 Répartition par modèle:")
            for app_label, model_name, count in cursor.fetchall():
                self.stdout.write(f"  {app_label}.{model_name}: {count} vecteurs")

    def validate_coherence(self):
        """Valide la cohérence RAG-DB"""
        from django.apps import apps
        
        # Comptage des enregistrements DB
        total_db_records = 0
        model_counts = {}
        
        # Applications cibles
        target_apps = [
            'fournisseurs', 'materiel_informatique', 'commande_informatique',
            'materiel_bureautique', 'commande_bureau', 'demande_equipement',
            'livraison', 'users'
        ]
        
        for app_label in target_apps:
            try:
                app_models = apps.get_app_config(app_label).get_models()
                for model_class in app_models:
                    count = model_class.objects.count()
                    if count > 0:
                        model_key = f"{app_label}.{model_class.__name__}"
                        model_counts[model_key] = count
                        total_db_records += count
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Erreur comptage {app_label}: {e}")
                )
        
        # Comptage des vecteurs RAG
        total_vectors = DocumentVector.objects.count()
        
        # Calcul du ratio de cohérence
        if total_db_records > 0:
            coherence_ratio = (total_vectors / total_db_records) * 100
            
            self.stdout.write(f"\n🔍 VALIDATION DE COHÉRENCE:")
            self.stdout.write(f"📚 Enregistrements DB: {total_db_records}")
            self.stdout.write(f"🔢 Vecteurs RAG: {total_vectors}")
            self.stdout.write(f"📈 Ratio de cohérence: {coherence_ratio:.1f}%")
            
            # Évaluation de la cohérence
            if coherence_ratio >= 80:
                self.stdout.write(self.style.SUCCESS("✅ Cohérence excellente (≥80%)"))
            elif coherence_ratio >= 60:
                self.stdout.write(self.style.WARNING("⚠️ Cohérence acceptable (≥60%)"))
            else:
                self.stdout.write(self.style.ERROR("❌ Cohérence faible (<60%)"))
                self.stdout.write("💡 Recommandation: Vérifiez la configuration des modèles")
        
        else:
            self.stdout.write(self.style.ERROR("❌ Aucun enregistrement trouvé en base"))
