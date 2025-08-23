from django.urls import path
from . import views

app_name = 'materiel_bureautique'

urlpatterns = [
    # URLs principales
    path('', views.liste_materiels, name='liste_materiels'),
    path('ajouter/', views.ajouter_materiel, name='ajouter_materiel'),
    path('modifier/<int:pk>/', views.modifier_materiel, name='modifier_materiel'),
    path('supprimer/<int:pk>/', views.supprimer_materiel, name='supprimer_materiel'),
    path('export-excel/', views.export_materiels_excel, name='export_excel'),
    path('mes-equipements/', views.mes_equipements_bureautiques, name='mes_equipements_bureautiques'),
    # URLs API
    path('api/lignes-commande/<int:commande_id>/', views.lignes_commande_par_commande, name='lignes_commande_par_commande'),
    
    # URLs superadmin
    path('superadmin/', views.liste_materiels_superadmin, name='liste_materiels_superadmin'),
    path('superadmin/ajouter/', views.ajouter_materiel_superadmin, name='ajouter_materiel_superadmin'),
    path('superadmin/modifier/<int:pk>/', views.modifier_materiel_superadmin, name='modifier_materiel_superadmin'),
    path('superadmin/supprimer/<int:pk>/', views.confirmer_suppression_superadmin, name='confirmer_suppression_superadmin'),
    path('superadmin/export_excel/', views.export_materiels_excel_superadmin, name='export_excel_superadmin'),
    
    # URLs gestionnaire info
    path('gestionnaire-info/', views.liste_materiels_gestionnaire_info, name='liste_materiels_gestionnaire_info'),
    
    # URLs gestionnaire bureau
    path('gestionnaire-bureau/', views.liste_materiels_gestionnaire_bureau, name='liste_materiels_gestionnaire_bureau'),
    path('gestionnaire-bureau/ajouter/', views.ajouter_materiel_gestionnaire_bureau, name='ajouter_materiel_gestionnaire_bureau'),
    path('gestionnaire-bureau/modifier/<int:pk>/', views.modifier_materiel_gestionnaire_bureau, name='modifier_materiel_gestionnaire_bureau'),
    path('gestionnaire-bureau/supprimer/<int:pk>/', views.confirmer_suppression_gestionnaire_bureau, name='confirmer_suppression_gestionnaire_bureau'),
] 