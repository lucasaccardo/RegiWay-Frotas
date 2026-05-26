# Funcao: configuracao do app dashboard.
# Responsavel: Matheus Deleuterio.

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """Configuracao do app responsavel pela dashboard gerencial."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    label = "dashboard"
    verbose_name = "Dashboard Gerencial"
