from django.urls import path
from . import views

app_name = 'livraison'

urlpatterns = [
    # Vues principales
    path('', views.liste_livraisons, name='liste_livraisons'),
    path('nouvelle/', views.nouvelle_livraison, name='nouvelle_livraison'),
    path('<int:pk>/', views.detail_livraison, name='detail_livraison'),
    path('<int:pk>/modifier/', views.modifier_livraison, name='modifier_livraison'),
    path('<int:pk>/supprimer/', views.supprimer_livraison, name='supprimer_livraison'),
    
    # Actions sur les livraisons
    path('<int:pk>/marquer-livree/', views.marquer_livree, name='marquer_livree'),
    path('<int:pk>/valider-pv/', views.valider_pv_reception, name='valider_pv_reception'),
    
    # Rapports
    path('rapports/', views.rapports_livraison, name='rapports_livraison'),
    
    # API pour le formulaire dynamique
    path('api/commandes/', views.api_commandes, name='api_commandes'),
    path('api/commande/<int:commande_id>/', views.api_commande_details, name='api_commande_details'),
] 