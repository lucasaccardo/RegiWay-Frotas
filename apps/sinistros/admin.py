# Funcao: registra sinistros, historicos, anexos e status no Django Admin.
# Responsável: Lucas sureira.

from django.contrib import admin
from .models import Sinistro

@admin.register(Sinistro)
class SinistroAdmin(admin.ModelAdmin):
    list_display = ('placa', 'cliente', 'status', 'data_ocorrencia', 'criado_em')
    list_filter = ('status', 'data_ocorrencia')
    search_fields = ('placa', 'cliente')
