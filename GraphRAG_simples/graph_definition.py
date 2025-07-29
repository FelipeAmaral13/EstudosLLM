from langgraph.graph import StateGraph, START, END
from graph_nodes import *
from state_agent import AgentState

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("load_vectorstore", load_vectorstore)
    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("format_documents", format_documents)
    graph.add_node("generate_answer", generate_answer)

    graph.set_entry_point("load_vectorstore")

    graph.add_edge("load_vectorstore", "retrieve_documents")
    graph.add_edge("retrieve_documents", "format_documents")
    graph.add_edge("format_documents", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()
