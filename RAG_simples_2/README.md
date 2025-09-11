# Analisador Inteligente de Contratos com Multi-Agentes e RAG

**Sistema Web para Análise Automatizada de Documentos Contratuais via IA Generativa, RAG (Retrieval-Augmented Generation) e Multi-Agentes com LangGraph**

---

## Visão Geral

O projeto consiste em uma aplicação Flask para análise inteligente de contratos/documentos, unindo RAG, multi-agentes, LLMs e interface moderna. Utiliza LangGraph para orquestração do fluxo, FAISS como vector store, embeddings de estado-da-arte via HuggingFace, e Groq para chamadas de modelos LLM (Qwen, Llama3).

O sistema permite que o usuário envie perguntas sobre contratos/documentos PDF, e recebe análises em três etapas: resumo, raciocínio lógico e resposta final, com acompanhamento de progresso.

---

## Principais Diferenciais

- **Arquitetura Multi-Agentes**: Pipeline baseado em três agentes especialistas: DocumentAgent (resumo), ReasoningAgent (análise lógica), MetaAgent (resposta final).
- **RAG Completo**: Documentos PDF são lidos, divididos, embeddados (BAAI/bge-base-en), indexados em FAISS e consultados via similaridade vetorial.
- **Interface Moderna**: Front-end elegante, responsivo e funcional, pronto para uso profissional, com feedback em tempo real e status detalhado.
- **Pipeline Assíncrono**: Consultas processadas em background, com status e progresso exibidos para o usuário.
- **Stack Tecnológica Atual**: Integração com Groq, LangChain, HuggingFace, FAISS, Flask 3+, Python 3.10+, dotenv, etc.

---

## Estrutura dos Componentes

```
├── app.py              # Backend Flask principal e rotas
├── agentes/
│   └── agent.py        # Implementação dos agentes (Document, Reasoning, Meta)
├── utilitarios/
│   └── RAG.py          # Classe do modelo RAG (carrega PDFs, embeddings, vectorDB)
├── templates/
│   └── index.html      # Interface Web (HTML+JS+CSS embutido)
├── .env                # Variáveis de ambiente (SECRET_KEY, GROQ_API_KEY)
├── pyproject.toml      # Dependências e metadados do projeto
```

---

## Como Funciona

1. **Upload de Documentos**: PDFs são carregados na pasta `dados/documentos/` (pasta padrão esperada pelo sistema).
2. **Indexação e Embedding**: Documentos são divididos em chunks, embeddados (`BAAI/bge-base-en`), indexados no FAISS.
3. **Pergunta do Usuário**: O usuário digita perguntas via Web, por exemplo, “Quais são as cláusulas de rescisão?”.
4. **Orquestração Multi-Agentes** (LangGraph):
    - **DocumentAgent**: Recupera e sumariza os chunks mais relevantes.
    - **ReasoningAgent**: Analisa criticamente o resumo.
    - **MetaAgent**: Gera a resposta final consolidada para o usuário.
5. **Interface e Feedback**: Usuário acompanha o progresso em tempo real e visualiza o resultado da análise via interface moderna.

---

## Instalação e Execução

> **Pré-requisitos:**  
> - Python >= 3.10  
> - (Recomendado) Ambiente virtual  
> - API Key Groq (para LLMs)  

1. **Clone o projeto e acesse a pasta**

   ```bash
   git clone <repo-url>
   cd <repo>
   ```

2. **Crie o ambiente virtual e instale dependências**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   # ou
   pip install .
   ```

3. **Configure as variáveis de ambiente**

   Copie `.env.example` para `.env` e preencha `GROQ_API_KEY` e `SECRET_KEY`.

4. **Adicione os PDFs em `dados/documentos/`**

   > Os PDFs presentes nessa pasta serão indexados automaticamente na primeira execução.

5. **Execute o servidor Flask**

   ```bash
   python app.py
   ```

   Acesse: [http://localhost:5000](http://localhost:5000)

---

## Fluxo de Processamento

1. **/ask**: Recebe a pergunta, inicia thread assíncrona, gera session_id e começa a análise.
2. **/progress**: Endpoint consultado via JS para mostrar status, progresso, resumo e resposta final.
3. **/health**: Endpoint para healthcheck e debugging.

---

## Tecnologias Utilizadas

- **Flask 3+**
- **FAISS (Vector Store)**
- **LangChain / LangGraph**
- **HuggingFace Embeddings**
- **Groq LLMs (Qwen, Llama-3)**
- **PyMuPDF**
- **dotenv-python**
- **Frontend HTML/CSS/JS moderno** (sem dependências pesadas)

---

## Exemplo de Uso

1. Adicione contratos PDF na pasta `dados/documentos/`
2. Execute o sistema
3. No browser, pergunte:
    - “Quais as cláusulas de multa?”
    - “Existem previsões de reajuste?”
    - “Qual o prazo de vigência?”
4. O sistema retorna:
    - Resumo dos documentos relevantes
    - Raciocínio lógico (interno)
    - Resposta final consolidada

---

## Roadmap / Possíveis Extensões

- Upload dinâmico de documentos
- Autenticação de usuários
- Resposta detalhada via chat
- Exportação de respostas (.docx, .pdf)
- Logging avançado e auditoria

---

## Observações Executivas e Recomendações

- **Performance**: Para bases grandes de documentos, recomenda-se instâncias com maior memória.
- **Compliance**: Não armazene contratos sensíveis sem garantir segurança adequada.
- **Customização**: É possível alterar agentes, embeddings ou lógica dos fluxos no backend facilmente.
- **Deploy**: Aplicação pronta para containerização Docker e deploy em nuvem, se necessário.

---

## Dependências (pyproject.toml)

```toml
[project]
name = "cap14"
requires-python = ">=3.10"
dependencies = [
    "dotenv-python>=0.0.1",
    "faiss-cpu>=1.12.0",
    "flask>=3.1.2",
    "flask-cors>=6.0.1",
    "flask-session==0.5.0",
    "groq>=0.31.1",
    "langchain>=0.3.27",
    "langchain-community>=0.3.29",
    "langchain-huggingface>=0.3.1",
    "langgraph>=0.6.7",
    "pymupdf>=1.26.4",
    "python-dotenv>=1.1.1",
    "sentence-transformers>=5.1.0",
]
```
---

## Licença

Uso acadêmico e experimental. Para produção, revise pontos de compliance, LGPD e segurança de API Keys.