from django.urls import path
from . import views

app_name = 'commandes_bureau'

urlpatterns = [
    # URLs principales
    path('', views.liste_commandes, name='liste_commandes'),
    path('ajouter/', views.ajouter_commande, name='ajouter_commande'),
    path('modifier/<int:pk>/', views.modifier_commande, name='modifier_commande'),
    path('supprimer/<int:pk>/', views.supprimer_commande, name='supprimer_commande'),
    path('export-excel/', views.export_commandes_excel, name='export_excel'),
    
    # URLs API
    path('api/descriptions/<int:designation_id>/', views.get_descriptions, name='get_descriptions'),
    path('api/ajouter_fournisseur/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('api/ajouter_designation/', views.ajouter_designation, name='ajouter_designation'),
    path('api/ajouter_description/', views.ajouter_description, name='ajouter_description'),
] 