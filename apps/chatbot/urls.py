from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_ui, name='chatbot-ui'),
    path('api/', views.chatbot_api, name='chatbot-api'),
    path('process_query/', views.chatbot_api, name='chatbot-process-query'),  # Alias pour compatibilité
    path('status/', views.chatbot_status, name='chatbot-status'),
    path('feedback/', views.chatbot_feedback, name='chatbot-feedback'),
    path('export-pdf/', views.chatbot_export_pdf, name='chatbot-export-pdf'),
]