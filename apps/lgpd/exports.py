# Funcao: exportacao e portabilidade de dados pessoais do titular.
# Responsável: Lucas sureira, Pacheco.

import csv
from django.http import HttpResponse
from apps.sinistros.models import Sinistro
from apps.auditoria.services import registrar_evento


def exportar_dados_usuario_csv(user, request=None):
    """
    Gera um arquivo CSV com os dados pessoais e histórico de sinistros do usuário.
    Cumpre o requisito de Portabilidade de Dados da LGPD.
    """
    registrar_evento(
        tipo='exportacao',
        descricao=f'Usuário {user.username} exportou seus dados pessoais.',
        usuario=user,
        request=request,
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="meus_dados_{user.username}.csv"'

    writer = csv.writer(response)

    writer.writerow(['--- DADOS CADASTRAIS ---'])
    writer.writerow(['Usuario', 'Nome', 'Sobrenome', 'Email'])
    writer.writerow([user.username, user.first_name, user.last_name, user.email])

    writer.writerow([])

    writer.writerow(['--- HISTORICO DE SINISTROS REGISTRADOS ---'])
    writer.writerow(['ID Sinistro', 'Placa', 'Cliente', 'Data Ocorrencia', 'Status'])

    sinistros = Sinistro.objects.filter(responsavel=user)
    for sinistro in sinistros:
        writer.writerow([sinistro.id, sinistro.placa, sinistro.cliente, sinistro.data_ocorrencia, sinistro.status])

    return response
