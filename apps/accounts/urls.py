# Funcao: rotas de login, logout, recuperacao de senha, perfil e 2FA.
# Responsável: Kenzo.

from django.urls import path
from django.contrib.auth.views import LogoutView
from two_factor.views import (
    LoginView,
    SetupView,
    QRGeneratorView,
    SetupCompleteView,
    ProfileView,
    DisableView,
    BackupTokensView,
)

app_name = "two_factor"

urlpatterns = [
    path("account/login/", LoginView.as_view(), name="login"),
    path("account/logout/", LogoutView.as_view(), name="logout"),

    path("account/two_factor/setup/", SetupView.as_view(), name="setup"),
    path("account/two_factor/qrcode/", QRGeneratorView.as_view(), name="qr"),
    path("account/two_factor/setup/complete/", SetupCompleteView.as_view(), name="setup_complete"),

    path("account/two_factor/", ProfileView.as_view(), name="profile"),
    path("account/two_factor/disable/", DisableView.as_view(), name="disable"),
    path("account/two_factor/backup/tokens/", BackupTokensView.as_view(), name="backup_tokens"),
]
