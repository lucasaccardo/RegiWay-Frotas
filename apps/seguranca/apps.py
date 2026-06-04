# Funcao: configuracao do app seguranca.
# Responsável: Kenzo, Pacheco.

from django.apps import AppConfig


class SegurancaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.seguranca'
    verbose_name = 'Seguranca'
