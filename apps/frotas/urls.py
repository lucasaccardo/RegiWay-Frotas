# Funcao: rotas de clientes, veiculos, motoristas e consultas da frota.
# Responsável: Kenzo.
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("apps.accounts.urls", "two_factor"), namespace="two_factor")),
    path("frotas/", include("apps.frotas.urls")),
]
