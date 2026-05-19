# Funcao: views de cadastro, listagem, detalhe e edicao da frota.
# Responsável: Kenzo.
# apps/frotas/views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from frotas.forms import VeiculoForm
from frotas.models import Veiculo


class VeiculoUniquenessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="joao",
            password="senha123",
        )
        Veiculo.objects.create(
            placa="ABC1234",
            renavam="12345678901",
            chassi="9BWZZZ377VT004251",
            marca="Volkswagen",
            modelo="Gol",
            ano=2024,
            criado_por=self.user,
        )

    def test_form_mostra_erro_quando_placa_ja_existe(self):
        form = VeiculoForm(
            data={
                "placa": "ABC-1234",
                "renavam": "10987654321",
                "chassi": "9BWZZZ377VT004252",
                "marca": "Fiat",
                "modelo": "Uno",
                "ano": 2024,
                "cor": "Branco",
                "observacao": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "placa",
            "Já existe um veículo cadastrado com essa placa.",
        )
