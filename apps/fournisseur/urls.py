from django.urls import path
from . import views

urlpatterns = [
    path('', views.fournisseur_list, name='fournisseur_list'),
    path('ajouter/', views.fournisseur_create, name='fournisseur_create'),
    path('<int:fournisseur_id>/modifier/', views.fournisseur_update, name='fournisseur_update'),
    path('<int:fournisseur_id>/supprimer/', views.fournisseur_delete, name='fournisseur_delete'),
]