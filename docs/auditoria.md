# Auditoria
<!-- Responsável: Pacheco. -->

Funcao: documentar eventos auditaveis, rastreabilidade e politica de logs.

---

## Visão Geral

O módulo de auditoria registra automaticamente eventos críticos do sistema para garantir rastreabilidade de ações, conformidade com a LGPD e segurança operacional.

---

## Modelo: EventoAuditoria

Localização: `apps/auditoria/models.py`

| Campo | Tipo | Descrição |
|---|---|---|
| `usuario` | ForeignKey | Usuário que gerou o evento (nulo se anônimo) |
| `tipo` | CharField | Categoria do evento (ver tabela abaixo) |
| `descricao` | TextField | Descrição legível do evento |
| `ip` | GenericIPAddressField | IP da requisição |
| `caminho` | CharField | Rota acessada |
| `objeto_tipo` | CharField | Tipo do objeto afetado (ex: `Veiculo`) |
| `objeto_id` | CharField | PK do objeto afetado |
| `dados_extras` | JSONField | Informações adicionais livres |
| `criado_em` | DateTimeField | Timestamp do evento (automático) |

---

## Tipos de Eventos

| Tipo | Descrição |
|---|---|
| `login` | Login bem-sucedido |
| `logout` | Logout |
| `login_falhou` | Tentativa de login com credenciais inválidas |
| `alteracao` | Alteração de dados de um objeto |
| `exclusao` | Exclusão de registro |
| `acesso_negado` | Requisição bloqueada por permissão (HTTP 403) |
| `exportacao` | Exportação de dados pessoais |
| `solicitacao_lgpd` | Registro de solicitação do titular |
| `outro` | Evento genérico |

---

## Como Registrar um Evento

```python
from apps.auditoria.services import registrar_evento

registrar_evento(
    tipo='alteracao',
    descricao='Usuário atualizou dados do veículo.',
    usuario=request.user,
    request=request,
    objeto=veiculo,
)
```

---

## Registro Automático via Signals

Os seguintes eventos são registrados automaticamente via signals (`apps/auditoria/signals.py`):

- `user_logged_in` → evento `login`
- `user_logged_out` → evento `logout`
- `user_login_failed` → evento `login_falhou`

---

## Middleware de Auditoria

`AuditoriaMiddleware` (`apps/auditoria/middleware.py`) registra automaticamente respostas HTTP 403 como eventos `acesso_negado`.

Para ativar, descomentar em `config/settings/base.py`:
```python
'apps.auditoria.middleware.AuditoriaMiddleware',
```

---

## Política de Retenção de Logs

- Logs de auditoria **não podem ser editados ou excluídos** pelo admin (somente leitura).
- Retenção mínima recomendada: **5 anos** (conforme requisitos legais de sinistros e LGPD).
- Logs de tentativas de login falho devem ser monitorados para detecção de ataques de força bruta.

---

## Referências

- `apps/auditoria/models.py` — EventoAuditoria
- `apps/auditoria/services.py` — registrar_evento
- `apps/auditoria/signals.py` — registro automático
- `apps/auditoria/middleware.py` — AuditoriaMiddleware
- `apps/auditoria/admin.py` — visualização no Django Admin
