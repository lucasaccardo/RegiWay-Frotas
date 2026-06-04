# Funcao: views das telas de termos, politica, meus dados e solicitacoes LGPD.
# Responsável: Lucas sureira, Pacheco.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Imports locais do próprio app LGPD
from .forms import AtualizarDadosForm
from .exports import exportar_dados_usuario_csv
from .services import excluir_conta_usuario
from .models import TermoVigente, ConsentimentoUsuario, SolicitacaoTitular


# --- Views de Pacheco: Política de Privacidade e Aceite de Termos ---

def politica_privacidade(request):
    termo = TermoVigente.objects.filter(vigente=True).first()
    return render(request, 'lgpd/politica_privacidade.html', {'termo': termo})


@login_required
def aceite_termos(request):
    termo = TermoVigente.objects.filter(vigente=True).first()
    if not termo:
        return redirect('/')

    ja_aceitou = ConsentimentoUsuario.objects.filter(
        usuario=request.user, termo=termo, ativo=True
    ).exists()
    if ja_aceitou:
        return redirect('/')

    if request.method == 'POST':
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded.split(',')[0].strip() if x_forwarded else request.META.get('REMOTE_ADDR')
        ConsentimentoUsuario.objects.get_or_create(
            usuario=request.user,
            termo=termo,
            defaults={'ip': ip, 'ativo': True},
        )
        proximo = request.GET.get('proximo', '/')
        return redirect(proximo)

    return render(request, 'lgpd/aceite_termos.html', {'termo': termo})


@login_required
def meus_dados(request):
    """
    View principal do painel LGPD do usuário. 
    Permite a visualização e alteração dos dados cadastrais do titular.
    """
    if request.method == 'POST':
        # O parâmetro instance=request.user garante que a alteração seja estrita ao usuário logado
        form = AtualizarDadosForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso em conformidade com a LGPD!')
            return redirect('lgpd:meus_dados')
    else:
        # Carrega o formulário preenchido com o estado atual do banco
        form = AtualizarDadosForm(instance=request.user)
        
    return render(request, 'lgpd/meus_dados.html', {'form': form})


@login_required
def baixar_meus_dados(request):
    """
    Garante o Direito à Portabilidade (LGPD).
    Chama a função de exportação e retorna o download do arquivo CSV.
    """
    return exportar_dados_usuario_csv(request.user, request)


@login_required
def confirmar_exclusao(request):
    """
    Garante o Direito à Exclusão (LGPD).
    Exibe a tela de alerta e aciona o serviço de exclusão permanente/anonimização.
    """
    if request.method == 'POST':
        SolicitacaoTitular.objects.create(
            usuario=request.user,
            tipo='exclusao',
            status='em_andamento',
        )
        excluir_conta_usuario(request)
        return redirect('accounts:login')

    return render(request, 'lgpd/solicitar_exclusao.html')
