# Funcao: rotas da pagina inicial e recursos comuns do sistema.
# Responsável: Lucas sureira.

from django.urls import path
from . import views

# Define o nome do aplicativo para organização das URLs no Django
app_name = 'core'

urlpatterns = [
    # Rota raiz (ex: www.seusite.com/). Aciona a view de redirecionamento.
    path('', views.home_redirect, name='home_redirect'),
    
    # Rota para a página de suporte técnico/ajuda do sistema
    path('ajuda/', views.pagina_ajuda, name='ajuda'),
]
