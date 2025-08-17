from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chatbot'
    verbose_name = 'Chatbot Support'
    
    def ready(self):
        """Initialise les signals lors du démarrage de l'application"""
        try:
            import apps.chatbot.auto_vectorization
        except ImportError:
            pass