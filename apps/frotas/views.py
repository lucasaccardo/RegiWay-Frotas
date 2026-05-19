# Funcao: views de cadastro, listagem, detalhe e edicao da frota.
# Responsável: Kenzo.
# apps/frotas/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django_otp.decorators import otp_required
from .forms import VeiculoForm
from .models import Veiculo

@login_required(login_url="two_factor:login")
def veiculos_list(request):
    q = (request.GET.get("q") or "").strip()

    lista = Veiculo.objects.all()
    if q:
        lista = lista.filter(
            Q(placa__icontains=q)
            | Q(marca__icontains=q)
            | Q(modelo__icontains=q)
            | Q(renavam__icontains=q)
        )

    return render(
        request,
        "frotas/veiculos_list.html",
        {"veiculos": lista, "q": q},
    )


@otp_required(if_configured=True, login_url="two_factor:login")
def veiculo_novo(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.criado_por = request.user
            obj.save()

            messages.success(request, "Veículo salvo. Bora pro próximo.")
            return redirect("frotas:veiculos_list")
    else:
        form = VeiculoForm()

    return render(
        request,
        "frotas/veiculos_form.html",
        {"form": form, "titulozinho": "Novo veículo"},
    )


@otp_required(if_configured=True, login_url="two_factor:login")
def veiculo_editar(request, pk):
    veic = get_object_or_404(Veiculo, pk=pk)

    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES, instance=veic)
        if form.is_valid():
            form.save()
            messages.success(request, "Veículo atualizado.")
            return redirect("frotas:veiculos_list")
    else:
        form = VeiculoForm(instance=veic)

    return render(
        request,
        "frotas/veiculos_form.html",
        {"form": form, "titulozinho": f"Editar {veic.placa}"},
    )
