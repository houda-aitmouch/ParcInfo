from django.contrib import admin
from .models import DemandeEquipement, Fourniture, ArchiveDecharge

# Suppression de tous les enregistrements admin pour masquer l'app de l'interface
# @admin.register(DemandeEquipement)
# class DemandeEquipementAdmin(admin.ModelAdmin):
#     list_display = ['id', 'demandeur', 'categorie', 'type_article', 'statut', 'date_demande']
#     list_filter = ['categorie', 'type_article', 'statut', 'date_demande', 'decharge_signee']
#     search_fields = ['id', 'demandeur__username', 'demandeur__first_name', 'demandeur__last_name']
#     readonly_fields = ['id', 'date_demande', 'date_approbation', 'date_affectation']
#     ordering = ['-date_demande']
#     
#     fieldsets = (
#         ('Informations de base', {
#             'fields': ('id', 'demandeur', 'categorie', 'type_article', 'type_demande')
#         }),
#         ('Détails de la demande', {
#             'fields': ('designation_info', 'description_info', 'designation_bureau', 'description_bureau', 'fourniture')
#         }),
#         ('Statut et approbation', {
#             'fields': ('statut', 'approuve_par', 'decharge_signee', 'date_signature', 'signature_image')
#         }),
#         ('Affectation', {
#             'fields': ('date_affectation', 'materiel_selectionne_id')
#         }),
#         ('Dates', {
#             'fields': ('date_demande', 'date_approbation'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(Fourniture)
# class FournitureAdmin(admin.ModelAdmin):
#     list_display = ['nom', 'numero_serie', 'type', 'actif', 'date_creation']
#     list_filter = ['type', 'actif', 'date_creation']
#     search_fields = ['nom', 'numero_serie']
#     readonly_fields = ['date_creation', 'date_modification']
#     ordering = ['nom']
#     
#     fieldsets = (
#         ('Informations de base', {
#             'fields': ('nom', 'numero_serie', 'type')
#         }),
#         ('Statut', {
#             'fields': ('actif',)
#         }),
#         ('Dates', {
#             'fields': ('date_creation', 'date_modification'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(ArchiveDecharge)
# class ArchiveDechargeAdmin(admin.ModelAdmin):
#     list_display = ['numero_archive', 'demande', 'date_archivage', 'archive_par', 'statut_archive']
#     list_filter = ['statut_archive', 'date_archivage']
#     search_fields = ['numero_archive', 'demande__demandeur__username']
#     readonly_fields = ['numero_archive', 'date_archivage']
#     ordering = ['-date_archivage']
