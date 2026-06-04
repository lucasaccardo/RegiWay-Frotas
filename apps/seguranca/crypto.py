# Funcao: utilitarios de criptografia para campos e dados sensiveis.
# Responsável: Kenzo, Pacheco.

import hashlib
import hmac

from django.conf import settings


def mascarar_cpf(cpf: str) -> str:
    # ex: "12345678901" → "123.***.***-01"
    digits = "".join(c for c in (cpf or "") if c.isdigit())
    if len(digits) != 11:
        return cpf
    return f"{digits[:3]}.***.***.{digits[-2:]}"


def mascarar_telefone(telefone: str) -> str:
    digits = "".join(c for c in (telefone or "") if c.isdigit())
    if len(digits) < 8:
        return telefone
    return f"{'*' * (len(digits) - 4)}{digits[-4:]}"


def hash_identificador(valor: str) -> str:
    # HMAC com a SECRET_KEY — serve pra comparar sem guardar o valor original
    chave = settings.SECRET_KEY.encode()
    return hmac.new(chave, valor.encode(), hashlib.sha256).hexdigest()


def dados_sensiveis_log_safe(dados: dict, campos_sensiveis: list) -> dict:
    # remove campos sensíveis antes de jogar no log de auditoria
    resultado = dict(dados)
    for campo in campos_sensiveis:
        if campo in resultado:
            resultado[campo] = "***"
    return resultado
