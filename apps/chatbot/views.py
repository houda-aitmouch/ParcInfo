from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.db import transaction
import json
import uuid

from .forms import ChatForm
from .models import ChatMessage
from .llm_engine import ParcInfoChatbot

User = get_user_model()

# Instance globale du chatbot
chatbot = None

def get_chatbot():
    """Obtenir l'instance du chatbot (singleton)"""
    global chatbot
    if chatbot is None:
        chatbot = ParcInfoChatbot()
    return chatbot

def check_manager_access(user):
    """Vérifier que l'utilisateur a accès au chatbot (gestionnaire ou superadmin)"""
    return user.is_superuser or user.is_staff

@login_required
def chat_interface(request):
    """Interface principale du chatbot - Accès réservé aux gestionnaires"""
    # Vérifier que l'utilisateur est gestionnaire ou superadmin
    if not check_manager_access(request.user):
        messages.error(request, "Le chatbot IA est réservé aux gestionnaires et administrateurs.")
        return redirect('home')
    
    form = ChatForm()
    
    # Récupérer l'historique des conversations de l'utilisateur
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')[:10]
    
    # Obtenir les insights d'apprentissage du chatbot
    bot = get_chatbot()
    learning_insights = bot.get_learning_insights()
    
    context = {
        'form': form,
        'chat_history': chat_history,
        'user': request.user,
        'learning_insights': learning_insights,
        'user_role': 'Super Admin' if request.user.is_superuser else 'Gestionnaire'
    }
    
    return render(request, 'chatbot/chat_interface.html', context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API pour les requêtes de chat - Accès réservé aux gestionnaires"""
    try:
        # Vérifier les permissions
        if not check_manager_access(request.user):
            return JsonResponse({
                'error': 'Accès non autorisé - Réservé aux gestionnaires'
            }, status=403)
        
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'error': 'Message vide'
            }, status=400)
        
        # Obtenir le chatbot
        bot = get_chatbot()
        
        # Générer une réponse avec l'IA
        response = bot.get_response(message, request.user)
        
        # Sauvegarder la conversation
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        with transaction.atomic():
            ChatMessage.objects.create(
                user=request.user,
                message=message,
                response=response,
                session_id=session_id
            )
        
        return JsonResponse({
            'response': response,
            'session_id': session_id,
            'timestamp': ChatMessage.objects.latest('id').timestamp.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Données JSON invalides'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)

@login_required
def chat_history(request):
    """Afficher l'historique des conversations - Accès réservé aux gestionnaires"""
    # Vérifier les permissions
    if not check_manager_access(request.user):
        messages.error(request, "Accès non autorisé - Réservé aux gestionnaires.")
        return redirect('home')
    
    # Récupérer l'historique complet
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')
    
    context = {
        'chat_history': chat_history,
        'user': request.user,
        'user_role': 'Super Admin' if request.user.is_superuser else 'Gestionnaire'
    }
    
    return render(request, 'chatbot/chat_history.html', context)

@login_required
def clear_history(request):
    """Effacer l'historique des conversations - Accès réservé aux gestionnaires"""
    # Vérifier les permissions
    if not check_manager_access(request.user):
        messages.error(request, "Accès non autorisé - Réservé aux gestionnaires.")
        return redirect('home')
    
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
        messages.success(request, "Historique des conversations effacé.")
        return redirect('chatbot:chat_interface')
    
    return render(request, 'chatbot/clear_history_confirm.html')

@login_required
def chatbot_help(request):
    """Page d'aide pour le chatbot - Accès réservé aux gestionnaires"""
    # Vérifier les permissions
    if not check_manager_access(request.user):
        messages.error(request, "Accès non autorisé - Réservé aux gestionnaires.")
        return redirect('home')
    
    help_content = {
        'title': 'Aide - Assistant IA ParcInfo',
        'sections': [
            {
                'title': 'Utilisation de l\'assistant IA',
                'content': [
                    'Posez vos questions en français naturel',
                    'L\'assistant utilise LLaMA 3 pour comprendre et répondre',
                    'Il accède aux données système en temps réel',
                    'Il s\'améliore continuellement grâce à l\'apprentissage',
                    'Il fournit des insights et recommandations'
                ]
            },
            {
                'title': 'Exemples de questions techniques',
                'content': [
                    '"Analyser les tendances des demandes d\'équipement"',
                    '"Quel est le taux d\'approbation des demandes ?"',
                    '"Identifier les goulots d\'étranglement dans le processus"',
                    '"Optimiser la gestion du stock de matériel"',
                    '"Générer un rapport de performance du système"',
                    '"Analyser l\'utilisation des équipements"',
                    '"Suggérer des améliorations du workflow"'
                ]
            },
            {
                'title': 'Fonctionnalités avancées',
                'content': [
                    'Analytics système en temps réel',
                    'Insights basés sur les données',
                    'Recommandations d\'optimisation',
                    'Analyse des tendances',
                    'Rapports de performance',
                    'Apprentissage continu',
                    'Contexte utilisateur personnalisé'
                ]
            },
            {
                'title': 'Technologie IA utilisée',
                'content': [
                    'LLaMA 3 - Modèle de langage avancé',
                    'LangChain - Framework d\'IA conversationnelle',
                    'Apprentissage continu et adaptatif',
                    'Analyse sémantique avancée',
                    'Contexte système enrichi',
                    'Vectorstore pour la recherche intelligente'
                ]
            },
            {
                'title': 'Rôles et permissions',
                'content': [
                    'Super Admin: Accès complet et insights système',
                    'Gestionnaire Informatique: Focus sur le matériel informatique',
                    'Gestionnaire Bureau: Focus sur le matériel bureautique',
                    'Chaque rôle reçoit des réponses adaptées',
                    'Contexte personnalisé selon les responsabilités'
                ]
            }
        ]
    }
    
    context = {
        'help_content': help_content,
        'user': request.user,
        'user_role': 'Super Admin' if request.user.is_superuser else 'Gestionnaire'
    }
    
    return render(request, 'chatbot/help.html', context)

@login_required
def refresh_chatbot(request):
    """Rafraîchir le contexte du chatbot (pour les administrateurs)"""
    if not request.user.is_superuser:
        messages.error(request, "Accès non autorisé - Réservé aux Super Admin.")
        return redirect('home')
    
    try:
        bot = get_chatbot()
        bot.refresh_context()
        messages.success(request, "Contexte du chatbot IA rafraîchi avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors du rafraîchissement: {str(e)}")
    
    return redirect('admin:index')

@login_required
def learning_insights(request):
    """Afficher les insights d'apprentissage du chatbot"""
    if not check_manager_access(request.user):
        messages.error(request, "Accès non autorisé - Réservé aux gestionnaires.")
        return redirect('home')
    
    try:
        bot = get_chatbot()
        insights = bot.get_learning_insights()
        
        context = {
            'insights': insights,
            'user': request.user,
            'user_role': 'Super Admin' if request.user.is_superuser else 'Gestionnaire'
        }
        
        return render(request, 'chatbot/learning_insights.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la récupération des insights: {str(e)}")
        return redirect('chatbot:chat_interface') 