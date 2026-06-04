# Funcao: regras de negocio para montagem de metricas e alertas do dashboard.
# Responsável: Matheus Deleutério.

from django.apps import apps


def contar_modelo(app_label: str, model_name: str) -> int:
    """Conta registros de qualquer model sem quebrar se o app estiver incompleto."""
    try:
        model = apps.get_model(app_label, model_name)
        return model.objects.count()
    except Exception:
        return 0


def montar_indicadores() -> list:
    # ordem definida com o Matheus — ele pediu esse layout específico
    return [
        {"titulo": "Veículos cadastrados", "valor": contar_modelo("frotas", "Veiculo"), "classe": "card-blue"},
        {"titulo": "Sinistros registrados", "valor": contar_modelo("sinistros", "Sinistro"), "classe": "card-orange"},
        {"titulo": "Usuários ativos", "valor": contar_modelo("auth", "User"), "classe": "card-green"},
        {"titulo": "Eventos de auditoria", "valor": contar_modelo("auditoria", "EventoAuditoria"), "classe": "card-purple"},
    ]
