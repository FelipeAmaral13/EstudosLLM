import os
from dotenv import load_dotenv
from typing import TypedDict, Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


class GraphState(TypedDict):
    question: str
    classification: Literal['factual', 'research', 'general']
    answer: str | None
    history: list[dict] 

def handle_factual(state: GraphState):
    print("---Rota: FACTUAL")
    question = state['question']
    history = state.get('history', [])
    history_text = "\n".join([f"Q: {h['question']} | A: {h['answer']}" for h in history])

    print(f"Recebida pergunta factual: {question}")

    # 1. Configurar o LLM (seu código está perfeito aqui)
    model_name='meta-llama-3.1-8b-instruct'
    llm = ChatOpenAI(model_name=model_name,
                     openai_api_base="http://192.168.0.30:1234/v1",
                     openai_api_key="lm-studio",
                     temperature=0.0)

    # 2. Criar um prompt simples
    prompt = ChatPromptTemplate.from_template(
        "Histórico da conversa:\n{history}\nAgora, responda de forma direta e factual: {question}"
    )
    
    # 3. Criar a cadeia (chain) e invocar
    # O StrOutputParser apenas extrai o texto da resposta do LLM
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"history": history_text, "question": question})
    print(f"Resposta gerada: {answer} - Modelo utilizado: {model_name}")

    return {"answer": answer, "history": history + [{"question": question, "answer": answer}]}

def handle_research(state: GraphState):
    print("---Rota: PESQUISA")
    question = state['question']
    history = state.get('history', [])
    history_text = "\n".join([f"Q: {h['question']} | A: {h['answer']}" for h in history])
    print(f"Recebida pergunta pesquisa: {question}")

    # 1. Configurar o LLM (seu código está perfeito aqui)
    model_name='qwen/qwen3-4b-2507'
    llm = ChatOpenAI(model_name=model_name,
                     openai_api_base="http://192.168.0.30:1234/v1",
                     openai_api_key="lm-studio",
                     temperature=0.0)

    # 2. Criar um prompt simples
    prompt = ChatPromptTemplate.from_template(
        "Histórico da conversa:\n{history}\n.Faça a pesquisa necessaria para responder a seguinte pergunta: {question}")
    
    # 3. Criar a cadeia (chain) e invocar
    # O StrOutputParser apenas extrai o texto da resposta do LLM
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"history": history_text, "question": question})
    print(f"Resposta gerada: {answer} - Modelo utilizado: {model_name}")

    return {"answer": answer, "history": history + [{"question": question, "answer": answer}]}

def handle_general(state: GraphState):
    print("---Rota: GERAL")
    question = state['question']
    history = state.get('history', [])
    history_text = "\n".join([f"Q: {h['question']} | A: {h['answer']}" for h in history])
    print(f"Recebida pergunta geral: {question}")

    # 1. Configurar o LLM (seu código está perfeito aqui)
    model_name='meta-llama-3.1-8b-instruct'
    llm = ChatOpenAI(model_name=model_name,
                     openai_api_base="http://192.168.0.30:1234/v1",
                     openai_api_key="lm-studio",
                     temperature=0.0)

    # 2. Criar um prompt simples
    prompt = ChatPromptTemplate.from_template(
        "Histórico da conversa:\n{history}\n.Resposanda de maneira generalista a seguinte questão: {question}")
    
    # 3. Criar a cadeia (chain) e invocar
    # O StrOutputParser apenas extrai o texto da resposta do LLM
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"history": history_text, "question": question})
    print(f"Resposta gerada: {answer} - Modelo utilizado: {model_name}")

    return {"answer": answer, "history": history + [{"question": question, "answer": answer}]}

class RouteQuery(BaseModel):
    """Decida a rota para uma pergunta do usuario"""
    route: Literal["factual", "research", "general"] = Field(
        description="A rota a ser seguida com base na pergunta do usuário.",
    )

def classify_question(state: GraphState):
    print("---NÓ: CLASSIFICADOR---")
    question = state['question']
   
    model_name = "google/gemma-3-12b"

    llm = ChatOpenAI(model_name = model_name,
                    openai_api_base = "http://192.168.0.30:1234/v1",
                    openai_api_key = "lm-studio",
                    temperature = 0.0,
                    max_tokens = -1)
    
    structured_llm = llm.with_structured_output(RouteQuery)
    
    system_prompt = """Você é um roteador especialista. Sua função é classificar a pergunta do usuário em uma de três categorias:
    1.  **factual**: Perguntas que podem ser respondidas com um fato direto e rápido. Ex: "Qual a capital da França?", "Quantos planetas existem no sistema solar?".
    2.  **research**: Perguntas que exigem uma pesquisa mais aprofundada, síntese de informações ou uma explicação detalhada. Ex: "Quais são as implicações da inteligência artificial na economia global?", "Faça um resumo sobre a Revolução Francesa".
    3.  **general**: Perguntas de conversação, pedidos criativos ou que não se encaixam nas outras categorias. Ex: "Olá, tudo bem?", "Escreva um poema sobre a chuva", "Me ajude a planejar minha viagem".
    """
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Classifique a seguinte pergunta: {question}"),
        ]
    )
    
    router_chain = prompt | structured_llm
    
    result = router_chain.invoke({"question": question})
    
    print(f"Pergunta: '{question}' foi classificada como: {result.route}")
    
    return {"classification": result.route}

def decide_route(state: GraphState):
    return state["classification"]


workflow = StateGraph(GraphState)

workflow.add_node("classifier", classify_question)
workflow.add_node("factual_handler", handle_factual)
workflow.add_node("research_handler", handle_research)
workflow.add_node("general_handler", handle_general)

workflow.set_entry_point("classifier")

workflow.add_conditional_edges(
    "classifier", # Nó de origem
    decide_route, # Função que decide o caminho
    {
        # Mapeamento: se a função retornar "X", vá para o nó "Y"
        "factual": "factual_handler",
        "research": "research_handler",
        "general": "general_handler",
    },
)

workflow.add_edge("factual_handler", END)
workflow.add_edge("research_handler", END)
workflow.add_edge("general_handler", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


print("\n--- Teste 1: Pergunta Factual ---")
inputs = {"question": "Qual é a altura do Monte Everest?"}
app.invoke(inputs, config={"configurable": {"thread_id": "1"}})

print("\n--- Teste 2: Pergunta Factual ---")
inputs = {"question": "Faça a pesquisa sobre a vida de Tesla?"}
app.invoke(inputs, config={"configurable": {"thread_id": "1"}})

print("\n--- Teste 3: Pergunta Factual ---")
inputs = {"question": "Qual foi a primeira pergunta que fiz?"}
app.invoke(inputs, config={"configurable": {"thread_id": "1"}})