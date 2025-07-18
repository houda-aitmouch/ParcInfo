from django.urls import path
from . import views

app_name = 'equipements'

urlpatterns = [
    # URLs équipements
    path('equipements/', views.equipement_list, name='equipement_list'),
    path('equipements/ajouter/', views.equipement_create, name='equipement_create'),
    path('equipements/<int:pk>/modifier/', views.equipement_update, name='equipement_update'),
    path('equipements/<int:pk>/supprimer/', views.equipement_delete, name='equipement_delete'),
    path('equipements/export-excel/', views.export_excel_equipement, name='export_excel_equipement'),

    # URLs matériel bureau
    path('materiel/', views.materiel_list, name='materiel_list'),
    path('materiel/ajouter/', views.materiel_create, name='materiel_create'),
    path('materiel/<int:materiel_id>/modifier/', views.materiel_update, name='materiel_update'),
    path('materiel/<int:materiel_id>/supprimer/', views.materiel_delete, name='materiel_delete'),
    path('materiel/export-excel/', views.export_excel_materiel, name='export_excel_materiel'),
]