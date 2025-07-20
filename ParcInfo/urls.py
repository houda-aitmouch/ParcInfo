from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.users.urls')),

    path('accounts/', include('django.contrib.auth.urls')),

    # Inclure toutes les URLs liées à équipements ET matériel dans apps.equipements.urls
    path('', include('apps.equipements.urls', namespace='equiçpements')),
    path('materiel/', include(('apps.equipements.urls', 'materiel'), namespace='materiel')),
path('fournisseurs/', include(('apps.fournisseur.urls', 'fournisseur'), namespace='fournisseur')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)