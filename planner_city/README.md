
# **Planner City**

O **Planner City** é um assistente de viagens interativo que utiliza um grafo de estados e um modelo de linguagem grande (LLM) para criar itinerários personalizados de um dia. O projeto foi desenvolvido para coletar informações de destino e interesses do usuário e, com base nesses dados, gerar um itinerário conciso e informativo.

## **Características**

- **Entrada Interativa:**
  - Solicita informações sobre o destino e interesses diretamente do usuário.
- **Geração de Itinerário:**
  - Cria um itinerário de viagem personalizado com base nas preferências informadas.
- **Arquitetura Modular:**
  - Código bem organizado com separação de responsabilidades para facilitar a manutenção e escalabilidade.
- **Mensagens Centralizadas:**
  - Textos reutilizáveis para fácil customização e internacionalização.
- **Persistência de Dados:**
  - Salva o itinerário gerado em um arquivo local para referência futura.

---

## **Requisitos**

- Python 3.8 ou superior
- Bibliotecas:
  - `langchain_openai`
  - `dotenv`
  - `langgraph`
  - `langchain_core`

### **Instalação de Dependências**

Use o `pip` para instalar as dependências:

```bash
pip install -r requirements.txt
```

---

## **Estrutura do Projeto**

```
planner_city/
│
├── main.py                # Ponto de entrada do programa
├── core/
│   ├── llm_client.py      # Cliente LLM para interagir com o modelo de linguagem
│   ├── messages.py        # Mensagens centralizadas para interação com o usuário
│   ├── planner_state.py   # Definição do estado do planejador
│   └── state_graph.py     # Configuração do grafo de estados
│
├── modules/
│   ├── create_itinerary.py # Função para gerar itinerário com base nas entradas
│   ├── input_city.py       # Função para coletar o destino do usuário
│   └── input_interests.py  # Função para coletar os interesses do usuário
│
├── utils/
│   └── file_utils.py      # Utilitário para salvar itinerários
│
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto
```

---

## **Como Executar**

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd planner_city
   ```

2. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto.
   - Adicione a variável de API da OpenAI:
     ```
     OPENAI_API_KEY=<sua-chave-da-openai>
     ```

3. Execute o programa:

   ```bash
   python main.py
   ```

---

## **Fluxo de Funcionamento**

1. **Coleta de Dados:**
   - Solicita ao usuário o nome da cidade e seus interesses.
2. **Criação do Itinerário:**
   - O grafo de estados organiza as interações e invoca o modelo LLM para gerar o itinerário.
3. **Apresentação e Persistência:**
   - Exibe o itinerário no console e salva o resultado em um arquivo local.

---

## **Contribuição**

Contribuições são bem-vindas! Siga estas etapas para contribuir:

1. Faça um fork do repositório.
2. Crie um branch com sua funcionalidade:
   ```bash
   git checkout -b minha-nova-funcionalidade
   ```
3. Faça um pull request para análise.

---

## **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## **Autores**

- **Nome:** Felipe
- **Especialidade:** Inteligência Artificial, LLMs e Desenvolvimento Modular

---

Se precisar de suporte ou quiser sugerir melhorias, entre em contato!
