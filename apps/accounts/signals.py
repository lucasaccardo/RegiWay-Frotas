# Funcao: sinais automaticos relacionados a usuarios e eventos de conta.
# Responsável: Kenzo.

import logging

from django.dispatch import receiver
from two_factor.signals import user_verified

logger = logging.getLogger(__name__)


@receiver(user_verified)
def logou_com_2fa(sender, request, user, device, **kwargs):
    logger.info(
        "2FA ok | user_id=%s | username=%s | device=%s | ip=%s",
        user.pk,
        user.get_username(),
        getattr(device, "name", "sem-nome"),
        request.META.get("REMOTE_ADDR"),
    )
