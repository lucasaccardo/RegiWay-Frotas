# RegiWay-Frotas

O RegiWay Frotas é uma aplicação web desenvolvida para a gestão operacional, acompanhamento e cadastro de sinistros de frotas de veículos pesados. O sistema atua como um portal centralizado que garante a rastreabilidade dos clientes, a proteção de dados sensíveis e a auditoria contínua dos processos internos.

## Equipe

- João Pedro — Banco de dados
- Kenny — Front-end
- Kenzo — Veículos e autenticação
- Lucas Sureira — Sinistros e dados do usuário
- Pacheco — LGPD e auditoria
- Matheus Deleutério — Dashboard

## O que o sistema faz

- Cadastra e gerencia veículos da frota (com validação de placa, RENAVAM e chassi)
- Registra sinistros e acompanha o status de cada chamado
- Garante conformidade com a LGPD: aceite de termos, exportação de dados e exclusão de conta
- Auditoria automática de login, logout, falhas e acessos negados
- Dashboard com indicadores operacionais
- Sessões com expiração automática (30 min)

## Como rodar localmente

```bash
git clone <url-do-repo>
cd RegiWay-Frotas

python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000`

## Estrutura de pastas

```
apps/
  accounts/    autenticação
  frotas/      cadastro de veículos
  sinistros/   registro de sinistros
  lgpd/        conformidade LGPD
  auditoria/   trilha de eventos
  seguranca/   criptografia e headers
  dashboard/   painel gerencial
  core/        base compartilhada
config/
  settings/
    base.py         configurações compartilhadas
    development.py  desenvolvimento
    production.py   produção (HTTPS, cookies seguros)
docs/          documentação técnica
templates/     templates HTML
```

## Rodando os testes

```bash
python manage.py test
```

## Documentação

Toda a documentação técnica está na pasta `docs/`. Ver `docs/arquitetura.md` para começar.

## Tecnologias

Python 3 / Django 6 / SQLite (dev) / Bootstrap 5
