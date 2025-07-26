from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def redirect_user(request):
    user = request.user
    groups = user.groups.values_list('name', flat=True)

    if 'Super Admin' in groups:
        return redirect('users:superadmin_dashboard')  # Add 'users:' prefix
    elif 'Gestionnaire Informatique' in groups:
        return redirect('users:gestionnaire_info_dashboard')  # Add 'users:' prefix
    elif 'Gestionnaire Bureau' in groups:
        return redirect('users:gestionnaire_bureau_dashboard')  # Add 'users:' prefix
    elif 'Employe' in groups:
        return redirect('users:employe_dashboard')  # Add 'users:' prefix
    else:
        return HttpResponseForbidden("Erreur : Vous n'avez pas les permissions nécessaires pour accéder à cette application.")

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