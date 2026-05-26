# Funcao: modelos abstratos e classes base compartilhadas.
# Responsável: Lucas sureira, João Pedro.

from django.db import models

class BaseModel(models.Model):
    """
    Modelo abstrato que adiciona campos de auditoria de tempo
    em todas as tabelas do sistema que herdarem dele.
    """
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True
