# 📄💬 Assistente RAG com PDFs (Retrieval-Augmented Generation)

Este projeto implementa um pipeline de **RAG (Retrieval-Augmented Generation)** utilizando **LangChain**, **FAISS**, **HuggingFace Embeddings** e **Streamlit**, permitindo a realização de perguntas em linguagem natural sobre documentos PDF carregados pelo usuário.

---

## 🚀 Funcionalidades

- Upload de arquivos PDF diretamente pela interface web.
- Segmentação semântica dos documentos com `SemanticChunker`.
- Vetorização dos chunks com `HuggingFaceEmbeddings` e armazenamento em `FAISS`.
- Respostas geradas por LLM (via API compatível com OpenAI) com suporte a *source attribution*.
- Interface interativa construída com `Streamlit`.

---

## 🧱 Estrutura do Projeto

```
├── main.py                   # Interface Streamlit
├── rag_system.py            # Classe RAGSystem com toda a lógica do pipeline
├── requirements.txt         # Dependências do projeto
└── README.md                # Este documento
```

---

## 🧠 Tecnologias Utilizadas

- **LangChain** (`langchain`, `langchain_community`, `langchain_openai`, `langchain_experimental`)
- **FAISS** – indexação vetorial local
- **HuggingFaceEmbeddings** – modelo de embedding textual
- **ChatOpenAI** – LLM customizado (via endpoint local)
- **PDFPlumberLoader** – para leitura de PDFs
- **Streamlit** – para frontend interativo

---

## ⚙️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu_usuario/rag-pdf-assistant.git
cd rag-pdf-assistant
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

> ⚠️ Certifique-se de que o endpoint da LLM está rodando (por exemplo, LM Studio em `http://192.168.0.27:1234/v1`).

### 3. Execute a aplicação Streamlit

```bash
streamlit run main.py
```

---

## 📌 Parâmetros Importantes

Na classe `RAGSystem`, é possível configurar:

- `model_name`: Nome do modelo LLM compatível com OpenAI.
- `api_base`: URL do endpoint da LLM.
- `api_key`: Chave de autenticação (ou identificador de uso).
- `k_retrieval`: Número de chunks mais similares retornados pelo FAISS.

---

## ✅ Exemplo de Uso

1. Faça upload de um PDF via interface Streamlit.
2. Aguarde a construção do pipeline.
3. Digite uma pergunta relacionada ao conteúdo.
4. Receba a resposta com a indicação das fontes utilizadas (trechos do PDF).

---

## 🔒 Considerações de Segurança

- O código roda **localmente** e não envia arquivos ou textos para servidores externos (a menos que o endpoint LLM seja remoto).
- Ideal para uso em ambientes controlados, como laboratórios, clínicas, ambientes acadêmicos ou ambientes hospitalares com restrição de dados.

---

## 📚 Créditos e Inspiração

Este projeto foi inspirado por arquiteturas modernas de RAG utilizadas em soluções corporativas, adaptando pipelines do LangChain para cenários on-premise e edge.

---

## 🧾 Licença

Este projeto está sob a licença MIT – sinta-se livre para utilizar, modificar e redistribuir.