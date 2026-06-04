# Funcao: permissoes genericas reutilizadas pelos apps internos.
# Responsável: Lucas sureira.

from django.core.exceptions import PermissionDenied


def exigir_staff(usuario):
    """Lança PermissionDenied se o usuário não for staff."""
    if not usuario.is_staff:
        raise PermissionDenied


def exigir_autenticado(usuario):
    """Lança PermissionDenied se o usuário não estiver autenticado."""
    if not usuario.is_authenticated:
        raise PermissionDenied
