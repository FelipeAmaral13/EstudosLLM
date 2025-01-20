import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agentops import record_action, track_agent, init, end_session, record, ActionEvent, ToolEvent, ErrorEvent
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)


init(api_key=os.environ['AGENTOPS_API_KEY'], default_tags=["langgraph-agent"])
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
tavily_search = TavilySearchResults(max_results=3)

class TravelState(TypedDict):
    destination: str
    dates: str
    interests: str
    destination_info: str
    itinerary: str

@record_action("collect_preferences")
def collect_preferences(state: TravelState) -> TravelState:
    # Simular coleta de preferências
    state["destination"] = input("Qual é o destino da viagem? ")
    state["dates"] = input("Quais são as datas da viagem? ")
    state["interests"] = input("Quais são seus interesses (ex.: cultura, aventura, gastronomia)? ")
    return state

@record_action("search_destination")
def search_destination(state: TravelState) -> TravelState:
    try:
        # Busca informações sobre o destino usando Tavily
        search_results = tavily_search.invoke(state["destination"])
        # Formatar os resultados
        if isinstance(search_results, list) and all(isinstance(r, str) for r in search_results):
            formatted_results = "\n".join(search_results)
        elif isinstance(search_results, list) and all(isinstance(r, dict) for r in search_results):
            formatted_results = "\n".join([f"{r.get('title', '')}: {r.get('snippet', r.get('content', ''))}" for r in search_results])
        else:
            formatted_results = str(search_results)
        state["destination_info"] = formatted_results
    except Exception as e:
        # Registrar erro no AgentOps
        record(ErrorEvent(exception=e))
        state["destination_info"] = f"Erro ao realizar a busca: {str(e)}"
    return state

@record_action("summarize_destination")
def summarize_destination(state: TravelState) -> TravelState:
    prompt = ChatPromptTemplate.from_template(
        "Resuma as informações sobre {destination} com foco nos interesses: {interests}."
    )
    chain = prompt | model
    summary = chain.invoke({
        "destination": state["destination"],
        "interests": state["interests"],
        "destination_info": state["destination_info"]
    }).content
    state["destination_info"] = summary
    return state

@record_action("generate_itinerary")
def generate_itinerary(state: TravelState) -> TravelState:
    prompt = ChatPromptTemplate.from_template(
        "Crie um itinerário detalhado para {destination} com base nos interesses: {interests}, "
        "nas seguintes datas: {dates}.\n\nInformações disponíveis:\n{destination_info}"
    )
    chain = prompt | model
    itinerary = chain.invoke({
        "destination": state["destination"],
        "interests": state["interests"],
        "dates": state["dates"],
        "destination_info": state["destination_info"]
    }).content
    state["itinerary"] = itinerary
    return state

# Construção do grafo
builder = StateGraph(TravelState)

builder.add_node("collect_preferences", collect_preferences)
builder.add_node("search_destination", search_destination)
builder.add_node("summarize_destination", summarize_destination)
builder.add_node("generate_itinerary", generate_itinerary)

builder.add_edge(START, "collect_preferences")
builder.add_edge("collect_preferences", "search_destination")
builder.add_edge("search_destination", "summarize_destination")
builder.add_edge("summarize_destination", "generate_itinerary")
builder.add_edge("generate_itinerary", END)

graph = builder.compile()


png_graph = graph.get_graph().draw_mermaid_png()
with open("graph_agentOPs.png", "wb") as f:
    f.write(png_graph)

def execute_travel_plan():
    initial_state = {
        "destination": "",
        "dates": "",
        "interests": "",
        "destination_info": "",
        "itinerary": ""
    }

    final_state = graph.invoke(initial_state)
    end_session("Success", "Plano de viagem gerado com sucesso!")
    return final_state["itinerary"]

# Executar o fluxo
print("=== Planejamento de Viagem ===")
final_plan = execute_travel_plan()
print("\n=== Itinerário Final ===")
print(final_plan)