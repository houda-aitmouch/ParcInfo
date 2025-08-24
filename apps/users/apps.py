from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = "Utilisateurs"
    
    def ready(self):
        """Import des signals lors du démarrage de l'application"""
        import apps.users.signals
