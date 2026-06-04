# Funcao: registra veiculos no Django Admin.
# Responsável: Kenzo.

from django.contrib import admin

from .models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'ano', 'criado_por', 'criado_em')
    list_filter = ('marca', 'ano')
    search_fields = ('placa', 'renavam', 'chassi', 'marca', 'modelo')
    readonly_fields = ('criado_em', 'atualizado_em')
