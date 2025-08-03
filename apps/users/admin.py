from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

# Désenregistrer le modèle Group de l'admin par défaut
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    """Admin personnalisé pour les groupes"""
    
    class Meta:
        app_label = 'users'
        verbose_name = 'Groupe'
        verbose_name_plural = 'Groupes'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    
    # Filtres disponibles
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    
    # Champs de recherche
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Tri par défaut
    ordering = ('-date_joined',)
    
    # Champs dans le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Champs dans le formulaire d'ajout
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

# Personnaliser l'affichage de l'admin
admin.site.site_header = "Administration ParcInfo"
admin.site.site_title = "ParcInfo Admin"
admin.site.index_title = "Gestion du parc informatique" 