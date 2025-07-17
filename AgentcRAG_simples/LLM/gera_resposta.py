from langchain_core.output_parsers import StrOutputParser

from agent.agent_state import AgentState
from LLM.prompt import rag_prompt
from LLM.llm_model import llm



def gera_resposta(state: AgentState) -> AgentState:

    print("--- Nó: Gerando Resposta ---")
    question = state["question"]
    context = state["context"]
    rag_chain = (
        {"context": lambda x: x['context'], "question": lambda x: x['question']}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    print("Invocando cadeia RAG...")
    
    answer = rag_chain.invoke({"context": context, "question": question})
    print("Resposta gerada.")
    
    return {"answer": answer}