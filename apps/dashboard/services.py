# Funcao: regras de negocio para montagem de metricas e alertas do dashboard.
# Responsavel: Matheus Deleuterio.

from .dashboard_selectors import consultar_dashboard_completo


def montar_cards_indicadores(indicadores):
    """Transforma indicadores numericos em cards visuais para o template."""
    return [
        {
            "titulo": "Veículos cadastrados",
            "valor": indicadores.get("total_veiculos", 0),
            "icone": "car.png",
            "classe": "card-blue",
            "descricao": "Frota registrada no sistema",
        },
        {
            "titulo": "Sinistros registrados",
            "valor": indicadores.get("total_sinistros", 0),
            "icone": "alert.png",
            "classe": "card-orange",
            "descricao": "Ocorrências acompanhadas",
        },
        {
            "titulo": "Clientes ativos",
            "valor": indicadores.get("total_clientes", 0),
            "icone": "users.png",
            "classe": "card-green",
            "descricao": "Clientes vinculados à operação",
        },
        {
            "titulo": "Documentos",
            "valor": indicadores.get("total_documentos", 0),
            "icone": "document.png",
            "classe": "card-purple",
            "descricao": "Arquivos e documentos monitorados",
        },
    ]


def montar_alertas(sla, operacional):
    """Cria mensagens de alerta amigaveis para o usuario da dashboard."""
    alertas = []

    if sla.get("fora_sla", 0) > 0:
        alertas.append(
            f"Existem {sla['fora_sla']} sinistro(s) fora do SLA de 48 horas."
        )
    else:
        alertas.append("Nenhum sinistro fora do SLA no momento.")

    if operacional.get("documentos_pendentes", 0) > 0:
        alertas.append(
            f"Há {operacional['documentos_pendentes']} documento(s) pendente(s) ou vencido(s)."
        )
    else:
        alertas.append("Documentos pendentes não encontrados nos módulos disponíveis.")

    alertas.append("Mantenha os dados da frota atualizados para melhorar os relatórios gerenciais.")
    return alertas


def montar_contexto_dashboard(usuario=None):
    """Monta o contexto completo da tela principal da dashboard."""
    dados = consultar_dashboard_completo()
    indicadores = dados.get("indicadores_numericos", {})
    sla = dados.get("sla", {})
    operacional = dados.get("operacional", {})

    return {
        "titulo_pagina": "Dashboard",
        "subtitulo_pagina": "Visão geral do sistema RegiWay Frotas",
        "usuario_dashboard": usuario,
        "indicadores": montar_cards_indicadores(indicadores),
        "alertas": montar_alertas(sla, operacional),
        "sla": sla,
        "operacional": operacional,
        "grafico_veiculos_mes": dados.get("grafico_veiculos_mes", []),
        "grafico_sinistros_dia": dados.get("grafico_sinistros_dia", []),
    }
