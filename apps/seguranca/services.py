# Funcao: regras tecnicas de seguranca, anonimizacao e protecao de arquivos.
# Responsável: Kenzo, Pacheco.


def validar_recaptcha_manual(token, remoteip=None):
    """
    Valida token reCAPTCHA v2 diretamente na API do Google.
    Retorna (True, []) em caso de sucesso ou (False, [erros]) em falha.
    Usado como fallback caso o django-recaptcha não esteja instalado.
    """
    import requests
    from django.conf import settings

    if not token:
        return False, ["captcha-ausente"]

    payload = {
        "secret": getattr(settings, "RECAPTCHA_PRIVATE_KEY", ""),
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
    except Exception:
        return False, ["captcha-erro-conexao"]

    ok = dados.get("success", False)
    erros = dados.get("error-codes", [])
    return ok, erros
