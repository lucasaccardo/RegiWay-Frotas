# Funcao: sinais para registrar eventos automaticos de auditoria.
# Responsável: Pacheco.

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .services import registrar_evento


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    registrar_evento('login', f'Usuário {user} realizou login.', usuario=user, request=request)


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    registrar_evento('logout', f'Usuário {user} realizou logout.', usuario=user, request=request)


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request, **kwargs):
    registrar_evento(
        'login_falhou',
        f'Tentativa de login falhou para: {credentials.get("username", "?")}.',
        request=request,
    )
