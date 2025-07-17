from agent.agent_state import AgentState
from agentic_RAG import AgenticRAG

def recupera_documentos(state: AgentState) -> AgentState:


    print("--- Nó: Recuperando Documentos ---")
    question = state["question"]
    rag = AgenticRAG()
    retriever = rag.criar_vectordb().as_retriever(search_kwargs={'k': 5})

    print(f"Recuperando para a pergunta: {question}")
    documents = retriever.invoke(question)
    print(f"{len(documents)} documentos recuperados.")

    return {"documents": documents, "question": question}