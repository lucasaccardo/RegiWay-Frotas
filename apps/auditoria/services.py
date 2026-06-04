# Funcao: regras de negocio para gravacao padronizada de eventos de auditoria.
# Responsável: Pacheco.

from .models import EventoAuditoria


def registrar_evento(tipo, descricao, usuario=None, request=None, objeto=None, dados_extras=None):
    ip = None
    caminho = ''
    if request:
        ip = _get_client_ip(request)
        caminho = request.path

    objeto_tipo = ''
    objeto_id = ''
    if objeto is not None:
        objeto_tipo = type(objeto).__name__
        objeto_id = str(getattr(objeto, 'pk', ''))

    EventoAuditoria.objects.create(
        usuario=usuario,
        tipo=tipo,
        descricao=descricao,
        ip=ip,
        caminho=caminho,
        objeto_tipo=objeto_tipo,
        objeto_id=objeto_id,
        dados_extras=dados_extras or {},
    )


def _get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
