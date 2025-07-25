# 📄 RAG Multimodal para Análise de Notas Fiscais (Imagem + Contexto Contábil)

> Pipeline completo de IA Generativa com **LangGraph**, **FAISS**, **LLM Vision** e **Flask**, que interpreta **notas fiscais em imagem** com base em **regras contábeis vetorizadas**.

---

## 🚀 Visão Geral

Este projeto demonstra como aplicar **RAG (Retrieval-Augmented Generation) Multimodal** para analisar notas fiscais em formato de imagem (JPG, PNG, WEBP), interpretando tanto o conteúdo visual quanto o contexto semântico contábil — utilizando uma **LLM Vision local** e um vetor de conhecimento embasado em **PDFs contábeis**.

✔️ Upload de nota fiscal (imagem)  
✔️ Pergunta livre sobre a nota (ex: “qual o valor total?”)  
✔️ Análise contextual com base em documentos PDF indexados  
✔️ Resposta final gerada por LLM com suporte a imagem e texto

---

## 🧠 Arquitetura

```text
Usuário ⇨ Flask Web ⇨ LangGraph ⇨
├── retrieve_rag_node  ➜ FAISS (PDFs contábeis)
└── analyze_invoice_node ➜ LLM Vision (imagem + contexto)
                           ⇨ Resposta contábil contextualizada
```

---

## 📦 Tecnologias Utilizadas

| Camada        | Tecnologia                          |
|---------------|--------------------------------------|
| Orquestração  | [LangGraph](https://python.langgraph.dev) |
| Vetorização   | [FAISS + FastEmbed (BAAI)](https://github.com/facebookresearch/faiss) |
| LLM Multimodal| [LM Studio](https://lmstudio.ai) (compatível com OpenAI API) |
| UI            | [Flask](https://flask.palletsprojects.com/) + Bootstrap 5 |
| Embeddings    | `BAAI/bge-small-en-v1.5` via [FastEmbed](https://github.com/ai-forever/fastembed) |

---

## 📁 Estrutura do Projeto

```bash
.
├── analyzer.py           # Núcleo IA: LangGraph + análise multimodal
├── app.py                # Aplicação Flask (upload, roteamento, integração)
├── templates/
│   └── index.html        # Interface HTML com Bootstrap
├── static/
│   └── styles.css        # Estilo visual
├── uploads/              # Armazena imagens temporariamente
├── faiss_index_contabilidade/  # Base vetorial com PDFs
├── documentos_pdfs/      # PDF contábeis para indexação
└── README.md             # Este documento
```

---

## 🛠️ Como Rodar Localmente

### 1. Clone o projeto

```bash
git clone https://github.com/FelipeAmaral13/EstudosLLM.git
cd rag-multimodal-nota-fiscal
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

> Inclui: `langgraph`, `langchain`, `faiss-cpu`, `fastembed`, `flask`, `openai`

### 3. Indexe os PDFs contábeis

Coloque seus PDFs contábeis em `documentos_pdfs/` e execute:

```python
from analyzer import MultimodalRAGAnalyzer

analyzer = MultimodalRAGAnalyzer()
analyzer.cria_vectordb("documentos_pdfs")
```

### 4. Inicie o LM Studio

- Baixe e abra o [LM Studio](https://lmstudio.ai/)
- Carregue um modelo multimodal (ex: `gemma-3-12b`, `llava`, etc)
- Habilite a API local (porta `1234` por padrão)

### 5. Rode o app Flask

```bash
python app.py
```

Acesse via navegador em: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Exemplos de Perguntas

- "Qual é o valor líquido da nota?"
- "Existe retenção de ISS?"
- "A data de emissão está correta?"
- "A nota está em conformidade com a legislação vigente?"

> As respostas combinam a leitura da **imagem da nota** com **documentos contábeis vetorizados**.

---

## 🔐 Privacidade e Segurança

- Nenhuma imagem ou dado é enviado para a nuvem
- Toda análise é feita **localmente**
- Ideal para setores com alto rigor regulatório (saúde, financeiro, jurídico)

---

## 📌 Contribuindo

Pull requests são bem-vindos. Para contribuições maiores, abra uma issue primeiro para discutirmos a abordagem.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

---

## 🤝 Contato

Desenvolvido por **Felipe Meganha**  
