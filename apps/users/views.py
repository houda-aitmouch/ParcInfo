from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect

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