# Funcao: views de cadastro, listagem e edicao de veiculos.
# Responsável: Kenzo.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.auditoria.services import registrar_evento

from .forms import VeiculoForm
from .models import Veiculo


@login_required
def veiculos_list(request):
    q = request.GET.get('q', '').strip()
    veiculos = Veiculo.objects.all()
    if q:
        # filtra por placa, marca ou modelo
        veiculos = (
            veiculos.filter(placa__icontains=q)
            | veiculos.filter(marca__icontains=q)
            | veiculos.filter(modelo__icontains=q)
        )
    return render(request, 'frotas/veiculos_list.html', {'veiculos': veiculos, 'q': q})


@login_required
def veiculo_novo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.criado_por = request.user
            veiculo.save()
            registrar_evento(
                tipo='outro',
                descricao=f'Veículo {veiculo.placa} cadastrado.',
                usuario=request.user,
                request=request,
                objeto=veiculo,
            )
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('frotas:veiculos_list')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = VeiculoForm()
    return render(request, 'frotas/veiculos_form.html', {'form': form, 'titulozinho': 'Novo Veículo'})


@login_required
def veiculo_editar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        if form.is_valid():
            form.save()
            registrar_evento(
                tipo='alteracao',
                descricao=f'Veículo {veiculo.placa} atualizado.',
                usuario=request.user,
                request=request,
                objeto=veiculo,
            )
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('frotas:veiculos_list')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'frotas/veiculos_form.html', {'form': form, 'titulozinho': 'Editar Veículo'})
