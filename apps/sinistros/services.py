# Funcao: regras de negocio de cadastro, alteracao de status, SLA e auditoria.
# Responsável: Lucas sureira.

from apps.auditoria.services import registrar_evento


def atualizar_status_sinistro(sinistro, novo_status, usuario_responsavel):
    sinistro.status = novo_status
    sinistro.save()
    registrar_evento(
        tipo='alteracao',
        descricao=f'Status do sinistro {sinistro.pk} alterado para "{novo_status}".',
        usuario=usuario_responsavel,
        objeto=sinistro,
    )
    return sinistro
