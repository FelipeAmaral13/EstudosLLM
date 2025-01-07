from core.planner_state import PlannerState
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage
from core.llm_client import llm

itinerary_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        template="Você é um assistente de viagem útil. Crie um itinerário de viagem de um dia para {city} com base nos \
        interesses do usuário: {interests}. Forneça um itinerário breve e com marcadores. Não invente ou crie informações quando você não souber responder"),
    HumanMessage(content="Crie um itinerário para minha viagem de um dia.")]
)

def create_itinerary(state: PlannerState):
    try:
        print(f"Criando um itinerário para {state['city']} com base em interesses: {', '.join(state['interests'])}...")
        response = llm.invoke(itinerary_prompt.format_messages(city=state['city'], interests=", ".join(state['interests'])))
        print("========================================")
        print("\n### Itinerário Final:")
        print("========================================")
        print(response.content)
        print("========================================")
        return {
            "messages": state['messages'] + [("ai", response.content)],
            "itinerary": response.content,
        }
    except Exception as e:
        print(f"Erro ao gerar o itinerário: {e}")
        return {
            "messages": state['messages'],
            "itinerary": "Erro: Não foi possível criar o itinerário.",
        }
