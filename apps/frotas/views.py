# Funcao: views de cadastro, listagem, detalhe e edicao da frota.
# Responsável: Kenzo.
# apps/frotas/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe
from django_otp.decorators import otp_required

from .forms import VeiculoForm
from .models import Veiculo, normalizar_placa, normalizar_renavam


@require_safe
@login_required(login_url="two_factor:login")
def veiculos_list(request):
    """Lista os veículos da frota com uma busca simples."""
    termo_busca = (request.GET.get("q") or "").strip()

    veiculos = Veiculo.objects.all()

    if termo_busca:
        filtros = Q(marca__icontains=termo_busca) | Q(modelo__icontains=termo_busca)

        # Deixa a busca um pouco mais amigável para placa e RENAVAM.
        termo_placa = normalizar_placa(termo_busca)
        if len(termo_placa) >= 3:
            filtros |= Q(placa__icontains=termo_placa)

        termo_renavam = normalizar_renavam(termo_busca)
        if len(termo_renavam) >= 4:
            filtros |= Q(renavam__icontains=termo_renavam)

        veiculos = veiculos.filter(filtros)

    contexto = {
        "veiculos": veiculos,
        "q": termo_busca,
        "termo_busca": termo_busca,
    }
    return render(request, "frotas/veiculos_list.html", contexto)


@require_http_methods(["GET", "POST"])
@login_required(login_url="two_factor:login")
@otp_required(if_configured=True, login_url="two_factor:login")
def veiculo_novo(request):
    """Cadastra um novo veículo."""
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)

        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.criado_por = request.user
            veiculo.save()

            messages.success(request, "Veículo cadastrado com sucesso.")
            return redirect("frotas:veiculos_list")

        messages.error(request, "Não foi possível salvar o veículo. Confira os campos destacados.")
    else:
        form = VeiculoForm()

    titulo_pagina = "Novo veículo"
    contexto = {
        "form": form,
        "titulo": titulo_pagina,
        "titulozinho": titulo_pagina,  # compatibilidade com template existente
    }
    return render(request, "frotas/veiculos_form.html", contexto)


@require_http_methods(["GET", "POST"])
@login_required(login_url="two_factor:login")
@otp_required(if_configured=True, login_url="two_factor:login")
def veiculo_editar(request, pk):
    """Edita um veículo já cadastrado."""
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)

        if form.is_valid():
            form.save()
            messages.success(request, "Veículo atualizado com sucesso.")
            return redirect("frotas:veiculos_list")

        messages.error(request, "Não foi possível atualizar o veículo. Confira os campos destacados.")
    else:
        form = VeiculoForm(instance=veiculo)

    titulo_pagina = f"Editar {veiculo.placa}"
    contexto = {
        "form": form,
        "titulo": titulo_pagina,
        "titulozinho": titulo_pagina,  # compatibilidade com template existente
    }
    return render(request, "frotas/veiculos_form.html", contexto)
