from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatMessage(models.Model):
    """Modèle pour stocker l'historique des conversations du chatbot"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField(verbose_name="Message utilisateur")
    response = models.TextField(verbose_name="Réponse du chatbot")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure")
    session_id = models.CharField(max_length=100, blank=True, verbose_name="ID de session")
    
    class Meta:
        verbose_name = "Message de chat"
        verbose_name_plural = "Messages de chat"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Chat {self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}" 