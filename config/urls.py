# Funcao: roteador principal do projeto; inclui admin e URLs dos apps internos.
# Responsável: João Pedro.

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('contas/', include('apps.accounts.urls')),
    path('frotas/', include('apps.frotas.urls')),
    path('sinistros/', include('apps.sinistros.urls')),
    path('lgpd/', include('apps.lgpd.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
