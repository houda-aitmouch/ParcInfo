from django.core.management.base import BaseCommand
from apps.chatbot.rag_manager import RAGManager
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate RAG index with all relevant models and records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing index before populating',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Batch size for indexing (default: 100)',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 Starting RAG index population...")
        
        try:
            rag_manager = RAGManager()
            
            if options['clear']:
                self.stdout.write("🗑️  Clearing existing index...")
                rag_manager.clear_index()
            
            # Populate index with all models
            self.stdout.write("📚 Populating index with all models...")
            rag_manager.populate_index()
            
            # Get final count
            final_count = rag_manager.get_rag_count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ RAG index populated successfully!\n"
                    f"🔢 RAG vectors: {final_count}\n"
                    f"📚 All models indexed successfully"
                )
            )
            
        except Exception as e:
            logger.error(f"Error populating RAG index: {e}")
            self.stdout.write(
                self.style.ERROR(f"❌ Error populating RAG index: {str(e)}")
            )
            raise
