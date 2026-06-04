# Funcao: views do painel gerencial e indicadores operacionais.
# Responsável: Matheus Deleutério.

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render


def _safe_count(model_path):
    """
    Tenta contar registros de um model sem quebrar a dashboard caso
    algum app ainda esteja incompleto ou sem migração.
    """
    try:
        app_label, model_name = model_path.split(".")
        from django.apps import apps

        model = apps.get_model(app_label, model_name)
        return model.objects.count()
    except Exception:
        return 0


@login_required
def index(request):
    """Renderiza a tela principal do dashboard."""

    indicadores = [
        {
            "titulo": "Veículos cadastrados",
            "valor": _safe_count("frotas.Veiculo"),
            "icone": "car.png",
            "classe": "card-blue",
        },
        {
            "titulo": "Sinistros registrados",
            "valor": _safe_count("sinistros.Sinistro"),
            "icone": "alert.png",
            "classe": "card-orange",
        },
        {
            "titulo": "Clientes ativos",
            "valor": _safe_count("frotas.Cliente"),
            "icone": "users.png",
            "classe": "card-green",
        },
        {
            "titulo": "Documentos",
            "valor": _safe_count("documentos.Documento"),
            "icone": "document.png",
            "classe": "card-purple",
        },
    ]

    context = {
        "titulo_pagina": "Dashboard",
        "subtitulo_pagina": "Visão geral do sistema RegiWay Frotas",
        "indicadores": indicadores,
        "alertas": [
            "Acompanhe os sinistros pendentes e mantenha os dados da frota atualizados.",
            "Verifique anexos, documentos e dados sensíveis antes de gerar relatórios.",
        ],
    }
    return render(request, "dashboard/index.html", context)
