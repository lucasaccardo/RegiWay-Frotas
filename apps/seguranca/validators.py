# Funcao: validadores de senha forte e regras de dados sensiveis.
# Responsável: Kenzo, Pacheco.

import re

from django.core.exceptions import ValidationError


class SenhaComplexa:
    """
    Validador de senha que exige ao menos uma letra maiúscula,
    uma minúscula, um número e um caractere especial.
    Registrado em AUTH_PASSWORD_VALIDATORS quando ativado.
    """

    def validate(self, password, user=None):
        erros = []
        if not re.search(r"[A-Z]", password):
            erros.append("A senha deve conter ao menos uma letra maiúscula.")
        if not re.search(r"[a-z]", password):
            erros.append("A senha deve conter ao menos uma letra minúscula.")
        if not re.search(r"\d", password):
            erros.append("A senha deve conter ao menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            erros.append("A senha deve conter ao menos um caractere especial.")
        if erros:
            raise ValidationError(erros)

    def get_help_text(self):
        return (
            "Sua senha deve conter maiúscula, minúscula, número e caractere especial."
        )
