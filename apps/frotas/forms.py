# Funcao: formularios de clientes, veiculos, motoristas e contatos.
# Responsável: Kenzo.
# apps/frotas/forms.py
import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Veiculo

PLACA_RE = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")
CHASSI_RE = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            "placa",
            "renavam",
            "chassi",
            "marca",
            "modelo",
            "ano",
            "cor",
            "anexo",
            "observacao",
        ]
        widgets = {
            "observacao": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_placa(self):
        placa = (self.cleaned_data.get("placa") or "").upper().replace("-", "").strip()

        if not PLACA_RE.match(placa):
            raise ValidationError("Placa inválida. Ex.: ABC1234 ou BRA2E19.")

        qs = Veiculo.objects.filter(placa=placa)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Já existe um veículo com essa placa.")

        return placa

    def clean_renavam(self):
        renavam = re.sub(r"\D", "", self.cleaned_data.get("renavam", ""))

        if len(renavam) != 11:
            raise ValidationError("RENAVAM deve ter 11 dígitos.")

        qs = Veiculo.objects.filter(renavam=renavam)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Já existe um veículo com esse RENAVAM.")

        return renavam

    def clean_chassi(self):
        chassi = (self.cleaned_data.get("chassi") or "").upper().strip()

        if not CHASSI_RE.match(chassi):
            raise ValidationError("Chassi inválido. Tem que ter 17 caracteres válidos.")

        qs = Veiculo.objects.filter(chassi=chassi)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Já existe um veículo com esse chassi.")

        return chassi

    def clean(self):
        dados = super().clean()
        ano = dados.get("ano")

        # sem exagerar, só uma trava básica pra não deixarem 1900 ou 3000
        if ano and (ano < 1950 or ano > timezone.now().year + 1):
            self.add_error("ano", "Ano fora de faixa razoável.")

        return dados
