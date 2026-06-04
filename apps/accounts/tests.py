# Funcao: testes de login, logout e controle de sessao.
# Responsável: Kenzo.

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teste', password='senha123')
        self.url = reverse('accounts:login')

    def test_get_exibe_formulario(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_valido_redireciona(self):
        response = self.client.post(self.url, {'username': 'teste', 'password': 'senha123'})
        self.assertEqual(response.status_code, 302)

    def test_login_invalido_retorna_erro(self):
        response = self.client.post(self.url, {'username': 'teste', 'password': 'errada'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha incorretos.')

    def test_usuario_autenticado_redireciona(self):
        self.client.login(username='teste', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teste2', password='senha123')
        self.url = reverse('accounts:logout')

    def test_logout_via_post(self):
        self.client.login(username='teste2', password='senha123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
