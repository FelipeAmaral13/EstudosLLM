# LangGraph Router

Um sistema inteligente de roteamento e processamento de documentos baseado em LangGraph e LangChain.

## Descrição

O LangGraph Router é um sistema que permite classificar e processar automaticamente diferentes tipos de documentos (contratos, faturas e relatórios) utilizando modelos de linguagem natural. O sistema utiliza uma arquitetura de grafo para rotear as solicitações e processá-las de acordo com seu tipo.

## Funcionalidades

- Classificação automática de documentos em três categorias:
  - Contratos
  - Faturas
  - Relatórios
- Processamento específico para cada tipo de documento
- Sistema de logging detalhado para monitoramento
- Seleção automática do modelo mais adequado (rápido ou poderoso) baseado na complexidade da tarefa
- Extração estruturada de informações em formato JSON

## Tecnologias Utilizadas

- Python
- LangChain
- LangGraph
- OpenAI GPT (3.5-turbo e GPT-4)
- Logging
- Python-dotenv

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install langchain langchain-openai langgraph python-dotenv
```
3. Configure as variáveis de ambiente em um arquivo `.env`:
```bash
OPENAI_API_KEY=sua_chave_api
```

## Uso

```python
from langgraph_router import LangGraphRouter

# Inicializa o router
router = LangGraphRouter()

# Processa um documento
resposta = router.process_question(seu_documento)
print(resposta)
```

## Estrutura do Sistema

### Classificador
- Analisa o input inicial
- Determina o tipo de documento
- Escolhe o modelo mais apropriado (rápido ou poderoso)

### Processadores Específicos
- **Contratos**: Extrai partes envolvidas, datas de vigência, cláusulas importantes e riscos
- **Faturas**: Identifica número, data, valor total, itens cobrados e inconsistências
- **Relatórios**: Extrai objetivo, conclusões, recomendações e dados relevantes

### Sistema de Logging
- Logs detalhados de todas as operações
- Diferentes níveis de log (INFO, DEBUG, ERROR)
- Formato timestamp para rastreabilidade

## Exemplos de Uso

### Processando um Contrato
```python
contrato_exemplo = """
Este contrato é celebrado entre a Empresa XYZ Ltda. e o Cliente ABC S.A.
Data de vigência: 01/01/2025 a 31/12/2025.
...
"""
resposta = router.process_question(contrato_exemplo)
```

### Processando uma Fatura
```python
fatura_exemplo = """
Número da Fatura: 12345
Data de Emissão: 15/01/2025
...
"""
resposta = router.process_question(fatura_exemplo)
```

## Configuração de Logging

O sistema utiliza logging configurado para fornecer informações detalhadas sobre o processamento:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

## Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
