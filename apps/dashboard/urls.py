# Funcao: rotas do painel principal e telas gerenciais.
# Responsável: Matheus Deleutério.

from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
]
