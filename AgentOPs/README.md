# 🌍 Agente de Planejamento de Viagens com LangChain e Tavily

Este projeto implementa um agente inteligente para ajudar no planejamento de viagens. Ele coleta informações do usuário, busca dados relevantes sobre o destino utilizando **Tavily**, resume os resultados e gera um itinerário detalhado com base nas preferências do viajante.

## 🛠️ Tecnologias Utilizadas
- **Python**: Linguagem de programação principal.
- **LangChain**: Framework para construção de agentes baseados em modelos de linguagem.
- **LangGraph**: Gerenciamento de fluxos de trabalho em grafos.
- **Tavily Search**: Ferramenta para buscas na web.
- **AgentOps**: Rastreamento de ações e eventos.
- **ChatOpenAI**: Modelo de linguagem (GPT-4).
- **dotenv**: Gerenciamento de variáveis de ambiente.

## 📦 Estrutura do Projeto
```
.
├── main.py            # Código principal do agente
├── .env               # Arquivo de variáveis de ambiente (exemplo abaixo)
├── requirements.txt   # Dependências do projeto
└── README.md          # Documentação do projeto
```

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
- Python 3.9 ou superior.
- Uma conta configurada com as chaves de API do Tavily e AgentOps.

### 2. Instalação
Clone este repositório:
```bash
git clone https://github.com/FelipeAmaral13/planejador-viagens.git
cd planejador-viagens
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Configuração
Crie um arquivo `.env` com as seguintes variáveis de ambiente:
```
AGENTOPS_API_KEY=your_agentops_api_key
```

### 4. Execução
Execute o programa principal:
```bash
python main.py
```

O agente solicitará os seguintes dados:
1. **Destino**: Local para onde você quer viajar.
2. **Datas**: Período da viagem.
3. **Interesses**: Preferências, como "cultura", "gastronomia", etc.

### 5. Exemplo de Saída
```plaintext
=== Planejamento de Viagem ===
Digite o destino da viagem: Roma
Quais são as datas da viagem? 20 a 25 de abril
Quais são seus interesses? história, arte, gastronomia

=== Itinerário Final ===
Dia 1:
- Chegada em Roma e check-in no hotel.
- Jantar em um restaurante típico italiano.

Dia 2:
- Visita ao Coliseu e Fórum Romano.
- Almoço no Trastevere.
- Passeio noturno pela Piazza Navona.
```

## ⚙️ Como Funciona
### Etapas do Fluxo:
1. **Coleta de Preferências**:
   - O agente solicita informações básicas do usuário.
2. **Busca no Tavily**:
   - Realiza uma busca detalhada sobre o destino.
3. **Resumo das Informações**:
   - Utiliza o LangChain para criar um resumo relevante com base nos interesses.
4. **Geração do Itinerário**:
   - Monta um plano de viagem detalhado, categorizado por dias.

### Fluxo do Grafo:
```plaintext
START → collect_preferences → search_destination → summarize_destination → generate_itinerary → END
```

## 🔧 Personalização
- **Modelo de Linguagem**:
  - O modelo atual é o `gpt-4o-mini`. Pode ser ajustado no arquivo `main.py`.
- **Resultados do Tavily**:
  - Configure o número máximo de resultados com `TavilySearchResults(max_results=N)`.

## 📘 To-Do
- [ ] Adicionar suporte para reservas automáticas (voos, hotéis).
- [ ] Melhorar validação de entradas do usuário.
- [ ] Criar uma interface gráfica ou chatbot para facilitar a interação.

## 🧡 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir um [issue](https://github.com/seu-usuario/planejador-viagens/issues) ou enviar um pull request.


## 📜 Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
