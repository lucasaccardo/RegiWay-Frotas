# Funcao: mixins reutilizaveis para views, forms e regras comuns.
# Responsável: Lucas sureira.

from django.contrib.auth.mixins import LoginRequiredMixin

class AutenticacaoObrigatoriaMixin(LoginRequiredMixin):
    """
    Mixin base para garantir que rotas baseadas em classes (CBV) 
    exijam usuário logado.
    """
    login_url = '/login/'
    redirect_field_name = 'next'
