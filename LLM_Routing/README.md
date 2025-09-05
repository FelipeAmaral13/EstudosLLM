# LLM Routing Workflow

## Visão Geral

Este projeto implementa um fluxo modular para roteamento de perguntas utilizando modelos de linguagem de grande porte (LLMs). O objetivo é classificar automaticamente questões recebidas e direcioná-las para respostas factuais, pesquisas aprofundadas ou interações generalistas. A arquitetura está centrada na utilização de componentes **LangChain**, com orquestração via **LangGraph** e armazenamento de histórico em memória.

A abordagem privilegia separação de responsabilidades, flexibilidade para troca de modelos, e padronização de prompts, minimizando riscos de acoplamento excessivo e facilitando a manutenção. O pipeline é ideal para ambientes de P&D, squads de IA corporativa, e validação de fluxos conversacionais com múltiplas estratégias de resposta.

---

## Estrutura do Projeto

- **Roteamento Inteligente:** Perguntas são classificadas em três categorias: factual, pesquisa e geral. O roteador utiliza um LLM dedicado apenas à classificação, mitigando viés de decisão do modelo de resposta.
- **Orquestração:** Cada rota aciona um handler independente, que instancia um LLM e prompt adequados ao tipo de questão, permitindo A/B testing e substituição modular de modelos (OpenAI, Llama, Qwen, Gemma etc).
- **Persistência de Memória:** Todo o histórico da conversa é salvo para contexto incremental, abrindo espaço para implementações futuras de recuperação baseada em memória.
- **Componentização e Reusabilidade:** O código segue boas práticas de segregação de funções, com definição clara dos estados, handlers e prompts.

---

## Principais Tecnologias

- **LangChain**: Framework para integração de LLMs e construção de cadeias conversacionais.
- **LangChain OpenAI**: Wrapper para consumo de LLMs (OpenAI e modelos self-hosted).
- **LangGraph**: Definição de grafos de execução, facilitando condicionalidade e fluxos complexos.
- **dotenv**: Gerenciamento de variáveis sensíveis de ambiente.
- **Pydantic**: Validação tipada dos estados e dados de entrada/saída.

---

## Pré-requisitos

- Python >= 3.10
- Modelos LLM disponíveis em endpoint compatível (OpenAI ou servidor LM Studio)
- Dependências conforme especificadas no `pyproject.toml`

---

## Instalação

```bash
pip install -e .
```

---

## Utilização

O arquivo principal `main.py` executa três cenários de teste, ilustrando o roteamento entre handlers de perguntas factuais, pesquisa e geral. O workflow pode ser integrado em APIs, microserviços, pipelines de RAG ou bots corporativos.

---

## Pontos de Atenção

- Acoplamento com Endpoints Proprietários: A configuração dos modelos pressupõe endpoints customizados. O projeto não abstrai totalmente a dependência de servidores LM Studio ou equivalentes.
- Não há Interface Web/REST: A execução ocorre em linha de comando, não havendo frontend ou API exposta.
- Persistência em Memória Volátil: O histórico de conversas é perdido a cada execução; recomenda-se integrar storage persistente para cenários produtivos.
- Prompt Engineering Básico: Os prompts são exemplificativos e podem demandar customização para contextos de produção real.

---

## Conclusão

Este projeto serve como baseline robusto para squads que buscam acelerar a experimentação de fluxos de decisão baseados em LLMs. A estrutura é suficientemente flexível para rápida adaptação, mas requer integração adicional para deployment corporativo (APIs, persistência, autenticação etc).

Para evoluir, recomenda-se:
- Implementar persistência durável do histórico.
- Modularizar configuração de endpoints de LLMs.
- Incorporar logging estruturado e métricas.
- Adicionar testes unitários e de integração.

---

## Licenciamento

Projeto experimental. Consultar governança corporativa antes de aplicação em produção.
