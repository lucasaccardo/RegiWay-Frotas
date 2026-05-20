# Funcao: formularios de clientes, veiculos, motoristas e contatos.
# Responsável: Kenzo.

import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Veiculo, normalizar_chassi, normalizar_placa, normalizar_renavam

PLACA_REGEX = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")
CHASSI_REGEX = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")
MAX_ANEXO_MB = 5


class VeiculoForm(forms.ModelForm):
    """Formulário para cadastro e edição de veículos."""

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
            "placa": forms.TextInput(attrs={"placeholder": "ABC1234"}),
            "renavam": forms.TextInput(attrs={"placeholder": "Somente números"}),
            "chassi": forms.TextInput(attrs={"placeholder": "17 caracteres"}),
            "observacao": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Se precisar, adicione alguma observação sobre o veículo.",
                }
            ),
        }
        help_texts = {
            "placa": "Aceita placa antiga ou Mercosul.",
            "renavam": "Informe os 11 dígitos. Pontos e traços serão ignorados.",
            "chassi": "Informe os 17 caracteres do chassi.",
            "anexo": "Formatos aceitos: PDF, JPG, JPEG e PNG. Tamanho máximo: 5 MB.",
        }
        error_messages = {
            "placa": {"unique": "Já existe um veículo cadastrado com essa placa."},
            "renavam": {"unique": "Já existe um veículo cadastrado com esse RENAVAM."},
            "chassi": {"unique": "Já existe um veículo cadastrado com esse chassi."},
        }

    def clean_placa(self):
        placa = normalizar_placa(self.cleaned_data.get("placa"))
        # Valida o formato da placa (ABC1234 ou Mercosul).
        if not PLACA_REGEX.fullmatch(placa):
            raise ValidationError(
                "Informe uma placa válida. Ex.: ABC1234 ou BRA2E19.",
                code="placa_invalida",
            )
        return placa

    def clean_renavam(self):
        renavam = normalizar_renavam(self.cleaned_data.get("renavam"))
        # RENAVAM deve ter 11 dígitos.
        if len(renavam) != 11:
            raise ValidationError(
                "RENAVAM deve ter 11 dígitos.",
                code="renavam_invalido",
            )
        return renavam

    def clean_chassi(self):
        chassi = normalizar_chassi(self.cleaned_data.get("chassi"))
        # Chassi válido tem 17 caracteres (sem espaços).
        if not CHASSI_REGEX.fullmatch(chassi):
            raise ValidationError(
                "Informe um chassi válido com 17 caracteres.",
                code="chassi_invalido",
            )
        return chassi

    def clean_anexo(self):
        arquivo = self.cleaned_data.get("anexo")
        enviado = self.files.get("anexo")
        # Verifica tamanho máximo do arquivo (5 MB).
        if enviado:
            limite = MAX_ANEXO_MB * 1024 * 1024
            if enviado.size > limite:
                raise ValidationError(
                    f"O arquivo deve ter no máximo {MAX_ANEXO_MB} MB.",
                    code="arquivo_muito_grande",
                )
        return arquivo

    def clean(self):
        dados = super().clean()
        ano = dados.get("ano")
        if ano is None:
            return dados

        ano_maximo = timezone.now().year + 1
        # Aceita até o próximo ano para veículos novos.
        if ano < 1950 or ano > ano_maximo:
            self.add_error("ano", f"Informe um ano entre 1950 e {ano_maximo}.")
        return dados
