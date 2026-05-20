# Funcao: testes dos indicadores e consultas do dashboard.
# Responsável: Matheus Deu pro térian.

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.dashboard.views import _safe_count
from apps.frotas.models import Veiculo


class DashboardIndicadoresTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.usuario = User.objects.create_user(
            username="teste",
            email="teste@email.com",
            password="123456"
        )

        Veiculo.objects.create(
            placa="ABC1D23",
            renavam="12345678901",
            chassi="9BWZZZ377VT004251",
            marca="Volkswagen",
            modelo="Gol",
            ano=2020,
            cor="Branco",
            criado_por=self.usuario
        )

    def test_dashboard_exige_login(self):
        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_carrega_com_usuario_logado(self):
        self.client.login(username="teste", password="123456")

        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")

    def test_dashboard_possui_indicadores_no_contexto(self):
        self.client.login(username="teste", password="123456")

        response = self.client.get(reverse("dashboard:index"))

        self.assertIn("indicadores", response.context)
        self.assertEqual(len(response.context["indicadores"]), 4)

    def test_indicador_veiculos_cadastrados_conta_registros(self):
        self.client.login(username="teste", password="123456")

        response = self.client.get(reverse("dashboard:index"))
        indicadores = response.context["indicadores"]

        veiculos = next(
            item for item in indicadores
            if item["titulo"] == "Veículos cadastrados"
        )

        self.assertEqual(veiculos["valor"], 1)
        self.assertEqual(veiculos["icone"], "car.png")
        self.assertEqual(veiculos["classe"], "card-blue")

    def test_indicadores_possuem_campos_obrigatorios(self):
        self.client.login(username="teste", password="123456")

        response = self.client.get(reverse("dashboard:index"))

        for indicador in response.context["indicadores"]:
            self.assertIn("titulo", indicador)
            self.assertIn("valor", indicador)
            self.assertIn("icone", indicador)
            self.assertIn("classe", indicador)

    def test_dashboard_possui_alertas(self):
        self.client.login(username="teste", password="123456")

        response = self.client.get(reverse("dashboard:index"))

        self.assertIn("alertas", response.context)
        self.assertGreater(len(response.context["alertas"]), 0)

    def test_safe_count_model_existente(self):
        resultado = _safe_count("frotas.Veiculo")

        self.assertEqual(resultado, 1)

    def test_safe_count_model_inexistente_retorna_zero(self):
        resultado = _safe_count("app_inexistente.ModeloInexistente")

        self.assertEqual(resultado, 0)
