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
        return redirect('superadmin_dashboard')
    elif 'Gestionnaire Informatique' in groups:
        return redirect('gestionnaire_info_dashboard')
    elif 'Gestionnaire Bureau' in groups:
        return redirect('gestionnaire_bureau_dashboard')
    elif 'Employe' in groups:
        return redirect('employe_dashboard')
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
    return redirect('login')