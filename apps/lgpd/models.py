# Funcao: modelos de termos, consentimentos, solicitacoes e exportacoes LGPD.
# Responsável: Pacheco, João Pedro.

from django.db import models
from django.conf import settings


class TermoVigente(models.Model):
    titulo = models.CharField(max_length=200)
    versao = models.CharField(max_length=20)
    conteudo = models.TextField()
    vigente = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Termo Vigente'
        verbose_name_plural = 'Termos Vigentes'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.titulo} v{self.versao}'


class ConsentimentoUsuario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consentimentos',
    )
    termo = models.ForeignKey(TermoVigente, on_delete=models.PROTECT)
    aceito_em = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Consentimento'
        verbose_name_plural = 'Consentimentos'
        ordering = ['-aceito_em']

    def __str__(self):
        return f'{self.usuario} — {self.termo}'


class SolicitacaoTitular(models.Model):
    TIPO_CHOICES = [
        ('exclusao', 'Exclusão de Dados'),
        ('portabilidade', 'Portabilidade de Dados'),
        ('retificacao', 'Retificação de Dados'),
        ('oposicao', 'Oposição ao Tratamento'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('recusada', 'Recusada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='solicitacoes_lgpd',
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    justificativa = models.TextField(blank=True)
    resposta = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    prazo = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Solicitação do Titular'
        verbose_name_plural = 'Solicitações do Titular'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.usuario} ({self.get_status_display()})'
