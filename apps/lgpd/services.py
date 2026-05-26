# Funcao: regras de negocio de consentimento, exclusao, anonimizacao e auditoria.
# Responsável: Lucas sureira, Pacheco.

from django.contrib.auth import logout
from apps.auditoria.services import registrar_evento


def excluir_conta_usuario(request):
    """
    Anonimiza os dados pessoais do titular e desativa a conta.
    Dados vinculados a obrigações legais (sinistros, auditoria) são preservados anonimizados.
    Cumpre o Art. 18 da LGPD (Direito à Exclusão).
    """
    user = request.user

    registrar_evento(
        tipo='exclusao',
        descricao=f'Usuário {user.username} solicitou exclusão da própria conta.',
        usuario=user,
        request=request,
    )

    # Anonimiza os dados pessoais identificáveis mantendo o registro no banco
    # para preservar a rastreabilidade de sinistros e logs de auditoria
    user.first_name = 'Usuário'
    user.last_name = 'Removido'
    user.email = f'removido_{user.pk}@anonimizado.local'
    user.username = f'removido_{user.pk}'
    user.is_active = False
    user.save()

    logout(request)
    return True
