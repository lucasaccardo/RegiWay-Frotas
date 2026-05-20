# Funcao: registra modelos de accounts no Django Admin.
# Responsável: Kenzo.

from django.contrib import admin
from .models import PerfilUsuario, TermoAceiteUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefone', 'cargo')

@admin.register(TermoAceiteUsuario)
class TermoAceiteUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'versao_termo', 'aceito_em')
