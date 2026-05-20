# Funcao: modelos de Cliente, Veiculo, Motorista e Contato.
# Responsável: Kenzo, João Pedro.
#
# Campos sensiveis previstos, como placa, chassi e telefone, devem usar
# criptografia em repouso quando os modelos forem implementados.

import re
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


def normalizar_placa(valor):
    """Converte para maiúsculas e remove hífen ou espaços."""
    placa = (valor or "").upper().strip()
    return placa.replace("-", "").replace(" ", "")


def normalizar_renavam(valor):
    """Remove caracteres não numéricos."""
    return re.sub(r"\D", "", valor or "")


def normalizar_chassi(valor):
    """Converte para maiúsculas e remove espaços."""
    chassi = (valor or "").upper().strip()
    return chassi.replace(" ", "")



class Veiculo(models.Model):
    """Informações de um veículo da frota."""
    placa = models.CharField(max_length=8, unique=True)
    renavam = models.CharField(max_length=11, unique=True)
    chassi = models.CharField(max_length=17, unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    marca = models.CharField(max_length=80)
    modelo = models.CharField(max_length=80)
    ano = models.PositiveIntegerField()
    cor = models.CharField(max_length=40, blank=True)

    anexo = models.FileField(
        upload_to="veiculos/anexos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["pdf", "jpg", "jpeg", "png"])],
    )
    observacao = models.TextField(blank=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="veiculos_criados",
    )

    class Meta:
        ordering = ["placa"]
        verbose_name = "veículo"
        verbose_name_plural = "veículos"

    def save(self, *args, **kwargs):
        # Padroniza identificadores principais antes de salvar.
        self.placa = normalizar_placa(self.placa)
        self.renavam = normalizar_renavam(self.renavam)
        self.chassi = normalizar_chassi(self.chassi)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
