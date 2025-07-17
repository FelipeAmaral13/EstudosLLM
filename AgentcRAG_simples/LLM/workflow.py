from langgraph.graph import StateGraph, END
from agent.agent_state import AgentState
from LLM.formata_contexto import formata_contexto
from LLM.gera_resposta import gera_resposta
from LLM.recupera_documentos import recupera_documentos

print("\nConstruindo o grafo de agente...")
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", recupera_documentos)
workflow.add_node("format_context", formata_contexto)
workflow.add_node("generate", gera_resposta)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "format_context")
workflow.add_edge("format_context", "generate")
workflow.add_edge("generate", END)
agent_app = workflow.compile()
print("Grafo de agente compilado.")