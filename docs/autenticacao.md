# Autenticação
<!-- Responsável: Kenzo, Pacheco. -->

Documenta o login, sessões e o que foi implementado de segurança de acesso.

---

## Login

O fluxo atual usa as views do próprio Django (`authenticate`, `login`). O usuário informa usuário e senha, o sistema verifica e cria a sessão. Em caso de falha, o evento `login_falhou` é registrado na auditoria automaticamente via Signal.

Rota: `/contas/login/`

---

## Sessões

| Configuração | Valor |
|---|---|
| Tempo de sessão | 1800 segundos (30 min) |
| Fechar navegador | Encerra a sessão |
| Cookie seguro (produção) | Sim, apenas HTTPS |

---

## Senhas

O Django usa PBKDF2 com SHA-256 e salt aleatório por padrão. Os validadores ativos:
- Não pode ser parecida com o nome do usuário
- Mínimo 8 caracteres
- Não pode ser uma senha muito comum
- Não pode ser só números

---

## Recuperação de senha

Usa as views nativas do Django. Envia e-mail com link único que expira em 1 hora (`PASSWORD_RESET_TIMEOUT = 3600`).

---

## Controle de acesso

Todas as views protegidas usam `@login_required`. Quem não está logado é redirecionado para `/contas/login/?next=<rota>`.

---

## O que está planejado mas ainda não implementado

**2FA (Autenticação em dois fatores)**
Estava previsto com o pacote `django-two-factor-auth` + `django-otp`. As classes `LoginComCaptchaView` e `Setup2FAView` foram esboçadas em `apps/accounts/views.py` mas dependem da instalação dos pacotes.

**reCAPTCHA**
Previsto no formulário de login via `django-recaptcha`. Impede bots de tentar senhas automaticamente.

**Proteção contra força bruta**
Previsto com `django-axes` (bloqueia após 5 tentativas erradas por 1 hora). Já tem as configs em `base.py`:
```python
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
```
Só falta instalar o pacote e descomentar o middleware.

---

## Referências

- `apps/accounts/views.py`
- `apps/accounts/forms.py`
- `apps/accounts/urls.py`
- `config/settings/base.py`
