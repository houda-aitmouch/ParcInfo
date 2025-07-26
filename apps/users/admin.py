from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe


class CustomUserAdmin(BaseUserAdmin):
    """Configuration admin personnalisée pour les utilisateurs"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'get_groups', 'get_permissions_summary')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )
    
    def get_groups(self, obj):
        """Affiche les groupes de l'utilisateur avec des couleurs"""
        groups = obj.groups.all()
        if not groups:
            return format_html('<span style="color: #999;">Aucun groupe</span>')
        
        group_colors = {
            'Super Admin': '#dc3545',
            'Gestionnaire Informatique': '#007bff',
            'Gestionnaire Bureau': '#28a745',
            'Employe': '#ffc107'
        }
        
        group_links = []
        for group in groups:
            color = group_colors.get(group.name, '#6c757d')
            group_links.append(
                f'<span style="color: {color}; font-weight: bold;">{group.name}</span>'
            )
        
        return mark_safe(' | '.join(group_links))
    get_groups.short_description = 'Groupes'
    
    def get_permissions_summary(self, obj):
        """Affiche un résumé des permissions de l'utilisateur"""
        if obj.is_superuser:
            return format_html('<span style="color: #dc3545; font-weight: bold;">Toutes les permissions</span>')
        
        permissions = obj.user_permissions.all()
        group_permissions = set()
        for group in obj.groups.all():
            group_permissions.update(group.permissions.all())
        
        all_permissions = list(permissions) + list(group_permissions)
        
        if not all_permissions:
            return format_html('<span style="color: #999;">Aucune permission</span>')
        
        # Compter les permissions par app
        app_permissions = {}
        for perm in all_permissions:
            app = perm.content_type.app_label
            if app not in app_permissions:
                app_permissions[app] = 0
            app_permissions[app] += 1
        
        summary = []
        for app, count in app_permissions.items():
            if count > 0:
                summary.append(f'{app}: {count}')
        
        return format_html('<span style="color: #28a745;">{}</span>', ' | '.join(summary))
    get_permissions_summary.short_description = 'Résumé des permissions'


class CustomGroupAdmin(BaseGroupAdmin):
    """Configuration admin personnalisée pour les groupes"""
    
    list_display = ('name', 'get_members_count', 'get_permissions_summary', 'get_app_permissions')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_members_count(self, obj):
        """Affiche le nombre de membres du groupe"""
        count = obj.user_set.count()
        return format_html('<span style="color: #007bff; font-weight: bold;">{} membre(s)</span>', count)
    get_members_count.short_description = 'Membres'
    
    def get_permissions_summary(self, obj):
        """Affiche un résumé des permissions du groupe"""
        permissions = obj.permissions.all()
        if not permissions:
            return format_html('<span style="color: #999;">Aucune permission</span>')
        
        # Compter les permissions par type
        permission_types = {}
        for perm in permissions:
            action = perm.codename.split('_')[0] if '_' in perm.codename else perm.codename
            if action not in permission_types:
                permission_types[action] = 0
            permission_types[action] += 1
        
        summary = []
        for action, count in permission_types.items():
            if count > 0:
                summary.append(f'{action}: {count}')
        
        return format_html('<span style="color: #28a745;">{}</span>', ' | '.join(summary))
    get_permissions_summary.short_description = 'Types de permissions'
    
    def get_app_permissions(self, obj):
        """Affiche les permissions par application"""
        permissions = obj.permissions.all()
        if not permissions:
            return format_html('<span style="color: #999;">Aucune permission</span>')
        
        # Grouper par application
        app_permissions = {}
        for perm in permissions:
            app = perm.content_type.app_label
            model = perm.content_type.model
            if app not in app_permissions:
                app_permissions[app] = {}
            if model not in app_permissions[app]:
                app_permissions[app][model] = []
            app_permissions[app][model].append(perm.codename)
        
        # Créer les liens vers les permissions
        app_links = []
        for app, models in app_permissions.items():
            model_links = []
            for model, perms in models.items():
                perm_names = [p.replace('_', ' ').title() for p in perms]
                model_links.append(f'{model}: {", ".join(perm_names)}')
            
            app_color = {
                'commande_informatique': '#007bff',
                'commande_bureau': '#28a745',
                'materiel_informatique': '#ffc107',
                'materiel_bureautique': '#dc3545',
                'fournisseurs': '#6f42c1',
                'users': '#17a2b8'
            }.get(app, '#6c757d')
            
            app_links.append(
                f'<span style="color: {app_color}; font-weight: bold;">{app}</span>: '
                f'<span style="color: #666;">{"; ".join(model_links)}</span>'
            )
        
        return mark_safe('<br>'.join(app_links))
    get_app_permissions.short_description = 'Permissions par application'


# Désenregistrer les classes admin par défaut
admin.site.unregister(User)
admin.site.unregister(Group)

# Enregistrer les classes admin personnalisées
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)


# Configuration du site admin
admin.site.site_header = "Administration ParcInfo"
admin.site.site_title = "ParcInfo Admin"
admin.site.index_title = "Gestion du Parc Informatique et Bureautique"
