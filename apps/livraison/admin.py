from django.contrib import admin
# from .models import Livraison

# Modèle Livraison supprimé de l'administration
# @admin.register(Livraison)
# class LivraisonAdmin(admin.ModelAdmin):
#     list_display = [
#         'numero_commande', 'type_commande', 'fournisseur', 'statut_livraison', 
#         'date_livraison_prevue', 'date_livraison_effective', 'conforme', 'pv_reception_recu'
#     ]
#     list_filter = [
#         'type_commande', 'statut_livraison', 'conforme', 'pv_reception_recu', 
#         'date_livraison_prevue', 'date_creation'
#     ]
#     search_fields = [
#         'numero_commande', 'fournisseur__nom', 'notes'
#     ]
#     readonly_fields = [
#         'numero_commande', 'type_commande', 'date_creation', 'date_modification'
#     ]
    
#     fieldsets = (
#         ('Informations de commande', {
#             'fields': ('numero_commande', 'type_commande', 'commande_informatique', 'commande_bureau')
#         }),
#         ('Informations de livraison', {
#             'fields': ('date_livraison_prevue', 'date_livraison_effective', 'statut_livraison', 'livreur')
#         }),
#         ('Conformité et réception', {
#             'fields': ('conforme', 'pv_reception_recu')
#         }),
#         ('Notes', {
#             'fields': ('notes',)
#         }),
#         ('Traçabilité', {
#             'fields': ('cree_par', 'modifie_par', 'date_creation', 'date_modification'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def save_model(self, request, obj, form, change):
#         if not change:  # Nouvelle livraison
#             obj.cree_par = request.user
#         else:  # Modification
#             obj.modifie_par = request.user
#         super().save_model(request, obj, form, change)
    
#     def get_queryset(self, request):
#         """Optimiser les requêtes avec select_related"""
#         return super().get_queryset(request).select_related(
#             'commande_informatique__fournisseur',
#             'commande_bureau__fournisseur',
#             'livreur',
#             'cree_par',
#             'modifie_par'
#         )
