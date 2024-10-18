# Extrator de Informações de Certificados PDF

Este projeto é uma aplicação web desenvolvida em Python usando Streamlit, que permite extrair informações específicas de certificados em formato PDF, como a instituição de ensino, nome do aluno, curso realizado e carga horária. A aplicação utiliza um modelo de linguagem da OpenAI para realizar a extração e formatação dos dados.

## Funcionalidades
- Carregar um ou mais arquivos PDF de certificados.
- Extrair informações do certificado como instituição, nome do aluno, curso e carga horária.
- Formatar as informações extraídas em formato JSON para facilitar o uso dos dados.

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **Streamlit**: Biblioteca para criação da interface web.
- **Langchain**: Framework para trabalhar com modelos de linguagem e encadear prompts.
- **OpenAI GPT-3.5**: Modelo de linguagem utilizado para interpretar e extrair informações dos certificados.
- **dotenv**: Para carregar variáveis de ambiente, como chaves de API.

## Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior.
- Conta na [OpenAI](https://openai.com/) para acesso ao modelo GPT-3.5.
- Pip para instalar as dependências.

### Passos de Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/extrator-certificados-pdf.git
   cd extrator-certificados-pdf
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` para armazenar as chaves de API da OpenAI:
   ```env
   OPENAI_API_KEY=seu_token_openai
   ```

### Execução
1. Execute a aplicação com o Streamlit:
   ```bash
   streamlit run app.py
   ```
2. Acesse a aplicação no navegador através do endereço exibido, geralmente `http://localhost:8501`.

## Estrutura do Projeto
- **app.py**: Arquivo principal contendo a lógica da aplicação web.
- **requirements.txt**: Arquivo contendo as dependências do projeto.
- **.env**: Arquivo que contém as chaves de API para autenticação.

## Como Usar
1. Abra a aplicação e faça o upload do(s) certificado(s) em PDF.
2. O modelo processará o conteúdo e extrairá informações como instituição, nome do aluno, curso realizado e carga horária.
3. As informações extraídas serão exibidas no formato JSON, facilitando o uso e a análise dos dados.

## Melhorias Futuras
- **Suporte a outros idiomas**: Expandir o suporte para certificados em diferentes idiomas.
- **Melhoria no processamento de PDFs**: Adicionar suporte para arquivos PDF digitalizados (OCR) usando bibliotecas como Tesseract.
- **Autenticação de Usuários**: Implementar autenticação para restringir o uso da aplicação e possibilitar o armazenamento do histórico de certificados processados.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests para melhorias e correções.

## Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
