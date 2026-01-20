# Multi-Agents SOC IA

Um sistema de Security Operations Center (SOC) inteligente baseado em agentes múltiplos utilizando LangGraph e LangChain para investigação automatizada de incidentes de cibersegurança.

## Descrição

Este projeto implementa um SOC (Centro de Operações de Segurança) virtual usando inteligência artificial com múltiplos agentes especializados. O sistema orquestra três níveis de análise:

1. **Analista de Triagem**: Coleta dados técnicos brutos do incidente
2. **Investigador Forense**: Enriquece o contexto com perfil do usuário e reputação de IP
3. **Coordenador de Incidentes**: Toma decisões finais e gera relatórios executivos

O sistema inclui guardrails de segurança para proteger dados sensíveis e garantir conformidade.

## Funcionalidades

- **Análise Multi-Nível**: Investigação em camadas com especialização por agente
- **Integração com Banco de Dados**: Consulta automática de logs, usuários e reputação de IPs
- **Guardrails de Segurança**: Mascaramento automático de PII e dados sensíveis
- **Relatórios Estruturados**: Geração de relatórios em Markdown com recomendações claras
- **Orquestração com LangGraph**: Fluxo controlado de agentes com roteamento condicional
- **Integração com LLMs**: Suporte a modelos locais via LM Studio ou APIs externas

## Arquitetura

### Agentes
- **Analista de Triagem**: Coleta logs técnicos usando `buscar_dados_evento`
- **Investigador Forense**: Contextualiza com `buscar_historico_usuario` e `buscar_reputacao_ip`
- **Coordenador de Incidentes**: Análise final e geração de relatório

### Ferramentas
- `buscar_dados_evento`: Consulta detalhes de eventos de segurança
- `buscar_historico_usuario`: Obtém perfil e nível de acesso do usuário
- `buscar_reputacao_ip`: Verifica score de reputação e ameaças do IP

### Guardrails
- Mascaramento de nomes de usuários
- Proteção de IPs internos
- Remoção de hashes e tokens de autenticação
- Validação de recomendações de mitigação

## Pré-requisitos

- Python 3.12+
- SQLite3
- LM Studio (para execução local de LLMs) ou chave da API OpenAI

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd multi-agents
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente no arquivo `.env`:
```env
OPENAI_API_BASE=http://192.168.0.6:1234/v1
OPENAI_API_KEY=lm-studio
MODEL_NAME=meta-llama-3.1-8b-instruct@Q4_k_M
```

5. Execute o script de inicialização do banco:
```bash
python banco_db.py
```

## Uso

Execute o sistema principal:
```bash
python app.py
```

O sistema irá investigar um evento de exemplo (EVT108) e gerar um relatório protegido.

### Personalização

Para investigar um evento específico, modifique a variável `input_evento` em `app.py`:

```python
input_evento = "SEU_EVENT_ID"
```

## Estrutura do Projeto

```
multi-agents/
├── app.py                 # Arquivo principal com definição dos agentes e grafo
├── banco_db.py           # Inicialização e população do banco de dados SQLite
├── ferramentas.py        # Definição das ferramentas de consulta
├── guardrails.py         # Implementação dos guardrails de segurança
├── pyproject.toml        # Configuração do projeto e dependências
├── soc_ia.db            # Banco de dados SQLite (gerado automaticamente)
├── my_graph_agent_simple.png  # Diagrama visual do grafo de agentes
└── README.md            # Este arquivo
```

## Dependências

- `langchain>=1.2.6`: Framework para aplicações LLM
- `langchain-openai>=1.1.7`: Integração com OpenAI
- `langgraph>=1.0.6`: Orquestração de agentes
- `python-dotenv>=1.2.1`: Gerenciamento de variáveis de ambiente

## Banco de Dados

O sistema utiliza SQLite com três tabelas principais:

- **usuarios**: Perfis dos colaboradores
- **reputacao_ip**: Scores de reputação de endereços IP
- **eventos**: Logs de incidentes de segurança

## Configuração do LLM

### Opção 1: LM Studio (Local)
1. Instale o LM Studio
2. Baixe um modelo compatível (ex: Llama 3.1)
3. Inicie o servidor local na porta 1234
4. Configure as variáveis no `.env`

### Opção 2: API OpenAI
1. Obtenha uma chave da API OpenAI
2. Configure `OPENAI_API_BASE=https://api.openai.com/v1`
3. Defina `OPENAI_API_KEY=sua-chave-aqui`

## Exemplo de Saída

```
==================================================
RELATÓRIO DE INCIDENTE PROTEGIDO
==================================================
# Relatório de Incidente

## 1. Resumo
Incidente de tentativa de acesso não autorizado detectado...

## 2. Análise de Risco
- Usuário: [USUARIO_CONFIDENCIAL]
- IP: [IP_REDE_INTERNA]
- Score de reputação: Alto risco

## 3. Veredicto
Recomendação Final: BLOQUEAR ACESSO
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.