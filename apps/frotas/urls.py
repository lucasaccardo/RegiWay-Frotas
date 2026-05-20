# Funcao: rotas de clientes, veiculos, motoristas e consultas da frota.
# Responsável: Kenzo.

from django.urls import path

from . import views

app_name = "frotas"

urlpatterns = [
    path("", views.veiculos_list, name="veiculos_list"),
    path("novo/", views.veiculo_novo, name="veiculo_novo"),
    path("<int:pk>/editar/", views.veiculo_editar, name="veiculo_editar"),
]
