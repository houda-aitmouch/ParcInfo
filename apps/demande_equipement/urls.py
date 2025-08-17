from django.urls import path
from . import views

app_name = 'demande_equipement'

urlpatterns = [
    # URLs pour les utilisateurs
    path('', views.liste_demandes, name='liste_demandes'),
    path('nouvelle/', views.nouvelle_demande, name='nouvelle_demande'),
    path('modifier/<int:pk>/', views.modifier_demande, name='modifier_demande'),
    path('supprimer/<int:pk>/', views.supprimer_demande, name='supprimer_demande'),
    
    # URLs pour les gestionnaires
    path('toutes/', views.liste_toutes_demandes, name='liste_toutes_demandes'),
    path('approuver/<int:pk>/', views.approuver_demande, name='approuver_demande'),
    
    # APIs pour les champs dépendants
    path('api/designations/', views.get_designations, name='get_designations'),
    path('api/descriptions/', views.get_descriptions, name='get_descriptions'),
    path('api/fournitures/', views.get_fournitures, name='get_fournitures'),
    path('api/ajouter-fourniture/', views.ajouter_fourniture, name='ajouter_fourniture'),
    
    # Signature de décharge
    path('signer-decharge/<int:pk>/', views.signer_decharge, name='signer_decharge'),
    
    # Viewer PDF
    path('viewer-pdf/<int:pk>/', views.viewer_pdf, name='viewer_pdf'),
    
    # Téléchargement PDF
    path('decharge/<int:pk>/', views.telecharger_decharge, name='telecharger_decharge'),
    
    # URL pour l'archivage électronique unifié
    path('archives/', views.consulter_archives, name='consulter_archives'),
    path('archives/telecharger/<int:archive_id>/', views.telecharger_archive, name='telecharger_archive'),
] 