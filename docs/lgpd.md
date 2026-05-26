# LGPD
<!-- Responsável: Pacheco, Lucas sureira. -->

Funcao: documentar consentimento, direitos do titular, exclusao, anonimizacao e portabilidade.

---

## Visão Geral

O sistema RegiWay Frotas trata dados pessoais de usuários e motoristas em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018 — LGPD). Esta documentação descreve como os requisitos legais foram implementados no sistema.

---

## Consentimento

O consentimento é coletado no primeiro acesso do usuário autenticado, por meio da tela de **aceite de termos** (`/lgpd/aceite-termos/`).

- O modelo `TermoVigente` armazena o texto vigente da política.
- O modelo `ConsentimentoUsuario` registra o aceite com data, IP e referência ao termo.
- O middleware `ConsentimentoObrigatorioMiddleware` bloqueia o acesso a qualquer rota protegida enquanto o usuário não tiver aceite ativo.
- O usuário pode revogar o consentimento por meio de solicitação formal (`SolicitacaoTitular`).

---

## Direitos do Titular

| Direito | Tipo de Solicitação | Status Possíveis |
|---|---|---|
| Exclusão de dados | `exclusao` | pendente, em_andamento, concluida, recusada |
| Portabilidade | `portabilidade` | pendente, em_andamento, concluida, recusada |
| Retificação | `retificacao` | pendente, em_andamento, concluida, recusada |
| Oposição ao tratamento | `oposicao` | pendente, em_andamento, concluida, recusada |

As solicitações são registradas em `SolicitacaoTitular` e gerenciadas pelo administrador via Django Admin.

---

## Exclusão e Anonimização

- A exclusão de conta apaga ou anonimiza os dados pessoais identificáveis.
- Dados vinculados a obrigações legais (sinistros, auditoria) são anonimizados, não excluídos.
- O prazo legal de resposta a solicitações de exclusão é de **15 dias**.

---

## Portabilidade

- O usuário pode solicitar exportação dos seus dados pessoais em formato legível (JSON ou CSV).
- A exportação é gerada pelo módulo `apps/lgpd/exports.py`.

---

## Bases Legais Utilizadas

| Tratamento | Base Legal (Art. 7º LGPD) |
|---|---|
| Cadastro de usuário | Consentimento (inc. I) |
| Registro de sinistros | Cumprimento de obrigação legal (inc. II) |
| Logs de auditoria | Legítimo interesse / obrigação legal (inc. II e IX) |

---

## Referências

- Lei nº 13.709/2018 — LGPD
- `apps/lgpd/models.py` — modelos TermoVigente, ConsentimentoUsuario, SolicitacaoTitular
- `apps/lgpd/middleware.py` — ConsentimentoObrigatorioMiddleware
- `templates/lgpd/aceite_termos.html` — tela de aceite
- `templates/lgpd/politica_privacidade.html` — política de privacidade
