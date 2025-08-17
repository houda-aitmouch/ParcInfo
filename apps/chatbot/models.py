from django.db import models
from django.contrib.auth import get_user_model
from pgvector.django import VectorField, IvfflatIndex
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    session_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']


class DocumentVector(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    embedding = VectorField(dimensions=384)

    model_name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    indexed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            IvfflatIndex(fields=['embedding'], name='embedding_idx', lists=100),
        ]
        unique_together = ['content_type', 'object_id']


class ChatbotInteraction(models.Model):
    session_id = models.CharField(max_length=100)
    user_query = models.TextField()
    detected_intent = models.CharField(max_length=50, null=True, blank=True)
    sql_attempted = models.BooleanField(default=False)
    sql_results = models.IntegerField(default=0)
    rag_results = models.IntegerField(default=0)
    final_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']


class IntentExample(models.Model):
    intent = models.CharField(max_length=50)
    phrase = models.TextField()
    weight = models.FloatField(default=1.0)
    source = models.CharField(max_length=20, choices=[
        ('user', 'User'),
        ('system', 'System'),
        ('import', 'Import')
    ], default='system')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('intent', 'phrase')


class ChatbotFeedback(models.Model):
    session_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.TextField()

    intent_pred = models.CharField(max_length=50, null=True, blank=True)
    entities_pred = models.JSONField(null=True, blank=True)

    intent_final = models.CharField(max_length=50, null=True, blank=True)
    entities_final = models.JSONField(null=True, blank=True)

    rating = models.SmallIntegerField(null=True, blank=True)
    reward = models.FloatField(default=0.0)
    response_snippet = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']