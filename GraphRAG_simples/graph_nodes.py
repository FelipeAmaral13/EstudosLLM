from state_agent import AgentState
from langchain_core.documents import Document
from llm_model import llm

def load_vectorstore(state: AgentState):
    retriever = state["rag_instance"].criar_vectordb().as_retriever()
    
    return {"retriever": retriever}

def retrieve_documents(state: AgentState):
    query = state["query"]
    retriever = state["retriever"]
    docs = retriever.invoke(query)

    return {"docs": docs}

def format_documents(state: AgentState):
    rag = state["rag_instance"]
    docs = state["docs"]
    formatted = rag.formata_docs_metadados(docs)
    
    return {"context": formatted}

def generate_answer(state: AgentState):
    prompt = f"""Use o contexto abaixo para responder a pergunta:

{state['context']}

Pergunta: {state['query']}
"""
    resposta = llm.invoke(prompt)
    return {"resposta": resposta.content}