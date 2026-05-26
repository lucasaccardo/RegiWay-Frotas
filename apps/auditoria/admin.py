# Funcao: registra eventos de auditoria no Django Admin.
# Responsável: Pacheco.

from django.contrib import admin
from .models import EventoAuditoria


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('criado_em', 'tipo', 'usuario', 'ip', 'caminho')
    list_filter = ('tipo', 'criado_em')
    search_fields = ('usuario__username', 'descricao', 'ip', 'caminho')
    readonly_fields = (
        'criado_em', 'usuario', 'tipo', 'descricao',
        'ip', 'caminho', 'objeto_tipo', 'objeto_id', 'dados_extras',
    )
    ordering = ('-criado_em',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
