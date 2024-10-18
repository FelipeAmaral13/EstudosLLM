import streamlit as st
import faiss
import tempfile
import os
import time
import sqlite3
import uuid

from langchain_community.llms import HuggingFaceHub
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Converse com documentos 📚", page_icon="📚")
st.title("Converse com documentos 📚")

# Configuração do banco de dados
DB_FILE = 'chat_history.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            session_id TEXT,
            message_type TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para carregar histórico salvo
def load_chat_history(session_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT message_type, content FROM chat_history WHERE session_id = ?', (session_id,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        return [AIMessage(content=row[1]) if row[0] == 'AIMessage' else HumanMessage(content=row[1]) for row in rows]
    return [AIMessage(content="Olá, sou o seu assistente virtual! Como posso ajudar você?")]

# Função para salvar o histórico da conversa
def save_chat_history(session_id, history):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_history WHERE session_id = ?', (session_id,))
    for msg in history:
        message_type = 'AIMessage' if isinstance(msg, AIMessage) else 'HumanMessage'
        cursor.execute('INSERT INTO chat_history (session_id, message_type, content) VALUES (?, ?, ?)',
                       (session_id, message_type, msg.content))
    conn.commit()
    conn.close()

def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
    llm = HuggingFaceHub(
        repo_id=model,
        model_kwargs={
            "temperature": temperature,
            "return_full_text": False,
            "max_new_tokens": 512,
        }
    )
    return llm

# Indexação e recuperação
def config_retriever(uploads):
   docs = []
   temp_dir = tempfile.TemporaryDirectory()
   for file in uploads:
      temp_filepath = os.path.join(temp_dir.name, file.name)
      with open(temp_filepath, "wb") as f:
         f.write(file.getvalue())
      loader = PyPDFLoader(temp_filepath)
      docs.extend(loader.load())
    
   text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
   splits = text_splitter.split_documents(docs)

   embeddings = HuggingFaceEmbeddings(model_name = "BAAI/bge-m3")

   vectorstore = FAISS.from_documents(splits, embeddings)
   vectorstore.save_local('vectorstore/db_faiss')

   retriever = vectorstore.as_retriever(search_type = "mmr", search_kwargs={'k': 3, 'fetch_k': 4})
   return retriever

def config_rag_chain(retriever):
    llm = model_hf_hub()

    token_s, token_e = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>", "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

    context_q_system_prompt = "Given the following chat history and the follow-up question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    context_q_system_prompt = token_s + context_q_system_prompt
    context_q_user_prompt = "Question: {input}" + token_e
    context_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", context_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", context_q_user_prompt),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(llm=llm, retriever=retriever, prompt=context_q_prompt)
    
    qa_prompt_template = """Você é um assistente virtual prestativo e está respondendo perguntas gerais. 
    Use os seguintes pedaços de contexto recuperado para responder à pergunta. 
    Se você não sabe a resposta, apenas diga que não sabe. Mantenha a resposta concisa. 
    Responda em português. \n\n
    Pergunta: {input} \n
    Contexto: {context}"""

    qa_prompt = PromptTemplate.from_template(token_s + qa_prompt_template + token_e)

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return rag_chain

# Inicializar o banco de dados
init_db()

# Gerar ou carregar um ID de sessão único para cada sessão
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id

# Carregar histórico salvo
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history(session_id)

if "docs_list" not in st.session_state:
    st.session_state.docs_list = None

uploads = st.sidebar.file_uploader(
    label="Enviar arquivos",
    type=["pdf"],
    accept_multiple_files=True
)

# Se novos arquivos forem enviados, criar um novo session_id e resetar o histórico
if uploads and (st.session_state.docs_list is None or st.session_state.docs_list != uploads):
    st.session_state.session_id = str(uuid.uuid4())
    session_id = st.session_state.session_id
    st.session_state.chat_history = [AIMessage(content="Olá, você enviou novos arquivos. Como posso ajudar com eles?")]
    st.session_state.docs_list = uploads
    st.session_state.retriever = config_retriever(uploads)
    save_chat_history(session_id, st.session_state.chat_history)  # Salvar o novo estado de histórico

if not uploads:
    st.info("Por favor, envie algum arquivo para continuar")
    st.stop()

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Exibir mensagens anteriores
total_messages = len(st.session_state.chat_history)
for idx, message in enumerate(st.session_state.chat_history):
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            if idx == total_messages - 1 and uploads:
                st.info("Novo contexto carregado. Agora estou pronto para responder suas perguntas sobre os documentos enviados.")
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

start = time.time()
user_query = st.chat_input("Digite sua mensagem aqui...")

if user_query is not None and user_query != "" and uploads is not None:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        st.info("Estou processando sua consulta. Por favor, aguarde...")
        rag_chain = config_rag_chain(st.session_state.retriever)
        result = rag_chain.invoke({"input": user_query, "chat_history": st.session_state.chat_history})

        resp = result['answer']
        st.write(resp)

    st.session_state.chat_history.append(AIMessage(content=resp))

    # Salvar histórico da conversa
    save_chat_history(session_id, st.session_state.chat_history)

end = time.time()
print("Tempo: ", end - start)
