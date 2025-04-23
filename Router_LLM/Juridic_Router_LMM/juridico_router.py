from typing import Dict, TypedDict, List
from groq import Groq
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
import logging
from dotenv import load_dotenv
import os

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

# Inicializa o cliente Groq
cliente_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELS = {
    "fast": ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    "powerful": ChatOpenAI(model="gpt-4", temperature=0.7),
    "groq": "qwen-2.5-32b"
}

# Log model initialization
logger.info("Initialized models: %s", list(MODELS.keys()))

TASK_PROMPTS = {
    "contratos": """
    Você é um assistente especializado em análise de contrato. Sua tarefa é analisar o contrato fornecido e extrair as seguintes informações de forma clara e estruturada:
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
        # Em caso de falha, tenta usar o Groq como fallback
        return {
            "task_type": "contratos",  # Define uma tarefa padrão
            "current_model": "groq",   # Usa o Groq como fallback
            "next_step": "process"
        }

def process_with_groq(prompt: str, model_name: str) -> str:
    """Processa o prompt usando o Groq."""
    try:
        response = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq processing failed: {str(e)}")
        raise e

def process_task(state: Agent, task_type: str) -> Dict:
    """Processa a tarefa usando o modelo atual ou Groq em caso de falha."""
    message = state["messages"][-1].content
    logger.info(f"Processing {task_type} with {state['current_model']} model")
    logger.debug(f"{task_type} content length: {len(message)} characters")
    
    model_name = state["current_model"]
    prompt = PromptTemplate(
        template=TASK_PROMPTS[task_type],
        input_variables=["input"]
    )
    
    try:
        if model_name == "groq":
            # Usa o Groq diretamente
            response = process_with_groq(prompt.format(input=message), MODELS["groq"])
        else:
            # Usa a OpenAI
            model = MODELS[model_name]
            chain = prompt | model
            response = chain.invoke({"input": message})
        
        logger.info(f"{task_type} processed successfully")
        return {
            "response": response,
            "next_step": "end"
        }
    except Exception as e:
        logger.error(f"{task_type} processing failed with {model_name}: {str(e)}")
        if model_name != "groq":
            logger.info("Trying Groq as fallback...")
            try:
                response = process_with_groq(prompt.format(input=message), MODELS["groq"])
                logger.info(f"{task_type} processed successfully with Groq")
                return {
                    "response": response,
                    "next_step": "end"
                }
            except Exception as groq_error:
                logger.error(f"{task_type} processing failed with Groq: {str(groq_error)}")
                return {
                    "response": f"Erro ao processar {task_type}: {str(groq_error)}",
                    "next_step": "end"
                }
        else:
            return {
                "response": f"Erro ao processar {task_type}: {str(e)}",
                "next_step": "end"
            }

def process_contratos(state: Agent) -> Dict:
    """Processa documentos ou perguntas relacionadas a contratos."""
    return process_task(state, "contratos")

def process_faturas(state: Agent) -> Dict:
    """Processa documentos ou perguntas relacionadas a faturas."""
    return process_task(state, "faturas")

def process_relatorios(state: Agent) -> Dict:
    """Processa documentos ou perguntas relacionadas a relatórios."""
    return process_task(state, "relatorios")

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
