# RAG Simples 3

Um sistema simples de Retrieval-Augmented Generation (RAG) para auditoria inteligente, utilizando LangChain, FAISS e a API Groq para análise de conformidade baseada em documentos.

## Descrição

Este projeto implementa um agente de auditoria que carrega documentos de texto de uma pasta `dados/`, os processa em chunks, cria um banco de dados vetorial com embeddings, e responde perguntas sobre conformidade usando um modelo de linguagem da Groq.

## Funcionalidades

- Carregamento de documentos de texto (.txt) de uma pasta específica
- Divisão de texto em chunks com sobreposição
- Geração de embeddings usando HuggingFace BGE
- Armazenamento vetorial com FAISS
- Consulta inteligente com recuperação de contexto relevante
- Respostas em português focadas em conformidade

## Pré-requisitos

- Python 3.12 ou superior
- Chave da API Groq (GROQ_API_KEY)

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd rag-simples-3
   ```

2. Instale as dependências:
   ```bash
   pip install -e .
   ```

3. Configure a variável de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da API Groq:
     ```
     GROQ_API_KEY=sua-chave-aqui
     ```

4. Prepare os dados:
   - Crie uma pasta `dados/` no diretório raiz
   - Adicione arquivos de texto (.txt) contendo os documentos para análise

## Uso

### Execução Básica

Execute o script principal:

```bash
python main.py
```

Isso executará uma análise de exemplo sobre reembolso de transporte.

### Uso Programático

```python
from main import AuditAgent

agent = AuditAgent()
resposta = agent.ask("Sua pergunta sobre conformidade aqui")
print(resposta)
```

## Estrutura do Projeto

```
rag-simples-3/
├── main.py              # Script principal com o agente de auditoria
├── pyproject.toml       # Configuração do projeto e dependências
├── README.md            # Este arquivo
├── .gitignore           # Arquivos ignorados pelo Git
└── dados/               # Pasta para documentos de texto (não incluída no repositório)
```

## Dependências

- faiss-cpu: Para armazenamento vetorial
- groq: Cliente da API Groq
- langchain: Framework para aplicações LLM
- langchain-community: Componentes comunitários do LangChain
- langchain-huggingface: Integração com HuggingFace
- langchain-text-splitters: Divisão de texto
- python-dotenv: Carregamento de variáveis de ambiente
- sentence-transformers: Para embeddings
- streamlit: (Incluído, possivelmente para interface futura)
- unstructured: Processamento de documentos não estruturados

## Configuração

O sistema usa os seguintes parâmetros padrão:

- Modelo de embeddings: BAAI/bge-base-en-v1.5
- Tamanho do chunk: 1000 caracteres
- Sobreposição: 150 caracteres
- Número de documentos recuperados: 4
- Modelo LLM: llama-3.3-70b-versatile
- Temperatura: 0 (determinístico)

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.