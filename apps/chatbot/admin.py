from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_preview', 'response_preview', 'timestamp', 'session_id']
    list_filter = ['timestamp', 'user']
    search_fields = ['message', 'response', 'user__username']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def response_preview(self, obj):
        return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response
    response_preview.short_description = 'Réponse'
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user', 'session_id')
        }),
        ('Conversation', {
            'fields': ('message', 'response')
        }),
        ('Métadonnées', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    ) 