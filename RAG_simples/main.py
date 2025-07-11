import streamlit as st
from src.rag.rag_system import RAGSystem
import tempfile
import os

st.set_page_config(page_title="Assistente RAG", layout="centered")

st.title("📄💬 Assistente RAG com PDF")

# Upload do PDF
uploaded_file = st.file_uploader("Faça upload de um arquivo PDF", type="pdf")

# Inicializa variável de estado
if "rag" not in st.session_state:
    st.session_state.rag = None

if uploaded_file:
    # Cria arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success("📁 PDF carregado com sucesso.")
    
    # Monta o pipeline após o upload
    with st.spinner("🔧 Construindo o pipeline RAG..."):
        rag = RAGSystem(path_file=tmp_path)
        rag.build_pipeline()
        st.session_state.rag = rag

# Caixa de pergunta
question = st.text_input("Digite sua pergunta sobre o conteúdo do PDF")

if st.button("Responder") and question:
    if st.session_state.rag is None:
        st.error("⚠️ Carregue um PDF primeiro.")
    else:
        with st.spinner("💬 Gerando resposta..."):
            response = st.session_state.rag.qa_chain(question)

            st.markdown("### 🧠 Resposta:")
            st.write(response["result"])

            st.markdown("### 📚 Fontes utilizadas:")
            for doc in response["source_documents"]:
                st.markdown(f"- Página: `{doc.metadata.get('page', '?')}`")
                st.markdown(f"> {doc.page_content[:300]}...")

