from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('history/', views.chat_history, name='chat_history'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('help/', views.chatbot_help, name='help'),
    path('insights/', views.learning_insights, name='learning_insights'),
] 