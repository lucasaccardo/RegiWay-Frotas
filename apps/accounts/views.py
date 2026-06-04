# Funcao: views de autenticacao, login seguro com CSRF e protecao de sessao.
# Responsável: Kenzo.
#
# Nota: o fluxo de 2FA (django-two-factor-auth) e reCAPTCHA (django-recaptcha)
# estao previstos como proxima etapa de seguranca. Ver docs/autenticacao.md.

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            senha = form.cleaned_data['password']
            user = authenticate(request, username=usuario, password=senha)
            if user is not None:
                login(request, user)
                proximo = request.GET.get('next', '/dashboard/')
                return redirect(proximo)
            else:
                form.add_error(None, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('accounts:login')
