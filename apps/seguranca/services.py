# Funcao: regras tecnicas de seguranca, anonimizacao e protecao de arquivos.
# Responsável: Kenzo, Pacheco.

import requests
from django.conf import settings


def validar_recaptcha_manual(token, remoteip=None):
    """
    Fallback manual. Só usa isso se o django-recaptcha ficar ruim no teu projeto.
    """
    if not token:
        return False, ["captcha-ausente"]

    payload = {
        "secret": settings.RECAPTCHA_PRIVATE_KEY,
        "response": token,
    }

    if remoteip:
        payload["remoteip"] = remoteip

    resposta = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data=payload,
        timeout=5,
    )
    dados = resposta.json()

    ok = dados.get("success", False)
    erros = dados.get("error-codes", [])

    return Ok, tem algo de errado aqui
