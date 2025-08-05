# 📦 Projeto Chatbot de Perguntas Frequentes

## 📋 Visão Geral

Este projeto tem como objetivo **construir um sistema de perguntas e respostas (FAQ)** utilizando **Python**, **Jupyter Notebook** e um **dataset JSON** com perguntas e respostas predefinidas.  
Ele pode ser utilizado como base para:

- **Treinar chatbots**
- **Gerar FAQs interativas**
- **Servir de backend para sistemas de suporte automatizado**

O projeto demonstra **boas práticas em ciência de dados** e **pré-processamento de dados textuais**, podendo ser expandido para uso com **modelos de NLP e SLMs** para respostas inteligentes.

---

## 📂 Estrutura do Projeto

```
├── finetunning_SLM.ipynb          # Notebook principal com processamento e testes do chatbot
├── dataset.json            # Dataset com perguntas e respostas
└── README.md               # Documentação do projeto
```

- **`finetunning_SLM.ipynb`**: Contém o passo a passo do desenvolvimento, leitura do dataset, pré-processamento e testes.  
- **`dataset.json`**: Base de conhecimento do chatbot com 26 perguntas e respostas de um e-commerce fictício.  

---

## 🗃️ Dataset

O dataset é um arquivo JSON estruturado no seguinte formato:

```json
{
  "perguntas": [
    {
      "pergunta": "Como posso criar uma conta?",
      "resposta": "Para criar uma conta, clique no botão ‘Cadastre-se’..."
    },
    {
      "pergunta": "Que tipos de pagamentos você aceita?",
      "resposta": "Aceitamos os principais cartões de crédito..."
    }
  ]
}
```

- Contém **26 pares de pergunta/resposta**.
- Focado em **atendimento ao cliente para e-commerce**.
- Pode ser facilmente expandido para novos tópicos.

---

## ⚙️ Pré-requisitos

- **Python 3.9+**  
- **Jupyter Notebook ou JupyterLab**  
- Bibliotecas recomendadas:
  ```bash
  pip install pandas numpy scikit-learn nltk
  ```

Para compatibilidade futura com NLP avançado:
```bash
pip install sentence-transformers transformers
```

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório ou copie os arquivos para sua máquina**
   ```bash
   git clone https://github.com/seuusuario/finetunning_SLM-chatbot.git
   cd finetunning_SLM-chatbot
   ```

2. **Crie um ambiente virtual e instale dependências**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Abra o Jupyter Notebook**
   ```bash
   jupyter notebook finetunning_SLM.ipynb
   ```

4. **Execute todas as células** para carregar o dataset, processar dados e rodar os exemplos de perguntas.

---

## 🧪 Exemplo de Uso

### 1️⃣ Consulta Simples no Notebook
```python
import json

with open('dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

pergunta = "Como posso criar uma conta?"
resposta = next((p["resposta"] for p in dataset["perguntas"] if p["pergunta"] == pergunta), "Pergunta não encontrada.")
print(resposta)
```

**Saída esperada:**
```
Para criar uma conta, clique no botão ‘Cadastre-se’ no canto superior direito do nosso site e siga as instruções para concluir o processo de registro.
```

---

## 📈 Próximos Passos e Melhorias

- Implementar **busca semântica** para identificar respostas semelhantes usando embeddings.
- Criar **API Flask/FastAPI** para consumo externo do chatbot.
- Desenvolver **frontend interativo** para FAQ online.
- Integrar com **LLMs** para respostas dinâmicas e contextualizadas.

---

## 👨‍💻 Autor

**Felipe Meganha**  
Cientista de Dados, Especialista em IA e Visão Computacional  
LinkedIn: [linkedin.com/in/felipemeganha](https://linkedin.com/in/felipemeganha)
