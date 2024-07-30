# Sistema de Gerenciamento de Pacientes

## Descrição

O **Sistema de Gerenciamento de Pacientes** é uma aplicação desenvolvida para ajudar na gestão de informações de pacientes e na recomendação de tratamentos personalizados. Através desta plataforma, os usuários podem cadastrar, buscar, atualizar e deletar informações sobre pacientes, além de obter recomendações de tratamento baseadas nos sintomas informados.

## Funcionalidades

- **Cadastrar Paciente**: Permite o cadastro de novos pacientes no sistema.
- **Pesquisar Paciente**: Permite a busca por pacientes cadastrados usando o CPF ou o nome.
- **Atualizar Paciente**: Permite a atualização das informações de um paciente existente.
- **Deletar Paciente**: Permite a exclusão de pacientes pelo CPF.
- **Recomendar Tratamento**: Fornece recomendações de tratamento baseadas nos sintomas informados pelo paciente.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação da interface web.
- **SQLite**: Banco de dados relacional leve para armazenamento das informações dos pacientes.
- **LangChain**: Biblioteca para manipulação de linguagem natural.
- **OpenAI GPT-3.5**: Modelo de linguagem para geração de recomendações de tratamento.

## Configuração do Ambiente

1. **Clone o Repositório**

   ```bash
   git clone <URL-DO-REPOSITORIO>
   cd <NOME-DO-REPOSITORIO>
   ```

2. **Instale as Dependências**

   Certifique-se de ter o Python 3.x instalado. Em seguida, crie um ambiente virtual e instale as dependências necessárias.

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure o Arquivo `.env`**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```
   OPENAI_API_KEY=<SUA-CHAVE-API-OPENAI>
   ```

4. **Crie o Banco de Dados**

   Execute o script de criação do banco de dados para configurar as tabelas necessárias:

   ```bash
   python app.py
   ```

## Uso

1. **Inicie a Aplicação**

   ```bash
   streamlit run app.py
   ```

2. **Acesse a Interface Web**

   Abra um navegador e vá para [http://localhost:8501](http://localhost:8501).

## Instruções de Uso

- **Cadastrar Paciente**: Vá até a aba 'Cadastrar Paciente', preencha as informações e clique em 'Cadastrar'.
- **Pesquisar Paciente**: Vá até a aba 'Pesquisar Paciente', insira o CPF ou o nome e clique em 'Pesquisar'.
- **Atualizar Paciente**: Vá até a aba 'Atualizar Paciente', insira o CPF e atualize as informações necessárias.
- **Deletar Paciente**: Vá até a aba 'Deletar Paciente', insira o CPF e clique em 'Deletar'.
- **Recomendar Tratamento**: Vá até a aba 'Recomendar Tratamento', insira o CPF e clique em 'Recomendar Tratamento'.

## Estrutura de Diretórios

- **app.py**: Arquivo principal que executa a aplicação Streamlit.
- **.env**: Arquivo de configuração para variáveis de ambiente.
- **requirements.txt**: Lista de dependências do projeto.
- **bd_llm_analise_sintoma/db**: Diretório que contém o banco de dados SQLite.

## Contribuição

Contribuições são bem-vindas! Se você encontrar um bug ou tiver uma sugestão de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
