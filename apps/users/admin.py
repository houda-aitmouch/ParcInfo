from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from .models import CustomUser, NotificationDemande

# Désenregistrer le modèle Group de l'admin par défaut
admin.site.unregister(Group)

# Réenregistrer avec une configuration personnalisée
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    """Administration personnalisée des groupes d'utilisateurs"""
    
    # Personnaliser l'affichage de la liste
    list_display = ['name', 'get_user_count', 'get_permissions_count']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']
    
    # Personnaliser les champs d'édition
    fieldsets = (
        ('Informations du groupe', {
            'fields': ('name',)
        }),
        ('Permissions', {
            'fields': ('permissions',),
            'classes': ('collapse',),
            'description': 'Sélectionnez les permissions accordées à ce groupe'
        }),
    )
    
    def get_user_count(self, obj):
        """Afficher le nombre d'utilisateurs dans le groupe"""
        return obj.user_set.count()
    get_user_count.short_description = 'Nombre d\'utilisateurs'
    get_user_count.admin_order_field = 'user_count'
    
    def get_permissions_count(self, obj):
        """Afficher le nombre de permissions du groupe"""
        return obj.permissions.count()
    get_permissions_count.short_description = 'Nombre de permissions'
    get_permissions_count.admin_order_field = 'permissions_count'
    
    def get_queryset(self, request):
        """Optimiser les requêtes avec select_related et annotate"""
        from django.db.models import Count
        return super().get_queryset(request).annotate(
            user_count=Count('user'),
            permissions_count=Count('permissions')
        )

# Administration des utilisateurs personnalisés
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administration personnalisée des utilisateurs"""
    
    model = CustomUser
    
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'get_groups')
    
    # Filtres disponibles
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined', 'groups')
    
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
    
    def get_groups(self, obj):
        """Afficher les groupes de l'utilisateur"""
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groupes'
    get_groups.admin_order_field = 'groups__name'

# Personnaliser l'affichage de l'admin
admin.site.site_header = "Administration ParcInfo"
admin.site.site_title = "ParcInfo Admin"
admin.site.index_title = "Gestion du parc informatique"

@admin.register(NotificationDemande)
class NotificationDemandeAdmin(admin.ModelAdmin):
    """Administration des notifications de demandes"""
    
    list_display = ['utilisateur', 'type_notification', 'titre', 'statut_demande', 'lu', 'date_creation']
    list_filter = ['type_notification', 'statut_demande', 'lu', 'date_creation']
    search_fields = ['utilisateur__username', 'utilisateur__email', 'titre', 'message']
    ordering = ['-date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('utilisateur', 'type_notification', 'titre', 'message')
        }),
        ('Statut de la demande', {
            'fields': ('statut_demande', 'demande_id')
        }),
        ('État de la notification', {
            'fields': ('lu', 'date_lecture')
        }),
    )
    
    readonly_fields = ['date_creation']
    
    def get_queryset(self, request):
        """Optimiser les requêtes"""
        return super().get_queryset(request).select_related('utilisateur')
    
    def save_model(self, request, obj, form, change):
        """Logique personnalisée lors de la sauvegarde"""
        if change and 'lu' in form.changed_data and obj.lu:
            from django.utils import timezone
            obj.date_lecture = timezone.now()
        super().save_model(request, obj, form, change) 