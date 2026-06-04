# Funcao: consultas ao banco para filtros, dashboards e acompanhamento de SLA.
# Responsável: Lucas sureira.

from .models import Sinistro

def obter_sinistros_ativos():
    """Retorna todos os sinistros que ainda não foram concluídos."""
    return Sinistro.objects.exclude(status='Concluido').order_by('-criado_em')

def obter_sinistros_por_cliente(nome_cliente):
    """Filtra sinistros específicos de um cliente."""
    return Sinistro.objects.filter(cliente__icontains=nome_cliente)
