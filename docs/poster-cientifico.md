# Pôster Científico

**RegiWay Frotas — Sistema de Gestão de Frotas com Conformidade à LGPD**

Autores: João Pedro · Kenny · Kenzo · Lucas Sureira · Pacheco · Matheus Deleutério
Instituição: [Nome da Faculdade] — [Curso] — [Semestre] 2025

---

## Introdução

Com a vigência da LGPD (Lei nº 13.709/2018), empresas que tratam dados pessoais precisam garantir o consentimento do usuário, oferecer meios de portabilidade e exclusão de dados, e manter registros auditáveis das ações realizadas no sistema. Empresas de gestão de frotas lidam com dados pessoais de motoristas, clientes e funcionários, tornando a conformidade legal uma exigência prática e não apenas teórica.

O objetivo deste trabalho foi desenvolver um sistema web para gestão de frotas e sinistros que atenda a esses requisitos de forma integrada, usando o framework Django como base.

---

## Objetivo

Desenvolver e documentar um sistema funcional que:
- Gerencie veículos e sinistros de uma frota corporativa
- Implemente os principais requisitos da LGPD (consentimento, portabilidade, exclusão)
- Mantenha trilha de auditoria de eventos críticos
- Aplique boas práticas de segurança web

---

## Metodologia

O desenvolvimento foi dividido entre os membros da equipe por domínio de responsabilidade. Usamos Django 6 com SQLite em desenvolvimento e Bootstrap 5 no front-end.

A estrutura do sistema é organizada em apps Django independentes, cada um com seus modelos, views, forms e testes. A comunicação entre módulos é feita via services e signals do próprio framework.

Para os requisitos de LGPD, usamos middleware para interceptar requisições de usuários que ainda não aceitaram os termos, e implementamos as funcionalidades de portabilidade (exportação CSV) e exclusão (anonimização dos dados pessoais).

---

## Funcionalidades implementadas

**Gestão de frotas**
Cadastro de veículos com validação de placa (padrão antigo e Mercosul), RENAVAM e chassi. Os identificadores são normalizados automaticamente antes de salvar no banco.

**Sinistros**
Registro de sinistros com placa, cliente, data e descrição. Acompanhamento por status (Aberto → Em Andamento → Concluído). O histórico de alterações de status fica registrado na auditoria.

**LGPD**
- Aceite obrigatório de termos no primeiro acesso (middleware bloqueia acesso sem consentimento)
- Portabilidade: exportação em CSV dos dados pessoais e histórico de sinistros
- Exclusão: anonimização dos dados identificáveis, conta desativada, logs preservados para obrigação legal

**Auditoria**
Registro automático de login, logout, tentativas de acesso negado e alterações de dados. O histórico não pode ser editado nem excluído via Admin.

**Segurança**
Proteção CSRF em todos os formulários, sessões com expiração de 30 minutos, headers de segurança HTTP configurados para produção.

---

## Resultados

O sistema foi desenvolvido com 8 apps Django integrados, cobrindo as funcionalidades de gestão operacional e conformidade legal. Os testes automatizados cobrem os módulos de auditoria, LGPD, sinistros e autenticação (51 testes no total). A documentação técnica cobre arquitetura, banco de dados, autenticação, segurança, LGPD, auditoria e testes.

Das funcionalidades planejadas, ficaram para próximas iterações: autenticação em dois fatores, reCAPTCHA, bloqueio por força bruta e criptografia em repouso para campos sensíveis.

---

## Conclusão

O trabalho demonstrou que é possível atender requisitos de negócio, legais e de segurança em uma mesma base de código, com separação clara de responsabilidades. A LGPD não foi tratada como um módulo isolado, mas integrada ao fluxo principal via middleware e signals, o que reduziu o acoplamento entre os módulos.

---

## Referências

- Lei nº 13.709/2018 — LGPD
- Documentação Django 6 — docs.djangoproject.com
- OWASP Top 10 — owasp.org
