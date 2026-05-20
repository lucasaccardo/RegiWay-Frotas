# Funcao: modelo EventoAuditoria para logs de login, alteracoes e eventos criticos.
# Responsável: Pacheco, João Pedro.

from django.db import models
from django.conf import settings


class EventoAuditoria(models.Model):
    TIPO_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('login_falhou', 'Tentativa de Login Falhou'),
        ('alteracao', 'Alteração de Dados'),
        ('exclusao', 'Exclusão'),
        ('acesso_negado', 'Acesso Negado'),
        ('exportacao', 'Exportação de Dados'),
        ('solicitacao_lgpd', 'Solicitação LGPD'),
        ('outro', 'Outro'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_auditoria',
    )
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descricao = models.TextField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    caminho = models.CharField(max_length=500, blank=True)
    objeto_tipo = models.CharField(max_length=100, blank=True)
    objeto_id = models.CharField(max_length=50, blank=True)
    dados_extras = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento de Auditoria'
        verbose_name_plural = 'Eventos de Auditoria'
        ordering = ['-criado_em']

    def __str__(self):
        return f'[{self.criado_em:%d/%m/%Y %H:%M}] {self.get_tipo_display()} — {self.usuario or "anônimo"}'
