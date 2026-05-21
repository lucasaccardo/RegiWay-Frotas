# Frotas
<!-- Responsável: Todos os membros. -->

Funcao: documentacao inicial do sistema de gestao de frotas, sinistros, LGPD e auditoria.
# RegiWay Frotas: Sistema Intregrado de Gestão

## Visão Geral 
A **RegiWay Frotas** é um sistema corporativo web desenvolvido com intuito de otimizar a gestão de veiculos, controle de sinistros e acompanhamento operacional.
A platafroma foi arquitetada com foco em segurança da informação, rastreabiliade (Auditoria)  e conformidade integral com a Lei Geral de Proteção de Dados (LGPD).

---
## Arquitetura do Sistema 
O sistema utiliza a arquitetura **MVT(Model-View-Template)** nativo do framewoork Django que separa todo parte de banco de dados no Model que gerenciam e estruturam os dados dentro da aplicação, o View que faz a interpretação das requisições dos usuarios e retornar para eles no Template que mostrando os dados das requisições.

## Gestão Operacional de Sinistros
<!-- Lucas e Pacheco. -->
O módulo de Sinistros foi estruturado para garantir o acompanhamento da ocorrências veiculares da Frota.
O desenvolvimento focou na integridade da informação, no controle de fluxo de trabalho e na restreabilidade operacional.

**Principais Implementações:**
* **Ciclo de Vida (CRUD Dinâmico):** Sistema completo e otimizado para criação, leitura, edição e controle de status de sinistros, permitindo aos gestores uma resposta àgil aos incidentes.
* **Histórico e Imutalidade:**
  Implementação de regas de negócio para garantir que o histórico de transições de status e movimentções entre setores seja inviolável.
* **Gestão Eletrônica de Documentos (GED):**
  **Modulo de uploads seguros com validação de extensão e tamanho, permitindo o arquivamento organizado de fotos, boletins de ocorrência e orçamentos.
### Conformidade e Privacidade de Dados (LGPD)
A segurança jurídica e o respeito à privacidade dos usuários que conduzem o núcleo do RegiWay Frotas. O modulo LGPD foi construido seguindo os principios de *Privacy by Design*.

**Principais Implementaçõe:**
* **Gestã de Consentimento(Opt-in):**
  Sistema de bloqueio via *middleware* que exige o aceite obrigatótio da Política de Privacidade e dos Termos de Uso atualizados.
* **Transparencia e Controle:**
  Painel dedicado para que o titular dos dados possa consultar, revisar e retificar suas informações pessoais a qualquer momento.
* ** Direito ao Esquecimento & Portabilidade:**
  Fluxos automatizados para solicitação de exclusão/anonimização de dados pessoais e ferramentas para exportação de dados estruturados.

## Tecnologias Utilizadas 
* **Back-End:** Python 3, Django 6.0+
* **Front-End:** JavaScript, Django templates
* **Banco de Dados:** PostgreSQL

## Como Executar o Projeto Localmemte 

Para clonar e rodar o projeto na sua maquina local siga estes passos a baixo:

**1. Clone o repositorio:** git clone [https:github.com/seu-usuario/RegiWay-Frotas.git]

**2.Crie e ative o ambiente virtual**
# Para criar o ambiente rode o comando
python -m venv .venv
# Ativar
.\.venv\Scripts\activate
**3. Instalar as depedencias**
pip install -r requirements.txt
**4. Configure as variaveis de ambiente 
Crie uma copia do arquivo .env.example e renomeie para .env 
Rode as migraçoes para criar as tabelas do banco
python manage.py migrate
**5. Inicie o Servidor**
python manage.py runserver



































