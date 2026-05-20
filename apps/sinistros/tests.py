# Funcao: testes do fluxo de sinistros, historico, anexos e status.
# Responsável: Lucas sureira.

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import MagicMock, patch
from apps.core.utils import formatar_placa
from apps.auditoria.models import EventoAuditoria
from apps.lgpd.models import TermoVigente, ConsentimentoUsuario
from .services import atualizar_status_sinistro

User = get_user_model()


def criar_consentimento(user):
    termo, _ = TermoVigente.objects.get_or_create(
        titulo='Termos', versao='1.0',
        defaults={'conteudo': 'Conteúdo.', 'vigente': True}
    )
    ConsentimentoUsuario.objects.get_or_create(
        usuario=user, termo=termo, defaults={'ip': '127.0.0.1', 'ativo': True}
    )


class FormatarPlacaTest(TestCase):
    """Testa o utilitário de formatação de placa do core."""

    def test_formata_placa_sem_traco(self):
        self.assertEqual(formatar_placa('ABC1234'), 'ABC-1234')

    def test_placa_minuscula_vira_maiuscula(self):
        self.assertEqual(formatar_placa('abc1234'), 'ABC-1234')

    def test_placa_vazia_retorna_vazio(self):
        self.assertEqual(formatar_placa(''), '')

    def test_placa_com_tamanho_diferente_nao_altera(self):
        self.assertEqual(formatar_placa('ABCD1234'), 'ABCD1234')


class AtualiarStatusSinistroTest(TestCase):
    """Testa o service de atualização de status e a geração do evento de auditoria."""

    def setUp(self):
        self.user = User.objects.create_user(username='operador', password='senha123')

    def test_atualiza_status(self):
        sinistro = MagicMock()
        sinistro.pk = 99
        sinistro.status = 'Aberto'
        resultado = atualizar_status_sinistro(sinistro, 'Em Andamento', self.user)
        self.assertEqual(resultado.status, 'Em Andamento')
        sinistro.save.assert_called_once()

    def test_registra_evento_auditoria(self):
        sinistro = MagicMock()
        sinistro.pk = 99
        atualizar_status_sinistro(sinistro, 'Concluido', self.user)
        self.assertTrue(EventoAuditoria.objects.filter(tipo='alteracao').exists())

    def test_descricao_evento_contem_novo_status(self):
        sinistro = MagicMock()
        sinistro.pk = 99
        atualizar_status_sinistro(sinistro, 'Recusado', self.user)
        evento = EventoAuditoria.objects.filter(tipo='alteracao').first()
        self.assertIn('Recusado', evento.descricao)


class ListaSinistrosViewTest(TestCase):
    """Testa o acesso e autenticação da view de listagem."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='lista_user', password='senha123')
        criar_consentimento(self.user)
        self.url = reverse('sinistros:lista_sinistros')

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_autenticado_retorna_200(self):
        self.client.login(username='lista_user', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class NovoSinistroViewTest(TestCase):
    """Testa o formulário de criação de sinistro."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='novo_user', password='senha123')
        criar_consentimento(self.user)
        self.url = reverse('sinistros:novo_sinistro')

    def test_get_exibe_formulario(self):
        self.client.login(username='novo_user', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class DetailSinistroViewTest(TestCase):
    """Testa o acesso à tela de detalhe."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='detail_user', password='senha123')
        criar_consentimento(self.user)

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(reverse('sinistros:detail_sinistro', args=[1]))
        self.assertEqual(response.status_code, 302)


class HistoricoSinistroViewTest(TestCase):
    """Testa o acesso à tela de histórico."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='hist_user', password='senha123')
        criar_consentimento(self.user)

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(reverse('sinistros:historico_sinistro', args=[1]))
        self.assertEqual(response.status_code, 302)
