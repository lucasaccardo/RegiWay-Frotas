# Funcao: consultas para indicadores, graficos, SLA e acompanhamento operacional.
# Responsavel: Matheus Deleuterio.

from datetime import timedelta

from django.apps import apps
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone


def get_model_safe(model_path):
    """Retorna um model pelo caminho app_label.Modelo sem quebrar a dashboard."""
    try:
        app_label, model_name = model_path.split(".", 1)
        return apps.get_model(app_label, model_name)
    except Exception:
        return None


def count_model(model_path, filtros=None):
    """Conta registros de um model, retornando zero quando o app/model não existir."""
    model = get_model_safe(model_path)
    if model is None:
        return 0

    try:
        queryset = model.objects.all()
        if filtros:
            queryset = queryset.filter(**filtros)
        return queryset.count()
    except Exception:
        return 0


def consultar_indicadores_dashboard():
    """Indicadores numericos principais exibidos no topo do dashboard."""
    return {
        "total_veiculos": count_model("frotas.Veiculo"),
        "total_sinistros": count_model("sinistros.Sinistro"),
        "total_clientes": count_model("frotas.Cliente"),
        "total_documentos": count_model("documentos.Documento"),
    }


def consultar_grafico_cadastros_por_mes(model_path, campo_data="criado_em", meses=6):
    """Agrupa cadastros por mes para alimentar graficos visuais."""
    model = get_model_safe(model_path)
    if model is None:
        return []

    try:
        data_inicio = timezone.now().date() - timedelta(days=meses * 30)
        queryset = (
            model.objects.filter(**{f"{campo_data}__date__gte": data_inicio})
            .annotate(mes=TruncMonth(campo_data))
            .values("mes")
            .annotate(total=Count("id"))
            .order_by("mes")
        )
        return [
            {"rotulo": item["mes"].strftime("%m/%Y") if item["mes"] else "", "total": item["total"]}
            for item in queryset
        ]
    except Exception:
        return []


def consultar_grafico_sinistros_por_dia(dias=30):
    """Agrupa sinistros por dia para acompanhamento operacional."""
    model = get_model_safe("sinistros.Sinistro")
    if model is None:
        return []

    try:
        data_inicio = timezone.now().date() - timedelta(days=dias)
        queryset = (
            model.objects.filter(criado_em__date__gte=data_inicio)
            .annotate(data=TruncDate("criado_em"))
            .values("data")
            .annotate(total=Count("id"))
            .order_by("data")
        )
        return [
            {"rotulo": item["data"].strftime("%d/%m") if item["data"] else "", "total": item["total"]}
            for item in queryset
        ]
    except Exception:
        return []


def consultar_sla_sinistros():
    """Calcula SLA simples: sinistros abertos ha mais de 48h ficam fora do SLA."""
    model = get_model_safe("sinistros.Sinistro")
    if model is None:
        return {"dentro_sla": 0, "fora_sla": 0, "percentual_sla": 100}

    try:
        limite_sla = timezone.now() - timedelta(hours=48)
        total = model.objects.count()
        fora_sla = (
            model.objects.filter(criado_em__lt=limite_sla)
            .exclude(status__iexact="finalizado")
            .count()
        )
        dentro_sla = max(total - fora_sla, 0)
        percentual_sla = round((dentro_sla / total) * 100, 2) if total else 100
        return {"dentro_sla": dentro_sla, "fora_sla": fora_sla, "percentual_sla": percentual_sla}
    except Exception:
        return {"dentro_sla": 0, "fora_sla": 0, "percentual_sla": 100}


def consultar_acompanhamento_operacional():
    """Resumo dos principais status operacionais do sistema."""
    sinistro_model = get_model_safe("sinistros.Sinistro")
    veiculo_model = get_model_safe("frotas.Veiculo")
    documento_model = get_model_safe("documentos.Documento")

    dados = {
        "sinistros_abertos": 0,
        "sinistros_em_andamento": 0,
        "sinistros_finalizados": 0,
        "veiculos_ativos": 0,
        "documentos_pendentes": 0,
    }

    try:
        if sinistro_model:
            dados["sinistros_abertos"] = sinistro_model.objects.filter(
                Q(status__iexact="aberto") | Q(status__iexact="pendente")
            ).count()
            dados["sinistros_em_andamento"] = sinistro_model.objects.filter(
                status__iexact="em andamento"
            ).count()
            dados["sinistros_finalizados"] = sinistro_model.objects.filter(
                status__iexact="finalizado"
            ).count()

        if veiculo_model:
            dados["veiculos_ativos"] = veiculo_model.objects.filter(ativo=True).count()

        if documento_model:
            dados["documentos_pendentes"] = documento_model.objects.filter(
                Q(status__iexact="pendente") | Q(status__iexact="vencido")
            ).count()
    except Exception:
        pass

    return dados


def consultar_dashboard_completo():
    """Consolida todas as consultas usadas pela view principal."""
    return {
        "indicadores_numericos": consultar_indicadores_dashboard(),
        "grafico_veiculos_mes": consultar_grafico_cadastros_por_mes("frotas.Veiculo"),
        "grafico_sinistros_dia": consultar_grafico_sinistros_por_dia(),
        "sla": consultar_sla_sinistros(),
        "operacional": consultar_acompanhamento_operacional(),
    }
