# Funcao: views do painel gerencial e indicadores operacionais.
# Responsavel: Matheus Deleuterio.

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import montar_contexto_dashboard


def _safe_count(model_path):
    """Tenta contar registros de um model sem quebrar caso o app esteja incompleto."""
    try:
        app_label, model_name = model_path.split(".", 1)
        model = apps.get_model(app_label, model_name)
        return model.objects.count()
    except Exception:
        return 0


@login_required
def index(request):
    """Renderiza a tela principal do dashboard."""
    context = montar_contexto_dashboard(usuario=request.user)
    return render(request, "dashboard/index.html", context)
