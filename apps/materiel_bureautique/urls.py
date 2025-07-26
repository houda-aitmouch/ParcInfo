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
    # URLs API
    path('api/lignes-commande/<int:commande_id>/', views.lignes_commande_par_commande, name='lignes_commande_par_commande'),
] 