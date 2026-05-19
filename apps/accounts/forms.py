# Funcao: formularios de login, cadastro, senha, perfil e aceite de termos.
# Responsável: Kenzo.

from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class LoginPassoUmForm(AuthenticationForm):

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
