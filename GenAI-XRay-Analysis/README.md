# AI-Powered X-Ray Analysis

## Descrição

O projeto **AI-Powered X-Ray Analysis** utiliza inteligência artificial para análise de imagens de raio-X, fornecendo diagnósticos e recomendações de tratamento. A solução é desenvolvida usando Streamlit para a interface do usuário, PIL para manipulação de imagens, e o modelo Gemini da Google GenAI para a análise de imagens.

## Funcionalidades

- **Upload de Imagens:** Interface amigável para o upload de imagens de raio-X.
- **Análise Automática:** Análise detalhada das imagens pelo modelo de IA Gemini.
- **Diagnóstico e Recomendações:** Fornecimento de diagnósticos e sugestões de tratamento com base na interpretação das imagens.

## Tecnologias Utilizadas

- **Streamlit:** Para criação da interface web interativa.
- **PIL (Pillow):** Para manipulação e validação das imagens.
- **Google GenAI (Gemini):** Para análise e geração de diagnósticos.
- **dotenv:** Para gerenciamento de variáveis de ambiente.

## Instalação

1. Clone o repositório:
   git clone

2. Navegue até o diretório do projeto:
   cd AI-Powered-X-Ray-Analysis

3. Crie e ative um ambiente virtual (opcional, mas recomendado):
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate

4. Instale as dependências:
   pip install -r requirements.txt

5. Configure sua chave de API do Google GenAI. Crie um arquivo `.env` no diretório raiz do projeto e adicione a seguinte linha:
   API_KEY=your_google_genai_api_key

## Uso

1. Inicie a aplicação Streamlit:
   streamlit run app.py

2. Acesse a interface no seu navegador através do link fornecido no terminal.

3. Carregue uma imagem de raio-X e aguarde a análise automática.

## Código

O código-fonte do projeto está localizado no arquivo `app.py`. Aqui está uma visão geral das principais funções:

- **`criar_modelo()`:** Cria e configura uma instância do modelo Gemini com as configurações fornecidas.
- **`validar_imagem(image)`:** Verifica se a imagem carregada está em um formato suportado (JPEG, JPG ou PNG).
- **`main()`:** Configura a interface Streamlit, faz o upload da imagem, valida e processa a imagem, e exibe o diagnóstico gerado pelo modelo.

## Contribuição

Se você deseja contribuir com melhorias para o projeto, siga estes passos:

1. Faça um fork do repositório.
2. Crie uma nova branch para suas alterações:
   git checkout -b minha-nova-branch
3. Faça suas alterações e commit:
   git commit -am 'Adiciona nova funcionalidade'
4. Envie suas alterações para o repositório remoto:
   git push origin minha-nova-branch
5. Abra um pull request no GitHub.

## Licença

Este projeto é licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se você tiver dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou entrar em contato diretamente.
