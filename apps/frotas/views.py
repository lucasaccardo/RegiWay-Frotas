# Funcao: views de cadastro, listagem, detalhe e edicao da frota.
# Responsável: Kenzo.
# apps/frotas/views.py
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django_otp.decorators import otp_required

from .forms import VeiculoForm
from .models import Veiculo


@otp_required(login_url="/contas/account/login/")
def veiculos_list(request):
    busca = request.GET.get("q", "").strip()
    veiculos = Veiculo.objects.all()

    if busca:
        veiculos = veiculos.filter(
            Q(placa__icontains=busca) |
            Q(marca__icontains=busca) |
            Q(modelo__icontains=busca)
        )

    contexto = {
        "veiculos": veiculos,
        "q": busca,
    }
    return render(request, "frotas/veiculos_list.html", contexto)


@otp_required(login_url="/contas/account/login/")
def veiculo_novo(request):
    form = VeiculoForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        veiculo = form.save(commit=False)
        veiculo.criado_por = request.user
        veiculo.save()
        return redirect("frotas:veiculos_list")

    return render(request, "frotas/veiculos_form.html", {
        "form": form,
        "titulo": "Novo veículo",
    })


@otp_required(login_url="/contas/account/login/")
def veiculo_editar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    form = VeiculoForm(request.POST or None, instance=veiculo)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("frotas:veiculos_list")

    contexto = {
        "form": form,
        "titulo": "Editar veículo",
        "veiculo": veiculo,
    }
    return render(request, "frotas/veiculos_form.html", contexto)

