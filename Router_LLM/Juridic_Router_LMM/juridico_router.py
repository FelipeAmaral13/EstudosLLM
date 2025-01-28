from typing import Dict, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
import logging
from dotenv import load_dotenv

load_dotenv()

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Agent(TypedDict):
    messages: List[BaseMessage]
    task_type: str
    next_step: str
    response: str
    current_model: str

MODELS = {
    "fast": ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    "powerful": ChatOpenAI(model="gpt-4", temperature=0.7)
}

# Log model initialization
logger.info("Initialized models: %s", list(MODELS.keys()))

TASK_PROMPTS = {
    "contratos": """
    Analise o contrato abaixo e extraia as seguintes informações:
    - Partes envolvidas
    - Data de vigência
    - Cláusulas importantes (ex: rescisão, pagamento, confidencialidade)
    - Riscos potenciais (ex: multas, prazos curtos)

    Contrato: {input}

    Retorne um JSON com os campos:
    - partes_envolvidas: lista das partes
    - data_vigencia: data de início e término
    - clausulas_importantes: lista de cláusulas relevantes
    - riscos: descrição dos riscos identificados
    """,
    
    "faturas": """
    Analise a fatura abaixo e verifique:
    - Número da fatura
    - Data de emissão
    - Valor total
    - Itens cobrados (descrição e valor de cada item)
    - Inconsistências (ex: valores incorretos, itens duplicados)

    Fatura: {input}

    Retorne um JSON com os campos:
    - numero_fatura: número da fatura
    - data_emissao: data de emissão
    - valor_total: valor total da fatura
    - itens_cobrados: lista de itens com descrição e valor
    - inconsistencias: descrição de inconsistências encontradas
    """,
    
    "relatorios": """
    Analise o relatório abaixo e extraia as seguintes informações:
    - Objetivo do relatório
    - Principais conclusões
    - Recomendações
    - Dados relevantes (ex: números, estatísticas)

    Relatório: {input}

    Retorne um JSON com os campos:
    - objetivo: objetivo do relatório
    - conclusoes: principais conclusões
    - recomendacoes: recomendações sugeridas
    - dados_relevantes: lista de dados ou estatísticas importantes
    """
}

# Log prompt templates initialization
logger.info("Initialized prompt templates for tasks: %s", list(TASK_PROMPTS.keys()))

CLASSIFIER_PROMPT = """
Analise a pergunta ou solicitação e classifique em uma das seguintes categorias:
- contratos: para pedidos relacionados a análise, revisão ou extração de informações de contratos.
- faturas: para tarefas relacionadas a verificação, análise ou identificação de inconsistências em faturas.
- relatorios: para solicitações de análise, resumo ou extração de informações de relatórios.

Pergunta: {input}

Retorne apenas um JSON com os campos:
- task_type: tipo da tarefa (contratos, faturas, relatorios)
- explanation: breve explicação da classificação
- recommended_model: "fast" para tarefas simples ou "powerful" para tarefas complexas
"""

class ClassifierOutput(TypedDict):
    task_type: str
    explanation: str
    recommended_model: str

classifier_parser = JsonOutputParser(pydantic_object=ClassifierOutput)
logger.info("Initialized classifier parser")

def create_classifier_chain():
    """Cria a chain para classificação de tarefas"""
    logger.debug("Creating classifier chain")
    prompt = PromptTemplate(
        template=CLASSIFIER_PROMPT,
        input_variables=["input"]
    )
    
    chain = (
        prompt 
        | MODELS["fast"] 
        | classifier_parser
    )
    logger.debug("Classifier chain created successfully")
    return chain

def classify_task(state: Agent) -> Dict:
    """Classifica a tarefa e atualiza o estado"""
    message = state["messages"][-1].content
    logger.info("Starting task classification for message: %s", message[:100] + "..." if len(message) > 100 else message)
    
    classifier_chain = create_classifier_chain()
    
    try:
        result = classifier_chain.invoke({"input": message})
        logger.info("Task classified as: %s using %s model", result["task_type"], result["recommended_model"])
        logger.debug("Classification explanation: %s", result["explanation"])
        
        return {
            "task_type": result["task_type"],
            "current_model": result["recommended_model"],
            "next_step": "process"
        }
    except Exception as e:
        logger.error("Task classification failed: %s", str(e), exc_info=True)
        return {
            "task_type": "general",
            "current_model": "fast",
            "next_step": "process"
        }

def process_contratos(state: Agent) -> Dict:
    """Processa documentos ou perguntas relacionadas a contratos."""
    message = state["messages"][-1].content
    logger.info("Processing contract with %s model", state["current_model"])
    logger.debug("Contract content length: %d characters", len(message))
    
    model = MODELS[state["current_model"]]
    prompt = PromptTemplate(
        template=TASK_PROMPTS["contratos"],
        input_variables=["input"]
    )
    
    try:
        chain = prompt | model
        logger.debug("Contract processing chain created")
        
        response = chain.invoke({"input": message})
        logger.info("Contract processed successfully")
        logger.debug("Contract analysis response: %s", response)
        
        return {
            "response": response,
            "next_step": "end"
        }
    except Exception as e:
        logger.error("Contract processing failed: %s", str(e), exc_info=True)
        return {
            "response": f"Erro ao processar contrato: {str(e)}",
            "next_step": "end"
        }

