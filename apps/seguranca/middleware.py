# Funcao: middleware de headers de seguranca HTTP adicionais.
# Responsável: Kenzo, Pacheco.


class SecurityHeadersMiddleware:
    """
    Adiciona headers de segurança em todas as respostas HTTP.
    Complementa o SecurityMiddleware nativo do Django com
    headers não cobertos por padrão.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response["X-Content-Type-Options"] = "nosniff"
        return response
