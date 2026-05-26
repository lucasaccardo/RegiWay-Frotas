# Funcao: views de telas e endpoints do modulo de sinistros.
# Responsável: Lucas sureira.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sinistro
from .forms import SinistroForm
from apps.auditoria.services import registrar_evento


@login_required
def lista_sinistros(request):
    sinistros = Sinistro.objects.all().order_by('-criado_em')
    return render(request, 'sinistros/list.html', {'sinistros': sinistros})


@login_required
def novo_sinistro(request):
    if request.method == 'POST':
        form = SinistroForm(request.POST, request.FILES)
        if form.is_valid():
            sinistro = form.save(commit=False)
            sinistro.responsavel = request.user
            sinistro.save()
            registrar_evento(
                tipo='outro',
                descricao=f'Sinistro registrado: placa {sinistro.placa} — cliente {sinistro.cliente}.',
                usuario=request.user,
                request=request,
                objeto=sinistro,
            )
            messages.success(request, 'Sinistro registrado com sucesso!')
            return redirect('sinistros:lista_sinistros')
        else:
            messages.error(request, 'Erro ao registrar o sinistro. Verifique os campos.')
    else:
        form = SinistroForm()

    return render(request, 'sinistros/form.html', {'form': form, 'titulo': 'Novo Registro de Sinistro'})


@login_required
def detail_sinistro(request, pk):
    sinistro = get_object_or_404(Sinistro, pk=pk)
    return render(request, 'sinistros/detail.html', {'sinistro': sinistro})


@login_required
def historico_sinistro(request, pk):
    sinistro = get_object_or_404(Sinistro, pk=pk)
    return render(request, 'sinistros/historico.html', {'sinistro': sinistro})
