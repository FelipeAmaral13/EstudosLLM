# RAG Agentico

Este projeto utiliza a abordagem Retrieval-Augmented Generation (RAG) para análise e recuperação de informações específicas de contratos. Ele carrega documentos PDF, segmenta o texto em partes menores, armazena essas partes em um banco de vetores e usa um modelo de linguagem para responder a consultas baseadas nesses documentos.

## 📌 Funcionalidades
- **Carregamento de documentos PDF** de um diretório.
- **Segmentação de texto** para otimizar a busca e recuperação.
- **Armazenamento e busca vetorial** utilizando ChromaDB.
- **Uso do modelo GPT-4o-mini** para geração de respostas baseadas no contexto extraído dos documentos.
- **Construção de um fluxo de interação com LangGraph**, permitindo análise automática de contratos.

## 📂 Estrutura do Código

### 🔹 Carregamento e Processamento de Documentos
- Os PDFs são carregados utilizando `PyPDFDirectoryLoader`.
- O texto é dividido em fragmentos usando `RecursiveCharacterTextSplitter`.
- Os fragmentos são armazenados no banco de vetores `Chroma`.

### 🔹 Recuperação de Informações
- Um retriever é criado para buscar trechos relevantes nos documentos.
- A ferramenta `retrieve` busca informações relevantes com base em similaridade vetorial.

### 🔹 Fluxo de Decisão e Resposta
- O grafo de decisão usa `LangGraph` para definir a sequência de interações.
- As consultas do usuário são processadas e encaminhadas para recuperação ou resposta.

## 📦 Requisitos
Certifique-se de ter os seguintes pacotes instalados antes de rodar o código:

```bash
pip install langchain langchain_openai langchain_community langgraph chromadb pypdf dotenv
```

## 🚀 Como Executar
1. Coloque seus arquivos PDF no diretório `RAG_Agentico/documents`.
2. Certifique-se de definir suas chaves de API no arquivo `.env`.
3. Execute o script principal para carregar os documentos, criar o banco de vetores e iniciar as consultas:

```bash
python main.py
```

4. Teste uma consulta como:
```python
input_message = "Existem cláusulas de confidencialidade em algum contrato? Se sim, me informe o arquivo."
```

## 📜 Fluxo do Grafo
O código gera um grafo representando o fluxo de decisão e o salva como `graph_RAG_Agentic_2.png`.

## 🛠 Melhorias Futuras
- Integração com outras fontes de dados além de PDFs.
- Implementação de uma interface web para consulta interativa.
- Melhoria na precisão da recuperação de informações legais.

---
🔹 **Desenvolvido com LangChain, LangGraph e OpenAI** 🔹

