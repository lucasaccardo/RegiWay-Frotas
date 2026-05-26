# Funcao: rotas de lista, detalhe, novo sinistro, historico e anexos.
# Responsável: Lucas sureira.

from django.urls import path
from . import views

app_name = 'sinistros'

urlpatterns = [
    path('', views.lista_sinistros, name='lista_sinistros'),
    path('novo/', views.novo_sinistro, name='novo_sinistro'),
    path('<int:pk>/', views.detail_sinistro, name='detail_sinistro'),
    path('<int:pk>/historico/', views.historico_sinistro, name='historico_sinistro'),
]
