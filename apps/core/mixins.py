# Funcao: mixins reutilizaveis para views e regras comuns.
# Responsável: Lucas sureira.

from django.contrib.auth.mixins import LoginRequiredMixin


class AutenticacaoObrigatoriaMixin(LoginRequiredMixin):
    """Mixin base para CBVs que exigem usuário autenticado."""
    login_url = '/contas/login/'
    redirect_field_name = 'next'
