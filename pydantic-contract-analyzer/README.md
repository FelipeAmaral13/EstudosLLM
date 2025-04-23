
# ⚖️ Contract Analyzer - Análise Jurídica com IA (Pydantic-AI + RAG)

Este projeto tem como objetivo **automatizar a análise de contratos jurídicos**, utilizando modelos de linguagem (LLMs) integrados via [Pydantic-AI](https://github.com/pydantic/pydantic-ai). A solução compara cláusulas contratuais com **normas internas da empresa**, classifica riscos, sugere correções e atribui um **grau de risco global** ao contrato.

## 💡 Funcionalidades

- 📎 Comparação cláusula a cláusula com normas internas
- ⚠️ Avaliação de risco: `baixo`, `médio` ou `alto`
- 💡 Sugestão de correções para cláusulas problemáticas
- 🧠 Cálculo de grau de risco geral para o contrato
- 🖥️ Interface interativa via [Streamlit](https://streamlit.io/)
- 📄 Suporte a upload de contratos em `.txt` ou `.pdf`

## 🗂️ Estrutura de Diretórios

```text
projeto_pydanticai/
├── app/
│   ├── agents/          # Agente com modelo de linguagem (LLM)
│   ├── models/          # Modelos Pydantic de entrada/saída
│   ├── prompts/         # Prompts de sistema (template)
│   ├── tools/           # Ferramentas auxiliares (ex: busca vetorial)
│   └── utils/           # Funções de apoio
├──streamlit_app.py      # Interface Web
├── config/              # Configuração de ambiente (ex: .env)
└── README.md
```

## 🚀 Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/contract-analyzer.git
cd contract-analyzer
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> **Obs.**: Certifique-se de que o arquivo `.env` contenha sua chave da OpenAI:
> ```env
> OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
> ```

### 4. Execute o app Streamlit

```bash
streamlit run web/streamlit_app.py
```

## 🧠 Tecnologias Utilizadas

- **[Pydantic-AI](https://github.com/pydantic/pydantic-ai)**: Framework para agentes com validação estruturada
- **LLM via Groq (LLaMA 3)** ou OpenAI (pluggable)
- **[ChromaDB](https://www.trychroma.com/)**: Motor de busca vetorial para normas internas
- **[Streamlit](https://streamlit.io/)**: Interface web interativa
- **[PyMuPDF](https://github.com/pymupdf/PyMuPDF)**: Leitura de contratos em PDF

## 📌 Exemplo de Uso

1. Faça upload de um contrato no formato `.txt` ou `.pdf`
2. Clique em **“Executar Análise”**
3. Visualize:
   - Grau de risco geral
   - Cláusulas com seus respectivos riscos
   - Sugestões de correção

## 🛠️ Expansões Futuras

- Exportação de análise em `.pdf` ou `.docx`
- Histórico e rastreabilidade de contratos analisados
- API REST para integração com sistemas jurídicos internos
- Suporte a múltiplos idiomas

## 📄 Licença

Este projeto é distribuído sob a licença MIT
## 🤝 Contribuição

Contribuições são bem-vindas! Para isso:

1. Faça um fork
2. Crie sua branch: `git checkout -b feature/nome`
3. Commit suas alterações: `git commit -m 'feat: minha feature'`
4. Push para sua branch: `git push origin feature/nome`
5. Crie um Pull Request

---

Desenvolvido com 💼 por Felipe Meganha
