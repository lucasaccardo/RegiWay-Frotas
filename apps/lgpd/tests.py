# Funcao: testes de aceite obrigatorio, portabilidade e solicitacoes LGPD.
# Responsável: Pacheco.

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import TermoVigente, ConsentimentoUsuario, SolicitacaoTitular
from .middleware import ConsentimentoObrigatorioMiddleware
from apps.auditoria.models import EventoAuditoria

User = get_user_model()


def criar_termo(vigente=True):
    return TermoVigente.objects.create(
        titulo='Termos de Uso',
        versao='1.0',
        conteudo='Conteúdo dos termos.',
        vigente=vigente,
    )


def criar_consentimento(user, termo):
    return ConsentimentoUsuario.objects.create(
        usuario=user, termo=termo, ip='127.0.0.1', ativo=True
    )


class TermoVigenteModelTest(TestCase):
    def test_str(self):
        termo = criar_termo()
        self.assertEqual(str(termo), 'Termos de Uso v1.0')

    def test_apenas_vigente_retornado(self):
        criar_termo(vigente=False)
        criar_termo(vigente=True)
        self.assertEqual(TermoVigente.objects.filter(vigente=True).count(), 1)


class ConsentimentoUsuarioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='titular', password='senha123')
        self.termo = criar_termo()

    def test_str(self):
        c = criar_consentimento(self.user, self.termo)
        self.assertIn('titular', str(c))

    def test_consentimento_ativo_por_padrao(self):
        c = criar_consentimento(self.user, self.termo)
        self.assertTrue(c.ativo)


class SolicitacaoTitularModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='titular2', password='senha123')

    def test_cria_solicitacao_exclusao(self):
        s = SolicitacaoTitular.objects.create(usuario=self.user, tipo='exclusao')
        self.assertEqual(s.status, 'pendente')

    def test_str_contem_tipo(self):
        s = SolicitacaoTitular.objects.create(usuario=self.user, tipo='portabilidade')
        self.assertIn('Portabilidade', str(s))


class PoliticaPrivacidadeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('lgpd:politica_privacidade')

    def test_acesso_sem_login_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_exibe_termo_vigente(self):
        criar_termo()
        response = self.client.get(self.url)
        self.assertContains(response, 'Termos de Uso')

    def test_sem_termo_vigente_nao_quebra(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class AceiteTermosViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='novo', password='senha123')
        self.termo = criar_termo()
        self.url = reverse('lgpd:aceite_termos')

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/contas/login/?next={self.url}')

    def test_get_exibe_termo(self):
        self.client.login(username='novo', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Termos de Uso')

    def test_post_cria_consentimento(self):
        self.client.login(username='novo', password='senha123')
        self.client.post(self.url)
        self.assertTrue(
            ConsentimentoUsuario.objects.filter(usuario=self.user, ativo=True).exists()
        )

    def test_ja_aceitou_redireciona(self):
        self.client.login(username='novo', password='senha123')
        criar_consentimento(self.user, self.termo)
        response = self.client.get(self.url)
        self.assertRedirects(response, '/')

    def test_sem_termo_vigente_redireciona(self):
        self.termo.vigente = False
        self.termo.save()
        self.client.login(username='novo', password='senha123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/')


class MeusDadosViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='dados_user', password='senha123',
            first_name='João', email='joao@teste.com'
        )
        self.termo = criar_termo()
        criar_consentimento(self.user, self.termo)
        self.url = reverse('lgpd:meus_dados')

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_retorna_200(self):
        self.client.login(username='dados_user', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_atualiza_dados(self):
        self.client.login(username='dados_user', password='senha123')
        self.client.post(self.url, {
            'first_name': 'Carlos',
            'last_name': 'Silva',
            'email': 'carlos@teste.com',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Carlos')
        self.assertEqual(self.user.email, 'carlos@teste.com')


class ExcluirContaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='excluir_user', password='senha123')
        self.termo = criar_termo()
        criar_consentimento(self.user, self.termo)
        self.url = reverse('lgpd:confirmar_exclusao')

    def test_get_exibe_tela_confirmacao(self):
        self.client.login(username='excluir_user', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_anonimiza_usuario(self):
        self.client.login(username='excluir_user', password='senha123')
        pk = self.user.pk
        self.client.post(self.url)
        user = User.objects.get(pk=pk)
        self.assertFalse(user.is_active)
        self.assertIn('removido', user.username)

    def test_post_cria_solicitacao_titular(self):
        self.client.login(username='excluir_user', password='senha123')
        self.client.post(self.url)
        self.assertTrue(SolicitacaoTitular.objects.filter(tipo='exclusao').exists())

    def test_post_registra_evento_auditoria(self):
        self.client.login(username='excluir_user', password='senha123')
        self.client.post(self.url)
        self.assertTrue(EventoAuditoria.objects.filter(tipo='exclusao').exists())


class MiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='mw_user', password='senha123')
        self.termo = criar_termo()

        def dummy_view(request):
            from django.http import HttpResponse
            return HttpResponse('ok')

        self.middleware = ConsentimentoObrigatorioMiddleware(dummy_view)

    def _request(self, path='/sinistros/'):
        request = self.factory.get(path)
        request.user = self.user
        return request

    def test_usuario_sem_aceite_e_redirecionado(self):
        response = self.middleware(self._request('/sinistros/'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('aceite-termos', response['Location'])

    def test_usuario_com_aceite_passa(self):
        criar_consentimento(self.user, self.termo)
        response = self.middleware(self._request('/sinistros/'))
        self.assertEqual(response.status_code, 200)

    def test_rota_livre_nao_bloqueada(self):
        response = self.middleware(self._request('/lgpd/aceite-termos/'))
        self.assertEqual(response.status_code, 200)

    def test_sem_termo_vigente_nao_bloqueia(self):
        self.termo.vigente = False
        self.termo.save()
        response = self.middleware(self._request('/sinistros/'))
        self.assertEqual(response.status_code, 200)
