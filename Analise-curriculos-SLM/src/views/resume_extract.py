import os
import docx2txt
import streamlit as st
from typing import List

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

def show():
    st.title("Resume Extractor")
    st.subheader("App de IA Generativa com SLM, RAG e Engenharia de Prompt Para Assistente de RH")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Digite sua pergunta"}]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    llm = ChatOpenAI(
        model_name="google/gemma-3-12b",
        openai_api_base="http://172.30.64.1:1234/v1",
        openai_api_key="lm-studio",
        temperature=0.0,
        max_tokens=None,
    )

    custom_prompt = PromptTemplate.from_template("""
        Você é um assistente de RH especializado em análise de currículos.
        
        Regras obrigatórias:

        - Escreva os textos em português formal e objetivo.
        - Evite repetições, adjetivos vagos ou termos genéricos.
        - Se não encontrar a informação solicitada, responda com: "Não possíel encontrar a informação. Reformule a pergunta, por favor"

        Contexto:
        {context}

        Histórico de conversa:
        {chat_history}

        Pergunta:
        {question}
        """)

    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def load_documents_from_directory(directory: str, recursive: bool = True) -> List[Document]:
        documents = []
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                ext = file.lower().split(".")[-1]
                text = ""
                try:
                    if ext == "docx":
                        text = docx2txt.process(filepath)
                    elif ext == "txt":
                        with open(filepath, encoding="utf-8") as f:
                            text = f.read()
                except Exception as e:
                    st.warning(f"Erro ao ler {filepath}: {str(e)}")
                    continue

                if text and text.strip():
                    documents.append(Document(page_content=text, metadata={"source": filepath}))
            if not recursive:
                break
        return documents

    def construir_index(docs: List[Document]):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, embed_model)
        return vectorstore

    @st.cache_resource(show_spinner=False)
    def carregar_index():
        with st.spinner("Carregando e indexando os documentos... Isso pode levar alguns instantes."):
            docs = load_documents_from_directory("./documentos", recursive=True)
            if not docs:
                st.error("Nenhum documento encontrado no diretório './documentos'. Verifique o conteúdo.")
                st.stop()
            return construir_index(docs)

    index = carregar_index()

    if "chat_engine" not in st.session_state:
        retriever = index.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        st.session_state.chat_engine = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            combine_docs_chain_kwargs={"prompt": custom_prompt},
            return_source_documents=False,
        )

    if prompt := st.chat_input("Sua pergunta"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                user_message = st.session_state.messages[-1]["content"]
                response = st.session_state.chat_engine.invoke({
                    "question": user_message,
                    "chat_history": st.session_state.chat_history
                })
                st.write(response["answer"])
                st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
                st.session_state.chat_history.append((user_message, response["answer"]))
