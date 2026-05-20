# Funcao: modelos de usuario, perfil de usuario e aceite de termos.
# Responsável: Kenzo, João Pedro.
#
# Modelos previstos:
# - Usuario
# - PerfilUsuario
# - TermoAceiteUsuario

from django.conf import settings
from django.db import models

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    cargo = models.CharField("Cargo", max_length=80, blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        return self.usuario.get_username()

class TermoAceiteUsuario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    versao_termo = models.CharField("Versão do Termo", max_length=20)
    aceito_em = models.DateTimeField("Aceito em", auto_now_add=True)
    ip_aceite = models.GenericIPAddressField("IP de Aceite", null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.get_username()} - termo {self.versao_termo}"
