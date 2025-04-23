import streamlit as st
import asyncio
import fitz  # PyMuPDF
from app.agents.contract_agent import analyze_contract_text

st.set_page_config(page_title="Análise Jurídica de Contratos", layout="wide")

st.title("⚖️ Análise Automática de Contratos Jurídicos")
st.markdown("""
Este sistema utiliza inteligência artificial para **analisar automaticamente contratos**,
identificando riscos e sugerindo correções com base nas **normas internas da empresa**.

Funcionalidades:
- 📎 Comparação cláusula a cláusula com normas internas
- ⚠️ Avaliação de risco (baixo, médio, alto)
- 💡 Sugestões de correção
- 📊 Grau de risco geral do contrato
""")

def extrair_texto_pdf(uploaded_file) -> str:
    """Extrai texto de um arquivo PDF usando PyMuPDF."""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto.strip()

# Entrada de dados
with st.expander("📤 Enviar Contrato para Análise"):
    input_mode = st.radio("Modo de entrada", ["Colar texto manualmente", "Fazer upload de arquivo (.txt ou .pdf)"])

    contrato_texto = ""
    if input_mode == "Colar texto manualmente":
        contrato_texto = st.text_area("Cole abaixo o conteúdo do contrato", height=300)
    else:
        uploaded_file = st.file_uploader("Selecione o arquivo", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.name.endswith(".txt"):
                contrato_texto = uploaded_file.read().decode("utf-8")
            elif uploaded_file.name.endswith(".pdf"):
                contrato_texto = extrair_texto_pdf(uploaded_file)

# Execução da análise
if contrato_texto:
    if st.button("🔍 Executar Análise"):
        with st.spinner("Executando análise com modelo de linguagem..."):
            resultado = asyncio.run(analyze_contract_text(contrato_texto))

        st.success("✅ Análise concluída!")

        st.subheader("📊 Resultado da Análise")
        st.markdown(f"**🧠 Grau de Risco Geral:** `{resultado.overall_risk.upper()}`")

        for idx, clausula in enumerate(resultado.evaluated_clauses):
            with st.expander(f"📄 Cláusula {idx+1}"):
                st.markdown(f"**Texto da Cláusula:**\n```\n{clausula.clause}\n```")
                st.markdown(f"**Risco Avaliado:** `{clausula.risk_level}`")
                st.markdown(f"**Sugestão de Correção:** {clausula.suggestion or 'Nenhuma sugestão disponível.'}")
else:
    st.info("Insira o contrato para iniciar a análise.")
