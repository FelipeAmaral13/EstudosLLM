import streamlit as st
from youtube_video_summarizer import YouTubeVideoSummarizer
from langchain_core.output_parsers import StrOutputParser

# Configuração do Streamlit
st.set_page_config(page_title="Resumo de Vídeos do YouTube", layout="wide")
st.title("Resumo de Vídeos do YouTube com IA")

# Inputs do usuário
url_video = st.text_input("Insira a URL do vídeo do YouTube:")
query_user = st.text_input("Insira sua consulta para o resumo:")
model_class = st.selectbox("Escolha o modelo de linguagem:", ["openai", "hf_hub", "ollama"])

# Configurações adicionais do modelo
temperature = st.slider("Temperatura do modelo:", 0.0, 1.0, 0.1)
model_params = {"temperature": temperature}

# Botão para processar o vídeo
if st.button("Gerar Resumo"):
    if url_video and query_user and model_class:
        with st.spinner("Processando o vídeo, isso pode levar alguns minutos..."):
            try:
                # Inicializa o processador de vídeo
                video_processor = YouTubeVideoSummarizer(url_video, query_user, model_class, model_params)
                transcript, metadata = video_processor.get_video_info()

                # Exibe informações do vídeo
                st.subheader("Informações do Vídeo")
                st.write(f"**Título**: {metadata['title']}")
                st.write(f"**Autor**: {metadata['author']}")
                st.write(f"**Data de Publicação**: {metadata['publish_date'][:10]}")
                st.write(f"**URL**: [Link para o vídeo](https://www.youtube.com/watch?v={metadata['source']})")

                # Cria o prompt chain
                chain = video_processor.create_prompt_template() | video_processor.create_model(model_class) | StrOutputParser()

                # Sobre o que fala o vídeo
                st.subheader("Sobre o que fala o vídeo")
                res = chain.invoke({"transcricao": transcript, "consulta": "Explique em uma frase sobre o que fala esse vídeo. Responda direto com a frase."})
                st.write(res)

                # Temas principais do vídeo
                st.subheader("Temas Principais")
                res = chain.invoke({"transcricao": transcript, "consulta": "Liste os principais temas desse vídeo."})
                st.write(res)

                # Resposta para a consulta do usuário
                st.subheader("Resposta para a Consulta do Usuário")
                res = chain.invoke({"transcricao": transcript, "consulta": query_user})
                st.write(res)

                st.success("Resumo gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao processar o vídeo: {e}")
    else:
        st.warning("Por favor, preencha todos os campos antes de continuar.")
