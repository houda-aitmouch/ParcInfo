from django.urls import path, reverse
from django.shortcuts import redirect
from . import views
from .views import custom_logout_view

app_name = 'users'

urlpatterns = [
    path('', lambda request: redirect('users:redirect_user'), name='root'),  # Add 'users:' prefix
    path('redirect-user/', views.redirect_user, name='redirect_user'),
    path('superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin-debug/', views.superadmin_dashboard_debug, name='superadmin_dashboard_debug'),
    path('gestionnaire_info/', views.gestionnaire_info_dashboard, name='gestionnaire_info_dashboard'),
    path('gestionnaire_bureau/', views.gestionnaire_bureau_dashboard, name='gestionnaire_bureau_dashboard'),
    path('employe/', views.employe_dashboard, name='employe_dashboard'),
    path('logout/', custom_logout_view, name='logout'),
    path('profil/', views.profil, name='profil'),
    path('dashboard-garantie/', views.dashboard_garantie, name='dashboard_garantie'),
    path('search/', views.global_search, name='global_search'),
    path('notifications/garanties/', views.warranty_notifications_json, name='warranty_notifications_json'),
    path('notifications-garantie/', views.notifications_garantie, name='notifications_garantie'),
]