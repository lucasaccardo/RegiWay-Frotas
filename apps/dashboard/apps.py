# Funcao: configuracao do app dashboard.
# Responsável: Matheus Deu pro térian.

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'Dashboard'
