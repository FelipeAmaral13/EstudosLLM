# 🤖 Estudos com `pydantic-ai`

Este repositório contém uma série de exemplos práticos e comentados de **agentes de IA estruturados usando a biblioteca [`pydantic-ai`](https://github.com/ted-piotrowski/pydantic-ai)**.  
Cada script explora um domínio diferente e mostra como integrar **modelos de linguagem (LLMs)** com **validação tipada de dados**, ferramentas assíncronas e lógica de negócio.

---

## 🧠 O que é `pydantic-ai`?

É uma biblioteca que conecta **Pydantic + LLMs** com uma abordagem declarativa, segura e extensível para criar **agentes inteligentes com ferramentas controladas**.

> "Agentes com validação, contexto e ações reais — sem hallucination, com tipagem forte."

---

## 📁 Estrutura dos Projetos

Cada arquivo demonstra um cenário diferente com um agente de IA acoplado a ferramentas próprias:

| Arquivo | Descrição |
|--------|-----------|
| [`agente_IA_tickets.py`](./agente_IA_tickets.py) | Agente para abertura e consulta de chamados técnicos. Salva dados no SQLite. |
| [`agente_IA_Receitas.py`](./agente_IA_Receitas.py) | Geração automatizada de receitas culinárias com ingredientes, passos e dicas. |
| [`agente_IA_financeiro.py`](./agente_IA_financeiro.py) | Análise de transações financeiras com geração de alertas e insights estruturados. |
| [`agente_IA_livros.py`](./agente_IA_livros.py) | Recomendador de livros baseado em preferências de leitura. |
| [`agente_IA_Recomendacao_Filmes.py`](./agente_IA_Recomendacao_Filmes.py) | Agente que recomenda filmes e plataformas com base em preferências do usuário. |

---

## ✅ Conceitos Praticados

- Uso de `Agent`, `tool` e `RunContext` da `pydantic-ai`
- Validação robusta com `BaseModel`, `Field` e `Literal`
- Execução assíncrona com `asyncio`
- Persistência com SQLite (em alguns exemplos)
- Boas práticas de logging, modularidade e estruturação de prompts

---

## 💡 Exemplos de Aplicações Reais

- Sistemas de atendimento com geração automática de chamados
- Recomendadores personalizados de conteúdo (livros, filmes, receitas)
- Assistentes financeiros com validação de padrões e alertas

---

## 📌 Requisitos

- Python 3.10+
- `pydantic-ai`
- `python-dotenv`
- (opcional) API Key da Groq

