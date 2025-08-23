from django.urls import path
from . import views

app_name = 'fournisseurs'
urlpatterns = [
    path('', views.fournisseur_list, name='fournisseur_list'),
    path('ajouter/', views.fournisseur_form, name='fournisseur_create'),
    path('<int:pk>/modifier/', views.fournisseur_form, name='fournisseur_update'),
    path('<int:pk>/supprimer/', views.fournisseur_confirm_delete, name='fournisseur_delete'),
    path('exporter_excel/', views.exporter_fournisseurs_excel, name='exporter_excel'),
]