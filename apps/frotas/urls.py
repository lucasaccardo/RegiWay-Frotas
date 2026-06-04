# Funcao: rotas de listagem, cadastro e edicao de veiculos da frota.
# Responsável: Kenzo.

from django.urls import path

from . import views

app_name = 'frotas'

urlpatterns = [
    path('veiculos/', views.veiculos_list, name='veiculos_list'),
    path('veiculos/novo/', views.veiculo_novo, name='veiculo_novo'),
    path('veiculos/<int:pk>/editar/', views.veiculo_editar, name='veiculo_editar'),
]
