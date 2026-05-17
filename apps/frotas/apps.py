# Funcao: configuracao do app frotas.
# Responsável: Kenzo.

from django.apps import AppConfig


class FrotasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.frotas'
    verbose_name = 'Frotas'
