# Funcao: formulario de login seguro com validacao de campos.
# Responsável: Kenzo.
#
# Nota: reCAPTCHA e 2FA previstos para proxima etapa. Ver docs/autenticacao.md.

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'}),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
    )
