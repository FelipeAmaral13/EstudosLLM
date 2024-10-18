# Resumo de Vídeos do YouTube com IA

Este projeto é uma aplicação web desenvolvida em Python utilizando Streamlit, que permite aos usuários resumir vídeos do YouTube através de modelos de linguagem natural. Ele usa modelos como `openai`, `hf_hub` (Hugging Face) e `ollama` para gerar resumos e responder perguntas específicas baseadas no conteúdo do vídeo.

## Funcionalidades
- Carregar vídeos do YouTube e obter uma transcrição.
- Resumir o conteúdo do vídeo usando modelos de linguagem treinados.
- Responder a perguntas específicas feitas pelo usuário com base na transcrição do vídeo.
- Salvar transcrições em cache para otimizar o processamento de vídeos já vistos.
- Utiliza diferentes modelos de linguagem como `openai`, `hf_hub`, e `ollama`.

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **Streamlit**: Biblioteca para criação da interface web.
- **Langchain**: Ferramentas para processamento e manipulação de modelos de linguagem.
- **Hugging Face Hub**: Para integração com modelos de linguagem da comunidade Hugging Face.
- **OpenAI**: Para utilizar modelos como `gpt-3.5-turbo` para gerar respostas e resumos.
- **dotenv**: Para carregar variáveis de ambiente.
- **logging**: Para registrar o fluxo de execução e possíveis erros.

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Conta no [Hugging Face](https://huggingface.co/) e [OpenAI](https://openai.com/) para acesso aos modelos.
- Pip para instalar as dependências.

### Passos de Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/resumo-videos-youtube.git
   cd resumo-videos-youtube
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

4. Crie um arquivo `.env` para armazenar as chaves de API da Hugging Face e OpenAI:
   ```env
   HUGGINGFACEHUB_API_KEY=seu_token_huggingface
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
- **youtube_video_summarizer.py**: Classe responsável por carregar e resumir os vídeos do YouTube.
- **requirements.txt**: Arquivo contendo as dependências do projeto.
- **log.log**: Arquivo de log que armazena os eventos e erros da aplicação.
- **cache/**: Pasta onde ficam armazenadas as transcrições em cache dos vídeos processados.

## Como Usar
1. Abra a aplicação e insira a URL do vídeo do YouTube que deseja resumir.
2. Escolha o modelo de linguagem (ex.: `openai`, `hf_hub`, `ollama`) e configure a temperatura do modelo (controla a aleatoriedade das respostas).
3. Clique no botão "Gerar Resumo" para visualizar as informações do vídeo, resumo dos temas principais e uma resposta para a consulta específica.

## Melhorias Futuras
- **Autenticação de Usuário**: Adicionar autenticação para permitir o uso personalizado e salvar históricos de consultas.
- **Suporte a mais tipos de vídeo**: Expandir o suporte para outras plataformas de vídeo além do YouTube.
- **Melhorar a Interface**: Tornar a interface mais amigável e interativa com funcionalidades como navegação entre transcrições salvas.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests para melhorias e correções.

## Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
