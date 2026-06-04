# Resumo

**RegiWay Frotas — Sistema de Gestão de Frotas com Conformidade à LGPD**

Autores: João Pedro, Kenny, Kenzo, Lucas Sureira, Pacheco, Matheus Deleutério
Instituição: [Nome da Faculdade] — [Curso] — [Semestre] 2025

---

Este trabalho apresenta o desenvolvimento do RegiWay Frotas, um sistema web para gestão de frotas corporativas e registro de sinistros, com conformidade à Lei Geral de Proteção de Dados (LGPD, Lei nº 13.709/2018). O sistema foi desenvolvido com Django 6 e organizado em oito apps independentes: `accounts`, `frotas`, `sinistros`, `lgpd`, `auditoria`, `seguranca`, `dashboard` e `core`.

As principais funcionalidades incluem o cadastro de veículos com validação de placa, RENAVAM e chassi; o registro e acompanhamento de sinistros por status; e o controle de dados pessoais conforme a LGPD. Para a conformidade legal, foram implementados um middleware de consentimento obrigatório, a funcionalidade de portabilidade de dados via exportação CSV e a anonimização de dados pessoais para o exercício do direito ao esquecimento.

A auditoria do sistema registra automaticamente eventos de login, logout, falhas de autenticação e acessos negados, utilizando os Signals e Middlewares do Django. O histórico é imutável e preservado mesmo após exclusão de usuários.

Em termos de segurança, foram aplicadas proteção CSRF em todos os formulários, configuração de sessões com expiração por inatividade, headers HTTP de segurança para produção e validadores de senha. Ficaram planejadas para iterações futuras: autenticação em dois fatores, proteção contra força bruta com django-axes e criptografia em repouso para campos sensíveis.

Os testes automatizados cobrem os módulos de auditoria, LGPD, sinistros e autenticação, totalizando 51 testes. A documentação técnica abrange arquitetura, banco de dados, autenticação, segurança, LGPD, auditoria, testes e deploy.

**Palavras-chave:** gestão de frotas, sinistros, LGPD, segurança web, Django, auditoria.

---

**Abstract**

This paper presents the development of RegiWay Frotas, a web system for corporate fleet management and accident registration, compliant with Brazil's General Data Protection Law (LGPD). The system was built with Django 6 and structured in eight independent apps. Key features include vehicle registration with plate, RENAVAM and chassis validation; accident tracking with status history; and personal data control per LGPD requirements. A mandatory consent middleware, CSV data export for portability, and account anonymization for the right to erasure were implemented. An immutable audit trail logs authentication events and access denials automatically via Django Signals. Security measures include CSRF protection, session expiration, HTTP security headers, and password validators.

**Keywords:** fleet management, LGPD, web security, Django, audit trail.
