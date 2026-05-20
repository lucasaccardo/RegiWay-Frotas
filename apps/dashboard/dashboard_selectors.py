# Funcao: consultas para indicadores, graficos, SLA e acompanhamento operacional.
# Responsável: Matheus Deu pro térian.


from datetime import timedelta

from django.apps import apps
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from apps.dashboard.dashboard_selectors import consultar_dashboard_completo

def get_model_safe(model_path):
    try:
        app_label, model_name = model_path.split(".")
        return apps.get_model(app_label, model_name)
    except Exception:
        return None


def count_model(model_path, filtros=None):
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
    return {
        "total_veiculos": count_model("frotas.Veiculo"),
        "total_sinistros": count_model("sinistros.Sinistro"),
        "total_clientes": count_model("frotas.Cliente"),
        "total_documentos": count_model("documentos.Documento"),
    }


def consultar_grafico_cadastros_por_mes(model_path, campo_data="criado_em", meses=6):
    model = get_model_safe(model_path)

    if model is None:
        return []

    try:
        data_inicio = timezone.now().date() - timedelta(days=meses * 30)

        queryset = (
            model.objects
            .filter(**{f"{campo_data}__date__gte": data_inicio})
            .annotate(mes=TruncMonth(campo_data))
            .values("mes")
            .annotate(total=Count("id"))
            .order_by("mes")
        )

        return [
            {
                "mes": item["mes"].strftime("%m/%Y") if item["mes"] else "",
                "total": item["total"],
            }
            for item in queryset
        ]
    except Exception:
        return []


def consultar_grafico_sinistros_por_dia(dias=30):
    model = get_model_safe("sinistros.Sinistro")

    if model is None:
        return []

    try:
        data_inicio = timezone.now().date() - timedelta(days=dias)

        queryset = (
            model.objects
            .filter(criado_em__date__gte=data_inicio)
            .annotate(data=TruncDate("criado_em"))
            .values("data")
            .annotate(total=Count("id"))
            .order_by("data")
        )

        return [
            {
                "data": item["data"].strftime("%d/%m"),
                "total": item["total"],
            }
            for item in queryset
        ]
    except Exception:
        return []


def consultar_sla_sinistros():
    model = get_model_safe("sinistros.Sinistro")

    if model is None:
        return {
            "dentro_sla": 0,
            "fora_sla": 0,
            "percentual_sla": 100,
        }

    try:
        agora = timezone.now()
        limite_sla = agora - timedelta(hours=48)

        total = model.objects.count()

        fora_sla = model.objects.filter(
            criado_em__lt=limite_sla
        ).exclude(
            status__iexact="finalizado"
        ).count()

        dentro_sla = total - fora_sla

        percentual_sla = 100

        if total > 0:
            percentual_sla = round((dentro_sla / total) * 100, 2)

        return {
            "dentro_sla": dentro_sla,
            "fora_sla": fora_sla,
            "percentual_sla": percentual_sla,
        }
    except Exception:
        return {
            "dentro_sla": 0,
            "fora_sla": 0,
            "percentual_sla": 100,
        }


def consultar_acompanhamento_operacional():
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
            dados["veiculos_ativos"] = veiculo_model.objects.filter(
                ativo=True
            ).count()

        if documento_model:
            dados["documentos_pendentes"] = documento_model.objects.filter(
                Q(status__iexact="pendente") | Q(status__iexact="vencido")
            ).count()

    except Exception:
        pass

    return dados


def consultar_dashboard_completo():
    return {
        "indicadores": consultar_indicadores_dashboard(),
        "grafico_veiculos_mes": consultar_grafico_cadastros_por_mes(
            "frotas.Veiculo"
        ),
        "grafico_sinistros_dia": consultar_grafico_sinistros_por_dia(),
        "sla": consultar_sla_sinistros(),
        "operacional": consultar_acompanhamento_operacional(),
    }
