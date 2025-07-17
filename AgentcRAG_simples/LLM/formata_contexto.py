from agent.agent_state import AgentState
from agentic_RAG import AgenticRAG

def formata_contexto(state: AgentState) -> AgentState:
    
    print("--- Nó: Formatando Contexto ---")

    documents = state["documents"]
    rag = AgenticRAG()
    context = rag.formata_docs_metadados(documents)


    return {"context": context}