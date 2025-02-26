import streamlit as st
import os
import tempfile
import fitz  
import docx
from graphrag import GraphRAG

rag = GraphRAG()

st.set_page_config(page_title="GraphRAG com Streamlit", layout="wide")

st.title("📚 GraphRAG: Pergunte sobre múltiplos documentos!")

st.sidebar.header("📂 Upload de Documentos")
uploaded_files = st.sidebar.file_uploader(
    "Envie arquivos .pdf, .docx ou .txt", accept_multiple_files=True, type=["pdf", "docx", "txt"]
)

def extrair_texto_pdf(pdf_file):
    """Extrai texto de um arquivo PDF."""
    texto = ""
    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name

    doc = fitz.open(temp_pdf_path)
    for page in doc:
        texto += page.get_text("text") + "\n"
    doc.close()
    os.remove(temp_pdf_path)  # Remove o arquivo temporário
    return texto

def extrair_texto_docx(docx_file):
    """Extrai texto de um arquivo DOCX."""
    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp_docx:
        temp_docx.write(docx_file.read())
        temp_docx_path = temp_docx.name

    doc = docx.Document(temp_docx_path)
    texto = "\n".join([p.text for p in doc.paragraphs])
    os.remove(temp_docx_path)  # Remove o arquivo temporário
    return texto

def processar_arquivos(uploaded_files):
    """Processa os arquivos carregados e adiciona ao GraphRAG."""
    documentos = []

    for uploaded_file in uploaded_files:
        if uploaded_file.type == "text/plain":  # Arquivo TXT
            content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":  # Arquivo PDF
            content = extrair_texto_pdf(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:  # Arquivo DOCX
            content = extrair_texto_docx(uploaded_file)
        else:
            st.sidebar.warning(f"⚠️ Formato não suportado: {uploaded_file.name}")
            continue

        documentos.append(content)
        st.sidebar.write(f"✅ {uploaded_file.name}")

    # Construção da base de conhecimento
    with st.spinner("🔄 Processando documentos..."):
        for documento in documentos:
            rag.construir_base_conhecimento(documento)
    
    st.sidebar.success("✅ Base de conhecimento criada com sucesso!")

if uploaded_files:
    processar_arquivos(uploaded_files)

# Campo de entrada para perguntas
st.subheader("💡 Faça uma pergunta sobre os documentos")
pergunta = st.text_input("Digite sua pergunta aqui:")

if pergunta:
    # Busca por chunks mais relevantes (RAG clássico)
    chunks = rag.buscar_chunks_similares(pergunta)
    info_vetorial = "\n".join(chunks)

    # Busca por relações no grafo (GraphRAG)
    relacoes = rag.buscar_relacoes_relevantes(pergunta)

    # Exibição das relações encontradas
    if relacoes:
        st.subheader("📌 Relações encontradas no Grafo")
        for r in relacoes:
            if r["tipo"] == "direto":
                st.write(f"🔗 **{r['entidade1']}** --[{r['relacao']}]--> **{r['entidade2']}**")
            else:
                st.write(f"🛤 **Caminho:** {r['caminho']}")

    # Geração de resposta com LLM
    with st.spinner("💡 Gerando resposta..."):
        resposta = rag.gerar_resposta_llm(pergunta, info_vetorial, relacoes)

    # Exibição da resposta
    st.subheader("📝 Resposta")
    st.write(resposta)
