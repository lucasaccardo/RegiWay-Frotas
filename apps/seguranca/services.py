# Funcao: regras tecnicas de seguranca, anonimizacao e protecao de arquivos.
# Responsável: Kenzo, Pacheco.

import requests
from django.conf import settings

from apps.accounts.forms import CaptchaAuthenticationForm, LoginPassoUmForm


def validar_recaptcha_manual(token, remoteip=None):
    if not token:
        return False, ["captcha-ausente"]

    payload = {
        "secret": settings.RECAPTCHA_PRIVATE_KEY,
        "response": token,
    }

    if remoteip:
        payload["remoteip"] = remoteip

    try:
        resposta = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data=payload,
            timeout=5,
        )
        dados = resposta.json()

    except requests.RequestException:
        return False, ["erro-conexao-recaptcha"]

    ok = dados.get("success", False)
    erros = dados.get("error-codes", [])

    return ok, erros
