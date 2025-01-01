import re
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from typing import Any, Dict

from models.agent_state import AgentState
from database.data_base import DatabaseManager

# Carrega variáveis de ambiente
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Inicializa o modelo ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
data_base = DatabaseManager()

# Prompts reutilizáveis para o cenário jurídico
ROLE_PROMPTS = {
    "sql_writer": """
        Você é um especialista em SQL e Direito. Sua tarefa é escrever **apenas** a consulta SQL que responda à pergunta do usuário relacionada a um cenário jurídico. A consulta deve:

        - Usar nomes de tabelas e colunas conforme o esquema do banco de dados jurídico.
        - Garantir que consultas de valores textuais sejam realizadas de forma insensível a maiúsculas e minúsculas.
        - Não incluir explicações ou comentários.
        - Retornar apenas a consulta SQL válida.
    """,
    "qa_engineer": """
        Você é um engenheiro de QA especializado em Direito e SQL. Sua tarefa é verificar se a consulta SQL fornecida responde corretamente à pergunta jurídica do usuário.
    """,
    "chief_dba": """
        Você é um DBA experiente em sistemas jurídicos. Sua tarefa é fornecer feedback detalhado para melhorar a consulta SQL fornecida.
    """
}

def invoke_llm_safe(role_prompt: str, instruction: str) -> str:
    """
    Invoca o modelo LLM com segurança, tratando erros adequadamente.

    Args:
        role_prompt (str): O prompt para o papel do modelo.
        instruction (str): A instrução detalhada para o modelo.

    Returns:
        str: Resposta processada do modelo.
    """
    try:
        messages = [
            SystemMessage(content=role_prompt),
            HumanMessage(content=instruction)
        ]
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        return f"Erro ao invocar o LLM: {e}"

def build_instruction(state: AgentState, question: str, sql: str = None) -> str:
    """
    Constrói a instrução para o modelo com base no estado e na tarefa.

    Args:
        state (AgentState): Estado atual do agente.
        question (str): A questão a ser respondida.
        sql (str, optional): A consulta SQL existente, se aplicável.

    Returns:
        str: Instrução formatada para o modelo.
    """
    instruction = f"Com base no seguinte esquema de banco de dados jurídico:\n{state['table_schemas']}\n"
    if sql:
        instruction += f"E na seguinte consulta SQL:\n{sql}\n"
    instruction += f"{question}\n"
    return instruction

def normalize_question(question: str) -> str:
    """
    Normaliza a pergunta para garantir que consultas textuais sejam insensíveis a maiúsculas e minúsculas.

    Args:
        question (str): Pergunta fornecida pelo usuário.

    Returns:
        str: Pergunta normalizada.
    """
    return question.strip().lower()

def initialize_database_state(state: AgentState) -> Dict[str, Any]:
    """
    Configura o estado com o esquema do banco de dados e o nome do banco.

    Args:
        state (AgentState): Estado atual do agente.

    Returns:
        Dict[str, Any]: Estado atualizado com o esquema do banco de dados e nome do banco.
    """
    state['table_schemas'] = data_base.get_database_schema()
    state['database'] = 'sistema_juridico'
    return {"table_schemas": state['table_schemas'], "database": state['database']}

def generate_sql_query(state: AgentState) -> Dict[str, Any]:
    """
    Gera uma consulta SQL usando um modelo LLM baseado no esquema do banco de dados e na pergunta jurídica do usuário.

    Args:
        state (AgentState): Estado atual do agente.

    Returns:
        Dict[str, Any]: Consulta SQL gerada e revisão incrementada.
    """
    role_prompt = ROLE_PROMPTS["sql_writer"]
    normalized_question = normalize_question(state['question'])
    instruction = build_instruction(state, f"Escreva a consulta SQL que responda à seguinte pergunta jurídica: {normalized_question}")
    sql = invoke_llm_safe(role_prompt, instruction)
    return {"sql": sql, "revision": state['revision'] + 1}

def validate_sql_query(state: AgentState) -> Dict[str, Any]:
    """
    Valida a consulta SQL fornecida em relação à pergunta jurídica e ao esquema do banco de dados.

    Args:
        state (AgentState): Estado atual do agente.

    Returns:
        Dict[str, Any]: Resultado da validação.
    """
    role_prompt = ROLE_PROMPTS["qa_engineer"]
    normalized_question = normalize_question(state['question'])
    instruction = build_instruction(state, f"Verifique se a consulta SQL pode completar a tarefa jurídica: {normalized_question}", sql=state['sql'])
    response = invoke_llm_safe(role_prompt, instruction)
    return {"accepted": 'ACEITO' in response.upper()}

def provide_sql_feedback(state: AgentState) -> Dict[str, Any]:
    """
    Fornece feedback detalhado para melhorar a consulta SQL fornecida.

    Args:
        state (AgentState): Estado atual do agente.

    Returns:
        Dict[str, Any]: Feedback detalhado sobre a consulta SQL.
    """
    role_prompt = ROLE_PROMPTS["chief_dba"]
    normalized_question = normalize_question(state['question'])
    instruction = build_instruction(state, f"Por favor, forneça recomendações úteis e detalhadas para melhorar a consulta SQL para a tarefa jurídica: {normalized_question}", sql=state['sql'])
    reflect = invoke_llm_safe(role_prompt, instruction)
    state['reflect'].append(reflect)
    return {"reflect": state['reflect']}
