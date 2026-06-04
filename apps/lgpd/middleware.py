# Funcao: middleware para bloquear acesso sem consentimento LGPD ativo.
# Responsável: Pacheco.

from django.shortcuts import redirect
from .models import TermoVigente, ConsentimentoUsuario

ROTAS_LIVRES = [
    '/lgpd/aceite-termos/',
    '/lgpd/politica-privacidade/',
    '/contas/login/',
    '/contas/logout/',
    '/contas/cadastro/',
    '/admin/',
    '/static/',
    '/media/',
]


class ConsentimentoObrigatorioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            livre = any(request.path.startswith(rota) for rota in ROTAS_LIVRES)
            if not livre:
                termo = TermoVigente.objects.filter(vigente=True).first()
                if termo:
                    ja_aceitou = ConsentimentoUsuario.objects.filter(
                        usuario=request.user, termo=termo, ativo=True
                    ).exists()
                    if not ja_aceitou:
                        return redirect(f'/lgpd/aceite-termos/?proximo={request.path}')

        return self.get_response(request)
