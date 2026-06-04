# Funcao: consultas ao banco para listagem, filtros e busca de frotas.
# Responsável: Kenzo.

from .models import Veiculo


def listar_veiculos(busca: str = "") -> "QuerySet[Veiculo]":
    qs = Veiculo.objects.select_related("criado_por")
    if busca:
        qs = qs.filter(placa__icontains=busca) | qs.filter(
            marca__icontains=busca
        ) | qs.filter(modelo__icontains=busca)
    return qs


def buscar_veiculo_por_placa(placa: str):
    from apps.frotas.models import normalizar_placa
    return Veiculo.objects.filter(placa=normalizar_placa(placa)).first()
