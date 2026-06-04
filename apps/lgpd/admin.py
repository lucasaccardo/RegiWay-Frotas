# Funcao: registra termos, consentimentos e solicitacoes LGPD no Django Admin.
# Responsável: Pacheco.

from django.contrib import admin
from .models import TermoVigente, ConsentimentoUsuario, SolicitacaoTitular


@admin.register(TermoVigente)
class TermoVigenteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'versao', 'vigente', 'criado_em')
    list_filter = ('vigente',)
    search_fields = ('titulo', 'versao')


@admin.register(ConsentimentoUsuario)
class ConsentimentoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'termo', 'aceito_em', 'ip', 'ativo')
    list_filter = ('ativo', 'aceito_em')
    search_fields = ('usuario__username',)
    readonly_fields = ('aceito_em',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SolicitacaoTitular)
class SolicitacaoTitularAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'status', 'criado_em', 'prazo')
    list_filter = ('tipo', 'status')
    search_fields = ('usuario__username',)
    readonly_fields = ('criado_em', 'atualizado_em')
