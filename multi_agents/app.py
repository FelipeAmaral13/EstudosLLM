import os
import operator
import sqlite3
from typing import TypedDict, Annotated
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Imports dos seus módulos customizados
from guardrails import Guardrail
from ferramentas import buscar_dados_evento, buscar_historico_usuario, buscar_reputacao_ip

# Carregamento de configurações
load_dotenv()

# Configuração do LLM (Local via LM Studio ou API)
model_name = "meta-llama-3.1-8b-instruct@Q4_k_M"
llm = ChatOpenAI(
    model_name=model_name,
    openai_api_base="http://192.168.0.6:1234/v1",
    openai_api_key="lm-studio",
    temperature=0.0,
    max_tokens=512,
)

# Definição das ferramentas
tools = [
    buscar_dados_evento,
    buscar_historico_usuario,
    buscar_reputacao_ip,
]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

# Inicialização do Guardrail
guardrail = Guardrail()

# --- Definição do Estado do Grafo ---
class GraphState(TypedDict):
    messages: Annotated[list, operator.add]
    sender: str

# --- Funções de Nós (Agentes) ---

def agent_node(state: GraphState, agent, name):
    print(f"--- EXECUTANDO NÓ DO AGENTE: {name} ---")
    result = agent.invoke(state["messages"])
    return {"messages": [result], "sender": name}

def node_analista_triagem(state: GraphState):
    """Nível 1: Coleta de logs brutos."""
    prompt = (
        f"Investigue o evento: '{state['messages'][0].content}'. "
        "Use 'buscar_dados_evento' para obter os detalhes técnicos. "
        "Apenas colete os dados e passe para o próximo nível."
    )
    inputs = {"messages": [HumanMessage(content=prompt)]}
    return agent_node(inputs, llm_with_tools, "analista_triagem")

def node_investigador_forense(state: GraphState):
    """Nível 2: Enriquecimento de contexto (Usuário e IP)."""
    prompt = (
        "Com base nos logs, extraia o 'user_id' e o 'source_ip'. "
        "Use 'buscar_historico_usuario' e 'buscar_reputacao_ip' para contextualizar o incidente."
    )
    state['messages'].append(HumanMessage(content=prompt))
    return agent_node(state, llm_with_tools, "investigador_forense")

def node_coordenador_incidencias(state: GraphState):
    """Nível 3: Tomada de decisão final e relatório."""
    prompt = """Você é o CISO. Analise os logs, o perfil do usuário e a reputação do IP.
    Gere um relatório em Markdown com as seções: 1. Resumo, 2. Análise de Risco, 3. Veredito.
    Recomendação Final: BLOQUEAR ACESSO, ISOLAR MAQUINA ou FALSO POSITIVO."""
    
    state['messages'].append(HumanMessage(content=prompt))
    return agent_node(state, llm, "coordenador_incidencias")

# --- Lógica de Roteamento ---

def should_call_tool(state: GraphState):
    """Verifica se o agente solicitou o uso de uma ferramenta."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "call_tool"
    return "continue"

def router(state: GraphState):
    """Direciona o fluxo após a execução de uma ferramenta."""
    last_sender = state["sender"]
    if last_sender == "analista_triagem":
        return "investigador_forense"
    elif last_sender == "investigador_forense":
        return "coordenador_incidencias"

# --- Construção do Grafo ---

workflow = StateGraph(GraphState)

# Adicionando os nós
workflow.add_node("analista_triagem", node_analista_triagem)
workflow.add_node("investigador_forense", node_investigador_forense)
workflow.add_node("coordenador_incidencias", node_coordenador_incidencias)
workflow.add_node("tool_node", tool_node)

# Fluxo de entrada
workflow.set_entry_point("analista_triagem")

# Arestas condicionais
workflow.add_conditional_edges(
    "analista_triagem",
    should_call_tool,
    {"continue": "investigador_forense", "call_tool": "tool_node"}
)

workflow.add_conditional_edges(
    "investigador_forense",
    should_call_tool,
    {"continue": "coordenador_incidencias", "call_tool": "tool_node"}
)

workflow.add_conditional_edges(
    "tool_node",
    router,
    {
        "investigador_forense": "investigador_forense", 
        "coordenador_incidencias": "coordenador_incidencias"
    }
)

workflow.add_edge("coordenador_incidencias", END)
app_soc = workflow.compile()

png_graph = app_soc.get_graph().draw_mermaid_png()
with open("my_graph_agent_simple.png", "wb") as f:                                                                                                                                                                                                                                                                                                                  
    f.write(png_graph)


if __name__ == "__main__":
    # Exemplo de investigação de um incidente suspeito no banco SQL
    # EVT103 = Brute Force vindo da Rússia para Beatriz Silva
    input_evento = "EVT108" 
    
    print(f"\n[SOC-IA] Iniciando investigação do evento: {input_evento}")
    inputs = {"messages": [HumanMessage(content=f"ID do Evento: {input_evento}")]}
    
    relatorio_final = ""
    for output in app_soc.stream(inputs, {"recursion_limit": 20}):
        for key, value in output.items():
            if key == "coordenador_incidencias":
                relatorio_final = value["messages"][-1].content

    if relatorio_final:
        # Beatriz Silva é a usuária associada ao EVT103 (Beatriz Silva)
        # O Guardrail irá mascarar o nome dela e IPs internos
        resultado_seguro = guardrail.validate_output(relatorio_final, "Beatriz Silva")
        
        print("\n" + "="*50)
        print("RELATÓRIO DE INCIDENTE PROTEGIDO")
        print("="*50)
        print(resultado_seguro)