# Responsabilidades individuais no projeto
<!-- Responsável: Todos os membros. -->

Este arquivo organiza as responsabilidades de cada membro da equipe e as pastas/arquivos principais relacionados a cada área.

## João Pedro - Banco de dados

Responsável pela estrutura, manutenção e documentação do banco de dados.

Pastas/arquivos de responsabilidade:
- `docs/banco-de-dados.md`
- `apps/accounts/models.py`
- `apps/auditoria/models.py`
- `apps/core/models.py`
- `apps/frotas/models.py`
- `apps/lgpd/models.py`
- `apps/sinistros/models.py`
- `apps/accounts/migrations/`
- `apps/auditoria/migrations/`
- `apps/core/migrations/`
- `apps/frotas/migrations/`
- `apps/lgpd/migrations/`
- `apps/sinistros/migrations/`
- `config/settings/base.py`
- `config/settings/development.py`
- `config/settings/production.py`

## Kenny - Front-End

Responsável pelo desenvolvimento e manutenção da interface visual do sistema.

Pastas/arquivos de responsabilidade:
- `templates/`
- `static/css/app.css`
- `static/js/app.js`
- `static/vendor/`
- `templates/base.html`
- `templates/partials/`

## Kenzo - Cadastro de veículos e requisito LGPD de autenticação

Responsável pelos cadastros de veículos e pelo requisito LGPD relacionado à verificação em duas etapas no login e no cadastro de usuário.

Recomendação JP:
- Utilizar captcha.
- Utilizar API do Google para autenticação.

Pastas/arquivos de responsabilidade:
- `apps/frotas/`
- `templates/frotas/veiculos_list.html`
- `templates/frotas/veiculos_form.html`
- `apps/accounts/`
- `templates/accounts/login.html`
- `templates/accounts/two_factor.html`
- `docs/autenticacao.md`
- `docs/seguranca.md`
- `apps/seguranca/`

## Lucas sureira - Sinistros, processos de sistema e dados do usuário

Responsável pelos cadastros de sinistro, processos de sistema e requisito LGPD relacionado ao controle de dados do usuário, incluindo direito de exclusão e atualização dos dados pessoais.

Pastas/arquivos de responsabilidade:
- `apps/sinistros/`
- `templates/sinistros/`
- `media/anexos_sinistros/`
- `apps/core/`
- `apps/lgpd/views.py`
- `apps/lgpd/forms.py`
- `apps/lgpd/services.py`
- `apps/lgpd/exports.py`
- `templates/lgpd/meus_dados.html`
- `templates/lgpd/solicitar_exclusao.html`
- `templates/lgpd/portabilidade.html`

## Pacheco - Requisitos LGPD gerais

Responsável pelos requisitos gerais de LGPD, políticas, termos, auditoria e conformidade do sistema.

Pastas/arquivos de responsabilidade:
- `docs/lgpd.md`
- `docs/auditoria.md`
- `docs/testes-seguranca.md`
- `apps/lgpd/`
- `templates/lgpd/politica_privacidade.html`
- `templates/lgpd/aceite_termos.html`
- `apps/auditoria/`

## Matheus Deu pro térian - Dashboard e assets visuais

Responsável pelo desenvolvimento da dashboard e pelos templates visuais, imagens de background, ícones, arquivos PNG, schemas visuais e demais assets gráficos.

Pastas/arquivos de responsabilidade:
- `apps/dashboard/`
- `templates/dashboard/`
- `apps/dashboard/templates/`
- `static/img/`
- `media/`
- `static/css/app.css`
- `templates/base.html`
- `templates/partials/`

