# Testes de seguranca
<!-- Responsável: Pacheco, Kenzo. -->

Funcao: documentar validacoes de seguranca, tentativas falhas, sessoes e LGPD.

---

## Visão Geral

Este documento descreve os testes de segurança implementados e os cenários que devem ser validados no sistema RegiWay Frotas.

---

## Testes de Autenticação

| Cenário | Resultado Esperado | Localização |
|---|---|---|
| Login com credenciais válidas | Redireciona para dashboard, registra evento `login` | `apps/auditoria/tests.py` |
| Login com senha errada | Retorna erro, registra evento `login_falhou` | `apps/auditoria/tests.py` |
| Logout | Encerra sessão, registra evento `logout` | `apps/auditoria/tests.py` |
| Acesso a rota protegida sem login | Redireciona para `/contas/login/` | `apps/lgpd/tests.py` |

---

## Testes de Consentimento LGPD

| Cenário | Resultado Esperado | Localização |
|---|---|---|
| Usuário sem aceite tenta acessar rota protegida | Redirecionado para `/lgpd/aceite-termos/` | `apps/lgpd/tests.py` |
| Usuário aceita os termos | `ConsentimentoUsuario` criado com `ativo=True` | `apps/lgpd/tests.py` |
| Usuário já aceitou e acessa tela de aceite | Redireciona para home | `apps/lgpd/tests.py` |
| Política de privacidade acessada sem login | HTTP 200 (rota pública) | `apps/lgpd/tests.py` |
| Nenhum termo vigente cadastrado | Redireciona para home | `apps/lgpd/tests.py` |

---

## Testes de Sessão

| Cenário | Resultado Esperado |
|---|---|
| Sessão expira após inatividade (1800s) | Usuário deslogado automaticamente (`SESSION_COOKIE_AGE`) |
| Navegador fechado | Sessão encerrada (`SESSION_EXPIRE_AT_BROWSER_CLOSE = True`) |

---

## Testes de Auditoria

| Cenário | Resultado Esperado | Localização |
|---|---|---|
| Evento criado sem usuário | `EventoAuditoria` com `usuario=None` | `apps/auditoria/tests.py` |
| Evento criado com usuário | `EventoAuditoria` vinculado ao usuário | `apps/auditoria/tests.py` |
| Evento com objeto | `objeto_tipo` e `objeto_id` preenchidos | `apps/auditoria/tests.py` |
| Acesso negado (HTTP 403) | Evento `acesso_negado` registrado pelo middleware | Manual |

---

## Testes de Controle de Acesso

| Cenário | Resultado Esperado |
|---|---|
| Usuário comum acessa área administrativa | HTTP 403 ou redirecionamento |
| Usuário tenta editar/excluir evento de auditoria | Operação bloqueada (Admin somente leitura) |
| Usuário tenta editar consentimento via Admin | Operação bloqueada (`has_change_permission = False`) |

---

## Como Executar os Testes

```bash
python manage.py test apps.auditoria apps.lgpd
```

---

## Referências

- `apps/auditoria/tests.py`
- `apps/lgpd/tests.py`
- `config/settings/base.py` — configurações de sessão
