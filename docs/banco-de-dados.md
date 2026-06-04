# Banco de dados
<!-- Responsável: João Pedro. -->

Documenta as entidades do sistema, seus campos e relacionamentos.

---

## Configuração

Desenvolvimento: SQLite (arquivo `db.sqlite3` na raiz).
Produção: previsto PostgreSQL via `psycopg[binary]`.

Todo acesso ao banco é feito pelo ORM do Django, sem SQL nas views.

---

## Entidades

### Veiculo — `apps/frotas`

Armazena os veículos da frota. Os campos `placa`, `renavam` e `chassi` são únicos e normalizados antes de salvar (sem traço, sem espaço, maiúsculo).

| Campo | Tipo | Obs |
|---|---|---|
| placa | CharField(8) | unique |
| renavam | CharField(11) | unique, só números |
| chassi | CharField(17) | unique |
| marca | CharField(80) | |
| modelo | CharField(80) | |
| ano | PositiveIntegerField | entre 1950 e ano atual +1 |
| cor | CharField(40) | opcional |
| anexo | FileField | PDF/JPG/PNG, máx 5 MB |
| observacao | TextField | opcional |
| criado_por | FK → User | PROTECT |
| criado_em | DateTimeField | automático |
| atualizado_em | DateTimeField | automático |

### Sinistro — `apps/sinistros`

Registro de sinistros e avarias. O status acompanha o andamento do chamado.

| Campo | Tipo | Obs |
|---|---|---|
| placa | CharField(10) | |
| chassi | CharField(17) | opcional |
| cliente | CharField(200) | |
| telefone_contato | CharField(20) | opcional |
| data_ocorrencia | DateField | |
| descricao | TextField | |
| status | CharField | Aberto / Em Andamento / Concluído / Recusado |
| documento_anexo | FileField | opcional |
| responsavel | FK → User | PROTECT |
| criado_em | DateTimeField | via BaseModel |
| atualizado_em | DateTimeField | via BaseModel |

### EventoAuditoria — `apps/auditoria`

Log imutável de ações. Não pode ser editado nem excluído (configurado no Admin).

| Campo | Tipo | Obs |
|---|---|---|
| usuario | FK → User | SET_NULL (preserva log se usuário for excluído) |
| tipo | CharField | login, logout, login_falhou, alteracao, exclusao, acesso_negado, exportacao, solicitacao_lgpd, outro |
| descricao | TextField | |
| ip | GenericIPAddressField | nullable |
| caminho | CharField(500) | rota acessada |
| objeto_tipo | CharField | ex: "Veiculo" |
| objeto_id | CharField | PK do objeto |
| dados_extras | JSONField | informações adicionais |
| criado_em | DateTimeField | automático |

### TermoVigente — `apps/lgpd`

Armazena o texto do termo de uso atual. Só um fica com `vigente=True` por vez (controle manual pelo admin).

### ConsentimentoUsuario — `apps/lgpd`

Registra quando o usuário aceitou os termos, com data e IP.

### SolicitacaoTitular — `apps/lgpd`

Registra pedidos de exclusão, portabilidade ou retificação de dados. Status: pendente → em_andamento → concluida/recusada.

---

## Relacionamentos principais

```
User → Veiculo (criado_por, PROTECT)
User → Sinistro (responsavel, PROTECT)
User → EventoAuditoria (usuario, SET_NULL)
User → ConsentimentoUsuario (usuario, CASCADE)
User → SolicitacaoTitular (usuario, SET_NULL)
TermoVigente → ConsentimentoUsuario (termo, PROTECT)
```

**Por que PROTECT e não CASCADE em Veiculo e Sinistro?**
Para não perder os registros operacionais caso um funcionário seja desligado. O registro fica, mas o usuário pode ser desativado.

**Por que SET_NULL em EventoAuditoria?**
O log de auditoria precisa ser preservado mesmo se o usuário for excluído (obrigação legal).

---

## Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```
