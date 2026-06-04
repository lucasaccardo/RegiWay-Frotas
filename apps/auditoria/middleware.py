# Funcao: middleware para capturar contexto de requisicoes auditaveis.
# Responsável: Pacheco.

from .services import registrar_evento


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403 and request.user.is_authenticated:
            registrar_evento(
                'acesso_negado',
                f'Acesso negado a {request.path}.',
                usuario=request.user,
                request=request,
            )
        return response
