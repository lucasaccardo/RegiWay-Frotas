# Funcao: modelos de Sinistro com status, SLA e anexo.
# Responsável: Lucas sureira, João Pedro.

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.core.models import BaseModel


class Sinistro(BaseModel):
    STATUS_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Em Andamento', 'Em Andamento'),
        ('Aguardando Peças', 'Aguardando Peças'),
        ('Concluido', 'Concluído'),
        ('Recusado', 'Recusado'),
    ]

    placa = models.CharField(max_length=10, verbose_name='Placa')
    chassi = models.CharField(max_length=17, blank=True, verbose_name='Chassi')
    cliente = models.CharField(max_length=200, verbose_name='Cliente')
    telefone_contato = models.CharField(max_length=20, blank=True, verbose_name='Telefone de Contato')
    data_ocorrencia = models.DateField(verbose_name='Data da Ocorrência')
    descricao = models.TextField(verbose_name='Descrição da Avaria')
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Aberto',
        verbose_name='Status',
    )
    documento_anexo = models.FileField(
        upload_to='sinistros/anexos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name='Documento Anexo',
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='sinistros_registrados',
        verbose_name='Responsável',
    )

    class Meta:
        verbose_name = 'Sinistro'
        verbose_name_plural = 'Sinistros'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Sinistro #{self.pk} — {self.placa} / {self.cliente} ({self.status})'
