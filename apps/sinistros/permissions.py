# Funcao: permissoes especificas do fluxo operacional de sinistros.
# Responsável: Lucas sureira.


def pode_alterar_status(usuario, sinistro) -> bool:
    """Apenas staff ou o responsável original podem alterar o status."""
    return usuario.is_staff or sinistro.responsavel == usuario


def pode_ver_sinistro(usuario, sinistro) -> bool:
    """Qualquer usuário autenticado pode visualizar sinistros."""
    return usuario.is_authenticated
