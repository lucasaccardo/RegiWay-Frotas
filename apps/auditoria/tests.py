# Funcao: testes dos registros de auditoria e rastreabilidade.
# Responsável: Pacheco.

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import EventoAuditoria
from .services import registrar_evento

User = get_user_model()


class EventoAuditoriaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='auditor', password='senha123')

    def test_cria_evento_sem_usuario(self):
        registrar_evento('outro', 'Evento anônimo.')
        self.assertEqual(EventoAuditoria.objects.count(), 1)
        self.assertIsNone(EventoAuditoria.objects.first().usuario)

    def test_cria_evento_com_usuario(self):
        registrar_evento('login', 'Login registrado.', usuario=self.user)
        evento = EventoAuditoria.objects.first()
        self.assertEqual(evento.usuario, self.user)
        self.assertEqual(evento.tipo, 'login')

    def test_dados_extras_padrao_vazio(self):
        registrar_evento('outro', 'Sem extras.')
        self.assertEqual(EventoAuditoria.objects.first().dados_extras, {})

    def test_str_contem_tipo(self):
        registrar_evento('logout', 'Logout.', usuario=self.user)
        evento = EventoAuditoria.objects.first()
        self.assertIn('Logout', str(evento))

    def test_cria_evento_com_objeto(self):
        registrar_evento('alteracao', 'Alterou usuário.', usuario=self.user, objeto=self.user)
        evento = EventoAuditoria.objects.first()
        self.assertEqual(evento.objeto_tipo, 'User')
        self.assertEqual(evento.objeto_id, str(self.user.pk))


class SinalAuditoriaTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sinaltest', password='senha123')

    def test_login_registra_evento(self):
        self.client.login(username='sinaltest', password='senha123')
        self.assertTrue(EventoAuditoria.objects.filter(tipo='login', usuario=self.user).exists())

    def test_logout_registra_evento(self):
        self.client.login(username='sinaltest', password='senha123')
        self.client.logout()
        self.assertTrue(EventoAuditoria.objects.filter(tipo='logout', usuario=self.user).exists())

    def test_login_falhou_registra_evento(self):
        self.client.post(reverse('admin:login'), {'username': 'sinaltest', 'password': 'errada'})
        self.assertTrue(EventoAuditoria.objects.filter(tipo='login_falhou').exists())
