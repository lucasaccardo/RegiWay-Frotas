# Funcao: registra clientes, veiculos, motoristas e contatos no Django Admin.
# Responsável: Kenzo.

from django.contrib import admin
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    """
    Configuração do painel administrativo para o modelo Veiculo.
    Aqui definimos quais informações aparecem na listagem,
    quais filtros podem ser usados e quais campos são somente leitura.
    """

    list_display = (
        "placa",
        "marca",
        "modelo",
        "ano",
        "renavam",
        "criado_por",
        "criado_em",
    )

    list_filter = (
        "marca",
        "ano",
        "criado_em",
    )

    search_fields = (
        "placa",
        "renavam",
        "chassi",
        "marca",
        "modelo",
    )

    readonly_fields = (
        "criado_por",
        "criado_em",
        "atualizado_em",
    )

    def save_model(self, request, veiculo, form, change):
        """
        Antes de salvar um veículo, verifica se ele ainda não possui
        um usuário responsável pelo cadastro.

        Caso não tenha, o sistema define automaticamente o usuário
        logado como o criador do registro.
        """

        if not veiculo.criado_por_id:
            veiculo.criado_por = request.user

        super().save_model(request, veiculo, form, change)a
