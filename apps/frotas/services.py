# Funcao: regras de negocio para cadastro e manutencao da frota.
# Responsável: Kenzo.

from apps.auditoria.services import registrar_evento

from .models import Veiculo


def cadastrar_veiculo(dados: dict, usuario) -> Veiculo:
    veiculo = Veiculo(**dados, criado_por=usuario)
    veiculo.full_clean()
    veiculo.save()
    registrar_evento(
        tipo="outro",
        descricao=f"Veículo {veiculo.placa} cadastrado.",
        usuario=usuario,
        objeto=veiculo,
    )
    return veiculo


def atualizar_veiculo(veiculo: Veiculo, dados: dict, usuario) -> Veiculo:
    for campo, valor in dados.items():
        setattr(veiculo, campo, valor)
    veiculo.full_clean()
    veiculo.save()
    registrar_evento(
        tipo="alteracao",
        descricao=f"Veículo {veiculo.placa} atualizado.",
        usuario=usuario,
        objeto=veiculo,
    )
    return veiculo
