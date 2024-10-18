# Converse com Documentos 📚

Este é um projeto desenvolvido em Python utilizando Streamlit para criar um chatbot interativo que permite ao usuário carregar documentos (PDFs) e conversar com o conteúdo desses documentos. O projeto usa técnicas de Processamento de Linguagem Natural (NLP) para responder a perguntas dos usuários baseadas nos documentos fornecidos.

## Funcionalidades
- Carregue um ou mais arquivos PDF e converse com o conteúdo deles.
- Histórico de chat persistente por meio de um banco de dados SQLite, onde cada conversa é identificada por um `session_id` único.
- Novo `session_id` é gerado sempre que novos documentos são enviados, possibilitando que o histórico de sessões anteriores seja mantido no banco de dados.
- O chatbot responde a perguntas específicas com base nos conteúdos dos PDFs, utilizando modelos de linguagem da Hugging Face.

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal.
- **Streamlit**: Interface de usuário web simples e interativa.
- **SQLite**: Banco de dados relacional para armazenamento do histórico de conversas.
- **FAISS**: Biblioteca para armazenamento vetorial e recuperação de documentos.
- **Hugging Face Hub**: Utilizado para obter modelos de linguagem que alimentam o chatbot.

## Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior
- Pip para gerenciar as dependências
- Conta na [Hugging Face](https://huggingface.co/) para acessar os modelos de linguagem

### Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/converse-com-documentos.git
    cd converse-com-documentos
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

4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave de acesso à API da Hugging Face:
    ```env
    HUGGINGFACEHUB_API_KEY=seu_token_aqui
    ```

### Execução
1. Inicialize o banco de dados:
    ```bash
    python init_db.py
    ```
2. Execute a aplicação Streamlit:
    ```bash
    streamlit run app.py
    ```

3. Abra o navegador no endereço exibido no terminal, geralmente `http://localhost:8501`.

## Estrutura do Projeto
- **app.py**: Arquivo principal que contém o código do chatbot e a interface Streamlit.
- **init_db.py**: Script para inicializar o banco de dados SQLite.
- **chat_history.db**: Banco de dados que armazena o histórico de conversas.
- **requirements.txt**: Lista de dependências do projeto.

## Como Usar
1. Faça o upload dos arquivos PDF na barra lateral.
2. Comece a conversar! Faça perguntas sobre o conteúdo dos documentos carregados.
3. Quando novos PDFs forem carregados, uma nova conversa é iniciada, preservando as conversas anteriores.

## Melhorias Implementadas
- **Experiência do Usuário**: Mensagens informativas foram adicionadas para melhorar o fluxo, como mensagens ao iniciar uma nova conversa ou quando o chatbot está processando uma consulta.
- **Sessão Persistente**: Cada conversa possui um `session_id` exclusivo que é salvo no banco de dados. Um novo `session_id` é gerado ao iniciar uma nova conversa.

## Possíveis Melhorias Futuras
- **Suporte a diferentes tipos de arquivos**: Atualmente, o projeto suporta apenas arquivos PDF. Futuramente, poderia incluir outros formatos como DOCX ou TXT.
- **Autenticação de Usuários**: Implementar um sistema de autenticação para permitir que diferentes usuários acessem seus históricos de conversa.
- **Escalabilidade**: Migrar o armazenamento dos documentos e do histórico de chat para uma solução em nuvem, permitindo melhor escalabilidade e acesso seguro aos dados.

## Contribuições
Sinta-se à vontade para contribuir com o projeto, seja enviando um pull request ou relatando problemas na seção de issues.

## Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
