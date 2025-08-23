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
    path('export-excel/', views.export_livraisons_excel, name='export_livraisons_excel'),
    
    # API pour le formulaire dynamique
    path('api/commandes/', views.api_commandes, name='api_commandes'),
    path('api/commande/<int:commande_id>/', views.api_commande_details, name='api_commande_details'),

    # Superadmin URLs
    path('superadmin/liste/', views.liste_livraisons_superadmin, name='liste_livraisons_superadmin'),
    path('superadmin/nouvelle/', views.nouvelle_livraison_superadmin, name='nouvelle_livraison_superadmin'),
    path('superadmin/<int:pk>/', views.detail_livraison_superadmin, name='detail_livraison_superadmin'),
    path('superadmin/<int:pk>/modifier/', views.modifier_livraison_superadmin, name='modifier_livraison_superadmin'),
    path('superadmin/<int:pk>/marquer-livree/', views.marquer_livree_superadmin, name='marquer_livree_superadmin'),
    path('superadmin/<int:pk>/valider-pv/', views.valider_pv_reception_superadmin, name='valider_pv_reception_superadmin'),
    path('superadmin/<int:pk>/supprimer/', views.supprimer_livraison_superadmin, name='supprimer_livraison_superadmin'),
    path('superadmin/rapports/', views.rapports_livraison_superadmin, name='rapports_livraison_superadmin'),
    path('superadmin/export-excel/', views.export_livraisons_excel_superadmin, name='export_livraisons_excel_superadmin'),
    
    # URLs gestionnaire info
    path('gestionnaire-info/liste/', views.liste_livraisons_gestionnaire_info, name='liste_livraisons_gestionnaire_info'),
    path('gestionnaire-info/nouvelle/', views.nouvelle_livraison_gestionnaire_info, name='nouvelle_livraison_gestionnaire_info'),
    path('gestionnaire-info/<int:pk>/', views.detail_livraison_gestionnaire_info, name='detail_livraison_gestionnaire_info'),
    path('gestionnaire-info/<int:pk>/modifier/', views.modifier_livraison_gestionnaire_info, name='modifier_livraison_gestionnaire_info'),
    path('gestionnaire-info/<int:pk>/marquer-livree/', views.marquer_livree_gestionnaire_info, name='marquer_livree_gestionnaire_info'),
    path('gestionnaire-info/<int:pk>/valider-pv/', views.valider_pv_reception_gestionnaire_info, name='valider_pv_reception_gestionnaire_info'),
    path('gestionnaire-info/<int:pk>/supprimer/', views.supprimer_livraison_gestionnaire_info, name='supprimer_livraison_gestionnaire_info'),
    path('gestionnaire-info/rapports/', views.rapports_livraison_gestionnaire_info, name='rapports_livraison_gestionnaire_info'),
    path('gestionnaire-info/export-excel/', views.export_livraisons_excel_gestionnaire_info, name='export_livraisons_excel_gestionnaire_info'),
    
    # URLs gestionnaire bureau
    path('gestionnaire-bureau/liste/', views.liste_livraisons_gestionnaire_bureau, name='liste_livraisons_gestionnaire_bureau'),
    path('gestionnaire-bureau/nouvelle/', views.nouvelle_livraison_gestionnaire_bureau, name='nouvelle_livraison_gestionnaire_bureau'),
    path('gestionnaire-bureau/<int:pk>/', views.detail_livraison_gestionnaire_bureau, name='detail_livraison_gestionnaire_bureau'),
    path('gestionnaire-bureau/<int:pk>/modifier/', views.modifier_livraison_gestionnaire_bureau, name='modifier_livraison_gestionnaire_bureau'),
    path('gestionnaire-bureau/<int:pk>/marquer-livree/', views.marquer_livree_gestionnaire_bureau, name='marquer_livree_gestionnaire_bureau'),
    path('gestionnaire-bureau/<int:pk>/valider-pv/', views.valider_pv_reception_gestionnaire_bureau, name='valider_pv_reception_gestionnaire_bureau'),
    path('gestionnaire-bureau/<int:pk>/supprimer/', views.supprimer_livraison_gestionnaire_bureau, name='supprimer_livraison_gestionnaire_bureau'),
    path('gestionnaire-bureau/rapports/', views.rapports_livraison_gestionnaire_bureau, name='rapports_livraison_gestionnaire_bureau'),
    path('gestionnaire-bureau/export-excel/', views.export_livraisons_excel_gestionnaire_bureau, name='export_livraisons_excel_gestionnaire_bureau'),
    

] 