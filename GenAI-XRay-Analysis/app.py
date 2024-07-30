# Imports
from PIL import Image
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('GOOGLE_GENAI_API_KEY')

MODEL_NAME = 'gemini-1.5-pro-latest'
GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

SYSTEM_PROMPT = """
    Você é um radiologista altamente qualificado, especializado na análise de imagens de raios-X. 
    Objetivo: Fornecer uma análise detalhada e recomendação de tratamento baseada na interpretação das imagens de raio-X.

    Responsabilidades:

        Análise detalhada: Analise minuciosamente cada imagem radiográfica, concentrando-se na identificação de fraturas ou quaisquer achados anormais.
        Relatar as descobertas: Documente todas as suas descobertas. Articule claramente essas descobertas em um formato estruturado.
        Recomendar tratamento: Com base na sua análise, sugira os próximos passos a seguir. Se houver fraturas ou quaisquer achados anormais, recomende o tratamento mais conhecido.

    Escopo de Resposta:

        Responda apenas se a imagem for uma imagem de raio-X.
        Se a qualidade da imagem estiver impedindo a análise, mencione isso ao usuário.
        Se a imagem não for uma imagem de raio-X ou se estiver fora do escopo das fraturas ósseas, informe que a análise não é possível.
"""

SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

def criar_modelo():
    """Cria uma instância do modelo com as configurações fornecidas."""
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
        system_instruction=SYSTEM_PROMPT
    )

def validar_imagem(image):
    """Valida se a imagem carregada é uma imagem de raio-X."""
    if image.format in ["JPEG", "JPG", "PNG"]:
        return True
    return False

def main():
    genai.configure(api_key=API_KEY)
    modelo = criar_modelo()
    
    st.title('GenAI para Diagnóstico de Imagens de Raio-X')
    st.write("Carregue uma imagem de raio-X para análise. O sistema fornecerá uma análise detalhada e recomendações de tratamento.")

    uploaded_file = st.file_uploader('Carregue uma imagem de raio-X:', type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        try:
            image_data = Image.open(uploaded_file)
            if not validar_imagem(image_data):
                st.error("O arquivo carregado não parece ser uma imagem de raio-X válida.")
                return

            col1, col2 = st.columns(2)
            with col1:
                st.image(image_data, caption='Imagem Carregada', use_column_width=True)
            with col2:
                with st.spinner('Analisando imagem...'):
                    content = ["Analise esta imagem.", image_data]
                    resposta_modelo = modelo.start_chat().send_message(content)
                    st.success('Análise Concluída!')
                    st.write('Resultado da Análise:')
                    st.write(resposta_modelo.text)
        except Exception as e:
            st.error(f'Ocorreu um erro ao processar a imagem: {e}')
    else:
        st.info('Por favor, carregue uma imagem para análise.')

if __name__ == '__main__':
    main()
