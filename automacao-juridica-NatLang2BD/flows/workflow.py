from models.agent_state import AgentState
from langgraph.graph import StateGraph, END
from service.llm_services import initialize_database_state, generate_sql_query, validate_sql_query, provide_sql_feedback
from langgraph.checkpoint.memory import MemorySaver

builder = StateGraph(AgentState)

# Adicionar nós
builder.add_node("initialize_database", initialize_database_state)
builder.add_node("sql_writer", generate_sql_query)
builder.add_node("qa_engineer", validate_sql_query)
builder.add_node("chief_dba", provide_sql_feedback)

# Adicionar arestas
builder.add_edge("initialize_database", "sql_writer")
builder.add_edge("sql_writer", "qa_engineer")
builder.add_edge("chief_dba", "sql_writer")

# Adicionar arestas condicionais
builder.add_conditional_edges(
    "qa_engineer", 
    lambda state: END if state['accepted'] or state['revision'] >= state['max_revision'] else "reflect", 
    {END: END, "reflect": "chief_dba"}
)

# Definir ponto de entrada
builder.set_entry_point("initialize_database")

# Configurar o checkpointer usando MemorySaver
memory = MemorySaver()

# Compilar o grafo
graph = builder.compile(checkpointer=memory)
