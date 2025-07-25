import streamlit as st

def show():

    st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 2.5em;">👋 Bem-vindo ao <span style="color:#3B82F6">Sistema de Automação de Currículos</span></h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    
        Este sistema <strong>automatiza a análise de currículos</strong>, além de gerar automaticamente uma análise estratégica com apenas um clique.<br><br>
        Digite <strong>perguntas específicas</strong> sobre os candidatos para obter <strong>respostas detalhadas com base no conteúdo dos currículos</strong>.<br><br>
        O assistente utiliza <strong>técnicas avançadas de Engenharia de Prompt</strong> e <strong>RAG (Retrieval-Augmented Generation)</strong> para garantir a precisão das respostas.<br><br>
        <span style="color: #EF4444;"><strong>Atenção:</strong></span> o processamento inicial dos documentos pode levar entre <strong>1 e 2 minutos</strong>. Seja paciente e aguarde a análise.
    """, unsafe_allow_html=True)
