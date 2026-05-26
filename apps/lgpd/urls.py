# Funcao: rotas de termos, meus dados, exclusao, portabilidade e privacidade.
# Responsável: Lucas Sureira, Pacheco.

from django.urls import path
from . import views

app_name = 'lgpd'

urlpatterns = [
    # Pacheco: Política de privacidade (pública) e aceite obrigatório de termos
    path('politica-privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('aceite-termos/', views.aceite_termos, name='aceite_termos'),

    # Lucas: Painel de dados do usuário
    path('meus-dados/', views.meus_dados, name='meus_dados'),
    path('baixar-dados/', views.baixar_meus_dados, name='baixar_dados'),
    path('excluir-conta/', views.confirmar_exclusao, name='confirmar_exclusao'),
]
