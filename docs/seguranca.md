# Segurança
<!-- Responsável: Kenzo, Pacheco. -->

Documenta as medidas de segurança implementadas e as que ainda estão planejadas.

---

## Proteção CSRF

Todos os formulários têm `{% csrf_token %}`. O `CsrfViewMiddleware` valida o token em cada POST — sem o token, a requisição é rejeitada com 403.

---

## Sessões

As sessões expiram em 30 minutos de inatividade (`SESSION_COOKIE_AGE = 1800`) e também quando o navegador é fechado (`SESSION_EXPIRE_AT_BROWSER_CLOSE = True`). Em produção, o cookie só trafega via HTTPS (`SESSION_COOKIE_SECURE = True`).

---

## Senhas

O Django usa PBKDF2-SHA256 com salt. Além dos validadores padrão, implementamos um validador próprio em `apps/seguranca/validators.py` que exige maiúscula, minúscula, número e caractere especial.

---

## Headers HTTP

Em produção (`config/settings/production.py`):

| Header | Valor |
|---|---|
| HTTPS obrigatório | `SECURE_SSL_REDIRECT = True` |
| HSTS | 1 ano, subdomínios, preload |
| X-Content-Type-Options | nosniff |
| X-Frame-Options | DENY (padrão do Django) |

O `SecurityHeadersMiddleware` (`apps/seguranca/middleware.py`) adiciona `Referrer-Policy` e `Permissions-Policy` em todas as respostas.

---

## Validação de entrada

- Placa: regex `^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$` — aceita padrão antigo e Mercosul
- RENAVAM: exatamente 11 dígitos
- Chassi: 17 caracteres conforme padrão internacional
- Arquivos: extensão (PDF, JPG, JPEG, PNG) e tamanho (máx 5 MB)

---

## Auditoria de segurança

Eventos registrados automaticamente:
- `login` e `logout` via Signals do Django
- `login_falhou` via Signal
- `acesso_negado` via `AuditoriaMiddleware` (captura respostas 403)

---

## O que ainda está pendente

**django-axes** — bloqueio após tentativas erradas. Configurações já estão em `base.py`, só falta instalar e descomentar o middleware.

**2FA** — `django-two-factor-auth`. Código esboçado em `apps/accounts/`, dependências não instaladas ainda.

**reCAPTCHA** — `django-recaptcha` no formulário de login. Idem.

**Criptografia em repouso** — para campos sensíveis como CPF e telefone. Utilitários de hash e mascaramento já existem em `apps/seguranca/crypto.py`, mas não estão aplicados nos models ainda.
