
# 🤖 Agentic RAG Jurídico

Um agente de IA baseado em **LangGraph** e **LangChain**, especializado em **analisar contratos legais em PDF**. O sistema realiza recuperação de contexto via busca vetorial (FAISS), formatação com metadados e geração de respostas com LLM local (via LM Studio ou outro backend compatível com OpenAI API).

---

## 🧠 Visão Geral

> “Transforme documentos jurídicos não estruturados em conhecimento acessível via linguagem natural.”

Este agente é capaz de:
- Carregar e indexar arquivos PDF de contratos;
- Fragmentar documentos e construir um índice vetorial (FAISS);
- Recuperar automaticamente os trechos mais relevantes para uma pergunta;
- Gerar respostas contextualizadas usando um modelo LLM local (Meta Llama 3, por exemplo);
- Informar a origem da resposta com base nos metadados dos documentos.

---

## 🔧 Tecnologias Utilizadas

| Tecnologia       | Finalidade                                |
|------------------|--------------------------------------------|
| LangChain        | Pipeline de RAG e abstração de LLMs        |
| LangGraph        | Orquestração baseada em fluxo de estados   |
| FAISS            | Vetorização e busca semântica              |
| HuggingFace Hub  | Modelo de embedding (`all-mpnet-base-v2`)  |
| LM Studio / vLLM | Backend para servir modelos Llama 3        |
| PyPDFLoader      | Carregamento e parsing de PDFs             |

---

## 📁 Estrutura do Projeto

```bash
project/
├── main.py                      # Interface CLI do agente
├── agentic_RAG.py              # Classe principal do sistema RAG
├── workflow.py                 # Definição do fluxo LangGraph
│
├── agent/
│   ├── agent_state.py
│   └── recupera_documentos.py
│
├── LLM/
│   ├── formata_contexto.py
│   ├── gera_resposta.py
│   ├── prompt.py
│   └── llm_model.py
│
├── documentos/                 # Pasta com contratos em PDF
└── dsavectordb/                # Base vetorial FAISS (gerada automaticamente)
```

---

## ▶️ Como Executar

### 1. **Pré-requisitos**
- Python 3.10+
- Modelo LLM rodando via LM Studio, vLLM, Ollama ou OpenRouter
- Instalar dependências:

```bash
pip install -r requirements.txt
```

### 2. **Preparar a pasta de documentos**
Coloque seus arquivos PDF de contrato dentro da pasta `documentos/`. Exemplo:

```bash
project/
├── documentos/
│   ├── contrato_1.pdf
│   └── contrato_2.pdf
```

### 3. **Executar**
No terminal:

```bash
python main.py
```

Você verá:

```
--- Inicializando o Agente de Contratos ---
Digite sua pergunta sobre os contratos (ou digite 'sair' para encerrar):
> Qual o prazo de vigência do contrato com a empresa X?
```

---

## 🧭 Fluxo LangGraph

O fluxo é composto por 3 nós principais:

```
[ retrieve ] → [ format_context ] → [ generate ] → [ END ]
```

- **retrieve**: busca os trechos relevantes com base na pergunta
- **format_context**: concatena os trechos e adiciona metadados
- **generate**: gera a resposta com base no contexto e na pergunta

---

## ⚙️ Configuração do LLM

A comunicação com o modelo segue o padrão da OpenAI API. No arquivo `LLM/llm_model.py`, configure:

```python
model_name = "meta-llama-3.1-8b-instruct@Q4_K_M"
api_base = "http://localhost:1234/v1"
api_key = "lm-studio"
```

---

## 🛡️ Exemplo de Prompt Usado

```text
Você é um assistente de IA especializado em analisar contratos legais.
Use o contexto recuperado dos documentos de contrato abaixo para responder à pergunta.
...
```

---

## 💡 Possíveis Extensões

- 🔁 Histórico de conversa multi-turno
- 🌐 Interface Web com Streamlit ou FastAPI
- 🧠 Persistência de logs de consulta
- 🛑 Filtros por tipo de contrato ou data
- 🔎 Ajuste fino do modelo (finetuning)

---

## 📜 Licença

MIT License. Livre para uso e modificação.

---

## 🤝 Contribuições

Pull requests e sugestões são bem-vindos! Este projeto serve como base educacional e profissional para construção de agentes RAG robustos.
