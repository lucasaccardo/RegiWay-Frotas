# Arquitetura
<!-- Responsável: Todos os membros. -->

O sistema segue o padrão MVT do Django, dividido em apps por domínio. Cada app cuida de uma responsabilidade separada para facilitar manutenção.

---

## Apps do projeto

| App | O que faz |
|---|---|
| `accounts` | Login, logout, recuperação de senha |
| `frotas` | Cadastro e gestão de veículos |
| `sinistros` | Registro e acompanhamento de sinistros |
| `lgpd` | Termos, consentimento, portabilidade e exclusão |
| `auditoria` | Registro de eventos críticos (login, alterações etc.) |
| `seguranca` | Utilitários de criptografia e headers HTTP |
| `dashboard` | Painel com indicadores operacionais |
| `core` | Modelos abstratos e utilitários compartilhados |

---

## Fluxo básico de uma requisição

```
Usuário → URL Router → Middleware → View → Model → Template → Resposta
```

Os middlewares importantes são:
- `CsrfViewMiddleware` — valida CSRF em todo POST
- `SessionMiddleware` — gerencia sessões
- `ConsentimentoObrigatorioMiddleware` — redireciona quem não aceitou os termos (LGPD)
- `AuditoriaMiddleware` — registra respostas 403

---

## Decisões de design

**Por que separar em apps?**
Cada membro da equipe ficou responsável por um domínio, então fez sentido separar. Também facilita encontrar o código depois.

**Por que usar services.py?**
Views ficam menores. A lógica de negócio (ex: cadastrar veículo, excluir conta) fica em `services.py` e pode ser testada sem precisar de requisição HTTP.

**Por que Signals para auditoria?**
Os eventos de login/logout são capturados por signals do próprio Django, sem precisar modificar cada view individualmente.

---

## Banco de dados

Usamos SQLite no desenvolvimento e está previsto PostgreSQL para produção. O acesso é feito pelo ORM do Django, sem SQL direto nas views.

---

## Deploy (previsto)

A configuração de produção (`config/settings/production.py`) já tem HTTPS obrigatório, cookies seguros e HSTS configurados. O deploy está previsto no Render. Ver `docs/deploy-render.md`.
