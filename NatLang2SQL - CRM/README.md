# CRM Automatizado com Multi-Agentes de IA e Consulta Natural a SQL

**Repositório para um sistema de demonstração de CRM inteligente** utilizando Python, SQLite, Streamlit e orquestração multi-agente baseada em LangGraph/LangChain.  
_Aborda desde a geração automática do banco, povoamento de dados simulados até a interface interativa orientada por IA, incluindo integração com LLMs (Groq/Llama3, OpenAI GPT)._

---

## Sumário Executivo

Este projeto é um _Proof-of-Concept (PoC)_ para automação e consulta de bancos de dados CRM via linguagem natural, implementando um fluxo de **assistentes de IA** (multi-agentes) capazes de interpretar perguntas, transformar em SQL e executar sobre base de dados local — tudo via interface Streamlit responsiva.  
**Propósito:** Reduzir a dependência de conhecimento técnico em SQL para equipes de negócio e acelerar discovery de insights em dados de clientes.

---

## Arquitetura & Componentes

- **Banco de Dados**:  
  - SQLite (`crm_database.db`): duas tabelas principais, `tb_clientes` e `tb_interacoes` (clientes, status, interações e metadados).
- **Scripts de Inicialização**:  
  - `create_db.py`: cria e popula o banco de dados automaticamente com clientes e interações de exemplo.
- **Backend e Orquestração**:
  - `main.py`: aplicação Streamlit, implementando agentes via LangChain/LangGraph, roteamento dinâmico, execução de queries e exibição do histórico conversacional.
  - Agentes distintos para LLMs OpenAI (GPT) e Groq (Llama3), com alternância lógica e fallback robusto.
- **Gerenciamento de Dependências**:  
  - `pyproject.toml`: gestão moderna de dependências, aderente a melhores práticas (poetry, PEP 621, etc.).

---

## Instruções de Instalação

### 1. **Pré-requisitos**

- Python 3.10+
- (Opcional) Ambiente virtual recomendado
- Acesso local para execução dos modelos LLM (LM Studio/Ollama) **OU** API key válida para Groq/OpenAI

### 2. **Instale as dependências**
```bash
pip install -r requirements.txt
# ou
pip install .
```
(_A lista de dependências críticas inclui: `streamlit`, `langchain`, `langchain-groq`, `langchain-openai`, `langgraph`, `sqlalchemy`, `dotenv`_)

### 3. **Gere o banco de dados**
```bash
python create_db.py
```
_Script idempotente: pode ser executado múltiplas vezes sem corromper dados já existentes._

### 4. **Execute a aplicação**
```bash
streamlit run main.py
```
_Acesse o app localmente via browser (default: `http://localhost:8501`)._

---

## Como Utilizar

- Pergunte na interface, **em linguagem natural**:  
  Exemplos:
  - “Quais clientes estão ativos?”
  - “Quais interações ocorreram com João Silva?”
  - “Quais clientes são leads?”
  - “Mostre interações do tipo e-mail realizadas na última semana.”
- O sistema interpreta, converte para SQL seguro, executa e exibe resultados na interface.

---

## Estrutura do Banco de Dados

- **tb_clientes**  
  - `customer_id` (PK, autoincremento)
  - `name`, `email` (único), `phone`, `company`
  - `status` (`Lead`, `Active`, `Inactive`, `Prospect`)
  - `created_at` (timestamp)
- **tb_interacoes**
  - `interaction_id` (PK)
  - `customer_id` (FK para tb_clientes)
  - `interaction_date` (timestamp)
  - `type` (`Email`, `Call`, `Meeting`, `Note`)
  - `notes` (texto)

---

## Lógica de Orquestração Multi-Agente

- **Roteamento Dinâmico**: Alternância entre agentes OpenAI e Groq, usando lógica customizada para redundância, validação cruzada e fallback em caso de erro.
- **Execução de SQL Restrito**: Somente consultas `SELECT` permitidas, mitigando riscos de manipulação/dano ao banco (governança básica de segurança).
- **Histórico Conversacional**: Toda a interação é registrada e pode ser revisitada pelo usuário (com separação clara do papel dos agentes e das ferramentas).

---

## Governança, Limitações e Avisos Críticos

- **Não usar em produção** sem validação adicional — este projeto é _experimental_, não audita input malicioso e não implementa autenticação avançada.
- **LLMs podem cometer erros e alucinações**: **Nunca** delegue decisões críticas sem double-check humano.  
- **Política de segurança básica**: apenas SELECT é permitido, mas não há isolamento ou restrição avançada de queries (não atenderia a requisitos regulatórios sérios, como LGPD em produção).
- **Customização necessária** para ambientes enterprise (ex: LGPD, integração com AD/LDAP, logging estruturado, APIs REST).

---

## Roadmap e Possíveis Extensões

- Integração com bancos SQL corporativos (PostgreSQL, SQL Server)
- Autenticação/Autorização (OAuth2, SSO, RBAC)
- Logging avançado e dashboards de uso
- Validação de queries via LLM + política estática
- Integração direta com canais (Slack, Teams, WhatsApp)

---

## Estrutura dos Arquivos

```plaintext
.
├── create_db.py         # Criação e povoamento do banco de dados SQLite
├── main.py              # Backend e interface Streamlit com IA
├── crm_database.db      # Banco de dados local (gerado pelo script)
├── pyproject.toml       # Dependências (formato moderno PEP 621)
├── README.md            # (Este arquivo)
```

---

## Reconhecimentos & Autoria

- **Frameworks**: [Streamlit](https://streamlit.io/), [LangChain](https://python.langchain.com/), [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Modelos LLM**: [OpenAI GPT](https://platform.openai.com/), [Groq Llama3](https://groq.com/)

---

## Disclaimer

Este projeto é uma **demonstração técnica**. Não oferece garantias de estabilidade, segurança nem aderência a compliance corporativo avançado. Use sob sua própria responsabilidade.

---

## Contato

Sugestões, críticas construtivas ou contribuições:  
_Felipe Meganha_
