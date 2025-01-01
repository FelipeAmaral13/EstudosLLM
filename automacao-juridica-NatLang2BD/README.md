
# **Consulta Jurídica Usando Linguagem Natural no SQL**

Este projeto utiliza inteligência artificial (IA) e processamento de linguagem natural (NLP) para transformar perguntas jurídicas em linguagem natural em consultas SQL, permitindo que usuários obtenham respostas precisas diretamente de um banco de dados jurídico relacional. A aplicação é desenvolvida com **Streamlit**, **PostgreSQL**, **LangGraph** e **LLMs (Large Language Models)** para oferecer uma solução robusta, eficiente e acessível.

---

## **Índice**
- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Descrição dos Componentes](#descrição-dos-componentes)
  - [Interface com o Usuário (Streamlit)](#interface-com-o-usuário-streamlit)
  - [Tradução de Perguntas para SQL (Question2SQL)](#tradução-de-perguntas-para-sql-question2sql)
  - [Banco de Dados Jurídico (PostgreSQL)](#banco-de-dados-jurídico-postgresql)
  - [Fluxo de Trabalho Inteligente (LangGraph)](#fluxo-de-trabalho-inteligente-langgraph)
- [Como Usar](#como-usar)
- [Exemplo Prático](#exemplo-prático)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## **Visão Geral**

O objetivo do projeto é simplificar o acesso a dados jurídicos estruturados, permitindo que profissionais jurídicos insiram perguntas em linguagem natural e recebam respostas rápidas e precisas. A aplicação combina tecnologias de IA com consultas SQL para criar uma experiência fluida e poderosa.

---

## **Tecnologias Utilizadas**

- **Python 3.9+**
- **Streamlit:** Para desenvolvimento da interface do usuário.
- **PostgreSQL:** Para armazenamento e manipulação de dados jurídicos.
- **LangGraph:** Para gerenciamento do fluxo de trabalho de geração, validação e revisão de consultas SQL.
- **LLMs (Large Language Models):** Para interpretar perguntas em linguagem natural e gerar consultas SQL.
- **dotenv:** Para gerenciamento de variáveis de ambiente.
- **psycopg2:** Para integração com o banco de dados PostgreSQL.

---

## **Funcionalidades**

1. Transformar perguntas em linguagem natural em consultas SQL.
2. Executar consultas SQL diretamente em um banco de dados jurídico.
3. Exibir respostas claras e organizadas ao usuário.
4. Revisar e ajustar automaticamente consultas SQL geradas.
5. Histórico de interações exibido diretamente na interface.

---

## **Instalação**

### **Pré-requisitos**

- Python 3.9+ instalado.
- PostgreSQL instalado e configurado.
- Credenciais de banco de dados no arquivo `.env`.

### **Passos**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/consulta-juridica-sql.git
   cd consulta-juridica-sql
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o banco de dados:**
   Crie um arquivo `.env` com as credenciais do banco:
   ```
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=sistema_juridico
   OPENAI_API_KEY=sua_chave_openai
   ```

4. **Inicialize o banco de dados:**
   Execute o script `db.py` para criar as tabelas e popular os dados simulados:
   ```bash
   python database/db.py
   ```

5. **Inicie a aplicação:**
   ```bash
   streamlit run main.py
   ```

---

## **Estrutura do Projeto**

```plaintext
project_root/
│
├── database/
│   ├── data_base.py          # Gerencia conexão com o PostgreSQL e criação de tabelas.
│   ├── dados.py              # Dados simulados para popular o banco de dados.
│   ├── db.py                 # Inicializa o banco e insere dados.
│
├── flows/
│   ├── workflow.py           # Define o fluxo de geração e validação de SQL com LangGraph.
│
├── models/
│   ├── agent_state.py        # Estrutura o estado dos agentes para o fluxo de trabalho.
│
├── service/
│   ├── llm_services.py       # Integra com LLMs para geração e validação de consultas SQL.
│
├── main.py                   # Interface do usuário com Streamlit.
├── question_sql.py           # Classe principal para transformar perguntas em SQL.
├── .env                      # Variáveis de ambiente (credenciais, chaves de API).
├── requirements.txt          # Dependências do projeto.
└── README.md                 # Documentação geral do projeto.
```

---

## **Descrição dos Componentes**

### **Interface com o Usuário (Streamlit)**
A interface permite que usuários insiram perguntas de forma intuitiva e visualizem respostas diretamente na tela.

#### **Código Principal**
```python
import streamlit as st
from question_sql import Question2SQL

# Inicializar o sistema
question_to_sql = Question2SQL()

st.title("Consulta Jurídica usando linguagem natural no SQL")
st.write("Digite sua pergunta jurídica e obtenha os resultados diretamente do banco de dados.")
```

---

### **Tradução de Perguntas para SQL (Question2SQL)**
A classe `Question2SQL` gerencia a conversão de perguntas em consultas SQL, utilizando fluxos inteligentes para validação e ajustes.

#### **Código Principal**
```python
class Question2SQL:
    def set_question(self, question):
        self.initial_state['question'] = question

    def extract_sql(self, query_text):
        match = re.search(r'```sql\s*(.*?)\s*```', query_text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            return query_text.strip()
```

---

### **Banco de Dados Jurídico (PostgreSQL)**
O banco armazena informações estruturadas, como clientes, advogados, casos e audiências.

#### **Criação de Tabelas**
```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    cpf VARCHAR(11) UNIQUE
);

CREATE TABLE advogados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    oab VARCHAR(15) UNIQUE
);
```

---

### **Fluxo de Trabalho Inteligente (LangGraph)**
Gerencia as etapas de geração, validação e refinamento das consultas SQL.

#### **Código Principal**
```python
builder = StateGraph(AgentState)
builder.add_node("initialize_database", initialize_database_state)
builder.add_edge("initialize_database", "sql_writer")
```

---

## **Como Usar**

1. Abra a aplicação no navegador após iniciar o Streamlit.
2. Insira perguntas jurídicas no campo designado, como:
   ```
   Quais advogados possuem casos em andamento?
   ```
3. Visualize a resposta na interface em segundos.

---

## **Exemplo Prático**

**Pergunta:**  
*"Quais clientes possuem audiências agendadas para os próximos 30 dias?"*  

**SQL Gerado:**  
```sql
SELECT * 
FROM clientes 
WHERE id IN (
    SELECT cliente_id 
    FROM audiencias 
    WHERE data BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
);
```

---

## **Contribuição**

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias.

---

## **Licença**

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE` para mais informações.
