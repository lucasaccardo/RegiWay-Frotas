# Funcao: sinais automaticos para historico, auditoria e atualizacoes derivadas.
# Responsável: Lucas sureira.

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sinistro

@receiver(post_save, sender=Sinistro)
def notificar_novo_sinistro(sender, instance, created, **kwargs):
    """Gatilho acionado automaticamente quando um sinistro é salvo no banco."""
    if created:
        # Aqui podemos disparar e-mails ou logs automáticos no futuro
        pass
