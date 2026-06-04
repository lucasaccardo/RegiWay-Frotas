# Funcao: regras de negocio de autenticacao e sessao.
# Responsável: Kenzo.

from django.contrib.auth import authenticate


def autenticar_usuario(username: str, password: str):
    """Autentica credenciais e retorna o User ou None."""
    return authenticate(username=username, password=password)
