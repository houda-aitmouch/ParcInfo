from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import requests
import logging

logger = logging.getLogger(__name__)

def get_user_dashboard_url(user):
    """Retourne l'URL du dashboard approprié selon le type d'utilisateur"""
    if user.is_superuser:
        return 'users:superadmin_dashboard'
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        return 'users:gestionnaire_info_dashboard'
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        return 'users:gestionnaire_bureau_dashboard'
    else:
        return 'users:employe_dashboard'

@login_required
def redirect_user(request):
    user = request.user
    
    # Utiliser les groupes Django par défaut
    if user.is_superuser:
        return redirect('users:superadmin_dashboard')
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        return redirect('users:gestionnaire_info_dashboard')
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        return redirect('users:gestionnaire_bureau_dashboard')
    else:
        return redirect('users:employe_dashboard')

@login_required
def superadmin_dashboard(request):
    return render(request, 'dashboards/superadmin.html')

@login_required
def gestionnaire_info_dashboard(request):
    return render(request, 'dashboards/gestionnaire_info.html')

@login_required
def gestionnaire_bureau_dashboard(request):
    return render(request, 'dashboards/gestionnaire_bureau.html')

@login_required
def employe_dashboard(request):
    return render(request, 'dashboards/employe.html')

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Make sure you have a 'login' URL name defined

@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})

@login_required
def profil(request):
    """Vue du profil utilisateur"""
    return render(request, 'users/profile.html')

@login_required
def dashboard_garantie(request):
    """Redirection vers le dashboard de garantie Streamlit"""
    # Vérifier les permissions de l'utilisateur
    user = request.user
    
    # Seuls les Super Admin, Gestionnaire Informatique et Gestionnaire Bureau peuvent accéder
    if not (user.is_superuser or 
            user.groups.filter(name='Gestionnaire Informatique').exists() or 
            user.groups.filter(name='Gestionnaire Bureau').exists()):
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires pour accéder au Dashboard de Garanties.')
        return redirect('users:profil')
    
    try:
        # Vérifier si le dashboard Streamlit est accessible
        response = requests.get('http://localhost:8501', timeout=5)
        if response.status_code == 200:
            # Passer l'utilisateur connecté en paramètre
            username = request.user.username
            # Encoder le nom d'utilisateur pour l'URL (gérer les espaces et caractères spéciaux)
            import urllib.parse
            encoded_username = urllib.parse.quote(username)
            streamlit_url = f'http://localhost:8501/?username={encoded_username}'
            logger.info(f"Redirection vers Streamlit avec utilisateur: {username} (encodé: {encoded_username})")
            return redirect(streamlit_url)
        else:
            messages.error(request, 'Le dashboard de garantie n\'est pas accessible. Veuillez le démarrer.')
            return redirect('users:profil')
    except requests.exceptions.RequestException as e:
        logger.warning(f"Dashboard de garantie non accessible: {e}")
        messages.warning(
            request,
            'Le dashboard de garantie n\'est pas démarré. '
            'Pour l\'utiliser, lancez la commande: python launch_dashboard.py'
        )
        return redirect('users:profil')

@require_http_methods(["POST"])
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')