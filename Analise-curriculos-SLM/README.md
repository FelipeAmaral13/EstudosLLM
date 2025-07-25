# Sistema de Automação de Currículos com IA Generativa

Este projeto implementa um sistema baseado em **Streamlit** para análise automatizada de currículos utilizando **SLMs (Small Language Models)**, **RAG (Retrieval-Augmented Generation)** e **engenharia de prompt**. Ideal para automação de triagem de candidatos e apoio à área de Recursos Humanos.

---

## Funcionalidades

- Interface web com navegação via menu lateral
- Leitura e indexação de currículos em `.docx` ou `.txt`
- Extração de conteúdo relevante via embeddings e FAISS
- Chat com assistente de RH especializado em análise de currículos
- Capacidade de responder perguntas baseadas nos dados indexados
- Geração de respostas formais e contextuais em português

---

## Estrutura do Projeto

```
├── main.py                # Inicialização da aplicação Streamlit
├── home.py                # Página inicial com explicação
├── resume_extract.py      # Página de análise e RAG
├── documentos/            # Currículos para análise
└── pyproject.toml         # Dependências do projeto
```

---

## Tecnologias Utilizadas

- `Streamlit` para a interface
- `LangChain` para orquestração de LLM + RAG
- `FAISS` para busca vetorial
- `HuggingFace Embeddings` para geração de vetores
- `ChatOpenAI` com LLM local via LM Studio (modelo: `google/gemma-3-12b`)
- `docx2txt` e `PyPDF2` para leitura de documentos

---

## Execução Local

1. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
```

2. Instale as dependências:
```bash
pip install -e .
```

3. Inicie o app:
```bash
streamlit run main.py
```

4. Coloque os currículos dentro do diretório `./documentos`.

---

## Observações

- O tempo de indexação depende da quantidade de documentos.
- A aplicação utiliza modelo local via LM Studio, com URL definida como `http://172.30.64.1:1234/v1`.

---

## Autor

Desenvolvido por Felipe Meganha – Cientista de Dados, Professor e Especialista em IA Generativa aplicada à Saúde.

