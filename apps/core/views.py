# Funcao: views comuns, pagina inicial e controle de layout base.
# Responsável: Lucas sureira.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    """
    Ponto de entrada inicial do site.
    Se o usuário já estiver logado, joga ele direto para o Dashboard.
    Se não estiver logado, redireciona para a tela de login.
    """
    if request.user.is_authenticated:
        # Redireciona para o app de dashboard (área do Matheus)
        return redirect('dashboard:index')
    else:
        # Redireciona para a tela de login (área do Kenzo)
        return redirect('accounts:login')


@login_required
def pagina_ajuda(request):
    """
    Uma página simples de suporte global para os usuários do sistema,
    explicando brevemente as regras de SLA e os prazos de sinistros.
    """
    # Renderiza o HTML de ajuda técnica do sistema
    return render(request, 'core/ajuda.html')
