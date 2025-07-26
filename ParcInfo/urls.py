from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.users.urls')),

    path('fournisseurs/', include('apps.fournisseurs.urls', namespace='fournisseurs')),
    path('commande-informatique/', include(('apps.commande_informatique.urls', 'commandes_informatique'), namespace='commandes_informatique')),
    path('commande-bureau/', include(('apps.commande_bureau.urls', 'commandes_bureau'), namespace='commandes_bureau')),
    path('materiels/', include('apps.materiel_informatique.urls', namespace='materiel_informatique')),
    path('materiels-bureau/', include('apps.materiel_bureautique.urls', namespace='materiel_bureautique')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)