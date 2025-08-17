from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_ui, name='chatbot-ui'),
    path('api/', views.chatbot_api, name='chatbot-api'),
    path('process_query/', views.chatbot_api, name='chatbot-process-query'),  # Alias pour compatibilité
    path('status/', views.chatbot_status, name='chatbot-status'),
]