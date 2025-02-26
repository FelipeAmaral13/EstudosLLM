# 📚 GraphRAG com Streamlit

**GraphRAG** é uma aplicação de **Recuperação Aumentada por Geração (RAG)** combinada com **Grafo Semântico** para responder perguntas sobre múltiplos documentos **PDF, DOCX e TXT**.

## 🚀 Funcionalidades
✅ **Upload de documentos** (`.pdf`, `.docx`, `.txt`).  
✅ **Indexação de texto e criação de embeddings** usando **FAISS**.  
✅ **Extração de relações entre entidades** e construção de um **grafo semântico**.  
✅ **Busca vetorial + navegação no grafo** para enriquecer a resposta.  
✅ **Geração de resposta contextualizada** usando **OpenAI (via LangChain)**.  

---

## 📥 Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/seuusuario/graphRAG-streamlit.git
cd graphRAG-streamlit
```

Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
Baixe o modelo do spaCy:
```bash
python -m spacy download pt_core_news_sm
```
🎮 Como Rodar

Execute o aplicativo Streamlit com:
```bash
streamlit run app_streamlit_graphrag.py
```
📂 Estrutura do Projeto
```bash
📁 graphRAG
│── app_streamlit_graphrag.py  # Interface Streamlit para interagir com GraphRAG
│── graphrag.py                # Implementação da classe GraphRAG
│── requirements.txt            # Dependências do projeto
│── README.md                   # Documentação
```
🔎 Como Funciona?

1️⃣ Envie arquivos PDF, DOCX ou TXT
2️⃣ O GraphRAG processa os textos e cria embeddings (FAISS)
3️⃣ Extrai relações semânticas e constrói um grafo (NetworkX)
4️⃣ Você pode perguntar sobre os documentos
5️⃣ O sistema retorna uma resposta baseada em contexto e conhecimento estruturado

📜 Licença

Este projeto é distribuído sob a licença MIT.
