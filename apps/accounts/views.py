# Funcao: views de autenticacao, cadastro, perfil, senha e aceite de termos.
# Responsável: Kenzo.

from two_factor.forms import AuthenticationTokenForm, BackupTokenForm
from two_factor.views import LoginView, SetupView

from .forms import LoginPassoUmForm


class LoginComCaptchaView(LoginView):
    template_name = "accounts/login.html"
    form_list = (
        (LoginView.AUTH_STEP, LoginPassoUmForm),
        (LoginView.TOKEN_STEP, AuthenticationTokenForm),
        (LoginView.BACKUP_STEP, BackupTokenForm),
    )


class Setup2FAView(SetupView):
    template_name = "accounts/two_factor.html"
