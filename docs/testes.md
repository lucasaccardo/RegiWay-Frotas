# Testes
<!-- Responsável: Todos os membros. -->

Documenta o que foi testado e como rodar os testes.

---

## Como rodar

```bash
# tudo
python manage.py test

# por módulo
python manage.py test apps.auditoria
python manage.py test apps.lgpd
python manage.py test apps.sinistros
python manage.py test apps.accounts
```

---

## O que está coberto

### Auditoria (`apps/auditoria/tests.py`)

Testa o registro dos eventos:
- Evento criado sem usuário (anônimo)
- Evento criado com usuário vinculado
- Dados extras vazios por padrão
- String do modelo exibe o tipo
- Evento com objeto preenche `objeto_tipo` e `objeto_id`
- Login registra evento `login`
- Logout registra evento `logout`
- Login com senha errada registra evento `login_falhou`

### LGPD (`apps/lgpd/tests.py`)

Testa os modelos e as views de privacidade:
- Strings dos modelos TermoVigente, ConsentimentoUsuario, SolicitacaoTitular
- Política de privacidade acessível sem login
- Aceite de termos redireciona sem login, cria ConsentimentoUsuario via POST
- Painel de dados do usuário: GET e POST funcionando
- Exclusão de conta: anonimiza dados, cria SolicitacaoTitular, registra evento
- Middleware: bloqueia sem aceite, libera com aceite, não bloqueia rotas livres

### Sinistros (`apps/sinistros/tests.py`)

- Utilitário `formatar_placa` (maiúscula, com/sem traço)
- Service `atualizar_status_sinistro` (atualiza status, registra auditoria)
- Views: lista, novo sinistro e detalhe redirecionam sem autenticação

### Accounts (`apps/accounts/tests.py`)

- Login válido redireciona
- Login com senha errada exibe mensagem de erro
- Usuário já logado é redirecionado
- Logout via POST encerra sessão

---

## O que ainda não tem teste

- Views de veículos (`apps/frotas/views.py`)
- Exportação CSV de dados (`apps/lgpd/exports.py`)
- Utilitários de criptografia (`apps/seguranca/crypto.py`)
- Dashboard

Esses ficaram planejados para a próxima iteração.

---

## Padrão usado

Cada `TestCase` tem `setUp()` próprio, sem dependência entre testes. O banco é limpo a cada execução pelo framework. Para simular requisições sem servidor, usamos `RequestFactory` nos testes de middleware.