def process_faturas(state: Agent) -> Dict:
    """Processa documentos ou perguntas relacionadas a faturas."""
    message = state["messages"][-1].content
    logger.info("Processing invoice with %s model", state["current_model"])
    logger.debug("Invoice content length: %d characters", len(message))
    
    model = MODELS[state["current_model"]]
    prompt = PromptTemplate(
        template=TASK_PROMPTS["faturas"],
        input_variables=["input"]
    )
    
    try:
        chain = prompt | model
        logger.debug("Invoice processing chain created")
        
        response = chain.invoke({"input": message})
        logger.info("Invoice processed successfully")
        logger.debug("Invoice analysis response: %s", response)
        
        return {
            "response": response,
            "next_step": "end"
        }
    except Exception as e:
        logger.error("Invoice processing failed: %s", str(e), exc_info=True)
        return {
            "response": f"Erro ao processar fatura: {str(e)}",
            "next_step": "end"
        }

def process_relatorios(state: Agent) -> Dict:
    """Processa documentos ou perguntas relacionadas a relatórios."""
    message = state["messages"][-1].content
    logger.info("Processing report with %s model", state["current_model"])
    logger.debug("Report content length: %d characters", len(message))
    
    model = MODELS[state["current_model"]]
    prompt = PromptTemplate(
        template=TASK_PROMPTS["relatorios"],
        input_variables=["input"]
    )
    
    try:
        chain = prompt | model
        logger.debug("Report processing chain created")
        
        response = chain.invoke({"input": message})
        logger.info("Report processed successfully")
        logger.debug("Report analysis response: %s", response)
        
        return {
            "response": response,
            "next_step": "end"
        }
    except Exception as e:
        logger.error("Report processing failed: %s", str(e), exc_info=True)
        return {
            "response": f"Erro ao processar relatório: {str(e)}",
            "next_step": "end"
        }

def create_graph():
    """Cria o grafo de processamento para triagem de documentos."""
    logger.info("Creating processing graph")
    
    graph = StateGraph(Agent)
    logger.debug("State graph initialized")

    # Adiciona os nós
    graph.add_node("classify", classify_task)
    graph.add_node("process_contratos", process_contratos)
    graph.add_node("process_faturas", process_faturas)
    graph.add_node("process_relatorios", process_relatorios)
    logger.debug("Graph nodes added")

    # Configura as conexões
    graph.set_entry_point("classify")
    
    # Conexões condicionais
    graph.add_conditional_edges(
        "classify",
        lambda state: state["task_type"],
        {
            "contratos": "process_contratos",
            "faturas": "process_faturas",
            "relatorios": "process_relatorios"
        }
    )
    logger.debug("Conditional edges configured")

    # Conexões para finalização
    graph.add_edge("process_contratos", END)
    graph.add_edge("process_faturas", END)
    graph.add_edge("process_relatorios", END)
    logger.debug("End edges added")

    workflow = graph.compile()
    logger.info("Processing graph created and compiled successfully")
    return workflow

class LangGraphRouter:
    def __init__(self):
        logger.info("Initializing LangGraphRouter")
        self.workflow = create_graph()
        logger.info("LangGraphRouter initialized successfully")
    
    def process_question(self, question: str) -> str:
        """Processa uma pergunta através do workflow"""
        logger.info("Processing new question")
        logger.debug("Question content: %s", question[:100] + "..." if len(question) > 100 else question)
        
        try:
            config = self.workflow.invoke({
                "messages": [HumanMessage(content=question)],
                "task_type": "",
                "next_step": "",
                "response": "",
                "current_model": ""
            })
            
            logger.info("Question processed successfully")
            return config["response"]
        except Exception as e:
            logger.error("Question processing failed: %s", str(e), exc_info=True)
            return f"Erro ao processar sua pergunta: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    logger.info("Starting main application")
    
    router = LangGraphRouter()
    
    contrato_exemplo = """
    Este contrato é celebrado entre a Empresa XYZ Ltda., com sede em São Paulo, Brasil, 
    inscrita no CNPJ 12.345.678/0001-99, e o Cliente ABC S.A., com sede no Rio de Janeiro, Brasil, 
    inscrita no CNPJ 98.765.432/0001-11.

    Data de vigência: 01/01/2025 a 31/12/2025.

    Cláusulas importantes:
    1. Pagamento: O valor total de R$ 500.000,00 será pago em 5 parcelas mensais de R$ 100.000,00.
    2. Rescisão: O contrato poderá ser rescindido com aviso prévio de 30 dias.
    3. Confidencialidade: Ambas as partes comprometem-se a manter as informações confidenciais.
    4. Multas: Em caso de atraso nos pagamentos, será aplicada uma multa de 2% sobre o valor devido.

    Riscos:
    - Multas por atraso no pagamento.
    - Curto prazo para rescisão, dificultando reorganizações.

    Assinam o presente contrato as partes mencionadas.
    """
    
    logger.info("Testing contract extraction")
    resposta = router.process_question(contrato_exemplo)
    print(f"Resposta:\n{resposta}")

    fatura_exemplo = """
    Número da Fatura: 12345
    Data de Emissão: 15/01/2025
    Valor Total: R$ 2.450,00

    Itens Cobrados:
    1. Serviço de Consultoria - R$ 1.500,00
    2. Licença de Software - R$ 750,00
    3. Taxa de Manutenção - R$ 200,00

    Inconsistências Identificadas:
    - Item duplicado: Taxa de Manutenção apareceu duas vezes.
    - Valor total incorreto: Soma dos itens resulta em R$ 2.450,00, mas o correto seria R$ 2.450,00.
    """

    logger.info("Testing invoice extraction")
    resposta = router.process_question(fatura_exemplo)
    print(f"Resposta:\n{resposta}")