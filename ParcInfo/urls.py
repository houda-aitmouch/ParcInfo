from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Ajoutez cette route si vous avez besoin d'un service worker
from django.views.generic import TemplateView
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

def login_login_redirect(request):
    """Redirige /login/login/ vers /accounts/login/"""
    return redirect('/accounts/login/')

urlpatterns = [
    path('login/login/', login_login_redirect, name='login_login_redirect'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.users.urls')),
    path('health', health),

    path('fournisseurs/', include('apps.fournisseurs.urls', namespace='fournisseurs')),
    path('commande-informatique/', include('apps.commande_informatique.urls', namespace='commandes_informatique')),
    path('commande-bureau/', include('apps.commande_bureau.urls', namespace='commandes_bureau')),
    path('materiels/', include('apps.materiel_informatique.urls', namespace='materiel_informatique')),
    path('materiels-bureau/', include('apps.materiel_bureautique.urls', namespace='materiel_bureautique')),
    path('demandes/', include('apps.demande_equipement.urls', namespace='demande_equipement')),
    path('livraisons/', include('apps.livraison.urls', namespace='livraison')),
    path('chatbot/', include('apps.chatbot.urls', namespace='chatbot')),
]

# Configuration des fichiers statiques - Version simplifiée
if settings.DEBUG:
    # En mode développement, servir depuis le dossier static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # En production, servir depuis STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Only expose service worker in non-debug environments
    urlpatterns += [
        re_path(r'^sw\.js$', TemplateView.as_view(
            template_name='sw.js',
            content_type='application/javascript'
        )),
        re_path(r'^sw\.js/$', TemplateView.as_view(
            template_name='sw.js',
            content_type='application/javascript'
        )),
    ]