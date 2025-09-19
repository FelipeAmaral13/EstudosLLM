import os
import streamlit as st
import sqlite3 
import operator
from dotenv import load_dotenv
from typing import Annotated, List, TypedDict
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain.tools import tool

DB_FILE = "crm_database.db" 

st.set_page_config(page_title="Project Linguagem Natural to SQL", page_icon=":100:", layout="wide")
st.title("Project Linguagem Natural to SQL ")
st.title("Gerenciamento de Memória e Contexto - Sistema Multi-Agentes de IA com LangGraph Para Automação do CRM e Consulta a Banco de Dados")

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

@tool
def query_crm_database(sql_query: str) -> str:
    # recebe uma string de consulta SQL e retorna uma string com o resultado
    """
    Executa uma consulta SQL SOMENTE do tipo SELECT no banco de dados CRM SQLite
    e retorna os resultados.
    Usamos esta ferramenta para obter informações sobre clientes ou interações.
    
    Tabelas disponíveis:

    1. tb_clientes (colunas: customer_id, name, email, phone, company, status, created_at)
       - status pode ser 'Lead', 'Active', 'Inactive', 'Prospect'
    2. tb_interacoes (colunas: interaction_id, customer_id, interaction_date, type, notes)
       - type pode ser 'Email', 'Call', 'Meeting', 'Note'

    Importante: Forneça APENAS consultas SQL `SELECT`. Não use `UPDATE`, `DELETE`, `INSERT` ou `DROP`.

    Exemplo de consulta SQL válida:
    'SELECT name, email FROM tb_clientes WHERE status = \\'Active\\';'
    'SELECT i.interaction_date, i.type, i.notes FROM tb_interacoes i JOIN tb_clientes c ON i.customer_id = c.customer_id WHERE c.name = \\'João Silva\\' ORDER BY i.interaction_date DESC;'
    """
    print(f"--- Ferramenta query_crm_database recebendo SQL: {sql_query} ---")

    if not sql_query.strip().upper().startswith("SELECT"):
        print("!!! ERRO DE SEGURANÇA: Tentativa de executar SQL não-SELECT !!!")
        return "Erro: Esta ferramenta só pode executar consultas SELECT."
    conn = None

    try:
        if not os.path.exists(DB_FILE):
            return f"Erro: Arquivo do banco de dados '{DB_FILE}' não encontrado. Execute o script 'create_crm_db.py' primeiro."

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        results = cursor.fetchall()
        if not results:
            return "Nenhum resultado encontrado para a consulta."

        else:
            column_names = [description[0] for description in cursor.description]
            header = " | ".join(column_names)

            # Converte cada linha de resultados em string, separando campos por " | "
            rows_str = [" | ".join(map(str, row)) for row in results]
            max_results = 15

            output = f"Resultados da consulta ({len(results)} encontrados):\n{header}\n" + "\n".join(rows_str[:max_results])

            if len(results) > max_results:
                output += f"\n... (mais {len(results) - max_results} resultados omitidos)"
            return output

    except sqlite3.Error as e:
        print(f"!!! ERRO SQL: {e} ao executar '{sql_query}' !!!")
        return f"Erro ao executar a consulta SQL: {e}. Verifique a sintaxe da sua consulta e os nomes das tabelas/colunas."
    except Exception as e:
        print(f"!!! ERRO Inesperado na ferramenta: {e} !!!")
        return f"Ocorreu um erro inesperado na ferramenta de banco de dados: {e}"
    finally:
        if conn:
            conn.close()

tools = [query_crm_database]
tool_node = ToolNode(tools)

def cria_agente_runnable(llm, system_prompt):

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name = "messages"),
        ]
    )
    agent_runnable = prompt | llm.bind_tools(tools)

    return agent_runnable

def groq_agent_node(state: AgentState):

    print("\n *** Executando o Nó Groq (CRM) *** \n")
    try:
        llm_groq = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.2) 
        
        system_prompt = """Você é um assistente de CRM chamado Groq (modelo Llama3).
        Sua principal função é responder perguntas sobre clientes e interações consultando o banco de dados CRM.
        Use a ferramenta 'query_crm_database' fornecendo uma consulta SQL SELECT válida para buscar as informações pedidas.
        Consulte a descrição da ferramenta para ver o schema do banco de dados (tabelas: tb_clientes, tb_interacoes e suas colunas).
        Seja direto e baseie suas respostas nos dados retornados pela ferramenta. Se a ferramenta retornar um erro, informe o usuário.
        Não invente informações se elas não estiverem no banco de dados.
        """
        
        agent_runnable = cria_agente_runnable(llm_groq, system_prompt)

        print("Runnable Groq (CRM) criado. Invocando...")
        response = agent_runnable.invoke({"messages": state['messages']})
        
        print(f"Nó Groq (CRM) Obteve Resposta: Tipo = {type(response)}, Conteúdo = '{response.content[:50]}...'")
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"Nó Groq (CRM) está chamando a ferramenta: {response.tool_calls}")
        
        return {"messages": [response]}

    except Exception as e:
        print(f"!!! ERRO NO NÓ Groq (CRM): {e} !!!")
        st.error(f"Ocorreu um erro ao contactar a API Groq: {e}")
        error_msg = AIMessage(content = f"[ERRO INTERNO GROQ]: Não foi possível processar com Groq. Detalhe: {e}", name = "ErroGroq")

        return {"messages": [error_msg]}

def openai_agent_node(state: AgentState):

    print("\n--- Executando Nó Agente OpenAI (CRM) ---")
    
    try:

        # Inicializa o LLM OpenAI com temperatura baixa e chave de API

        llm_openai = ChatOpenAI(model_name = 'qwen/qwen3-4b-2507',
                openai_api_base = "http://172.30.64.1:1234/v1",
                openai_api_key = "lm-studio",
                temperature = 0.0,
                max_tokens = -1)

        
        system_prompt = """Você é um assistente de CRM experiente chamado OpenAI (modelo GPT).
        Seu objetivo é ajudar o usuário com informações do banco de dados CRM.
        Utilize a ferramenta 'query_crm_database' para executar consultas SQL SELECT e buscar dados sobre clientes ou interações.
        Refira-se à descrição da ferramenta para entender o schema do banco (tabelas: tb_clientes, tb_interacoes; colunas relevantes como name, email, status, interaction_date, type, notes).
        Formule consultas SQL SELECT precisas com base na pergunta do usuário.
        Apresente os resultados de forma clara. Se encontrar um erro da ferramenta, comunique-o.
        Se a informação não estiver disponível, indique isso claramente.
        """
        agent_runnable = cria_agente_runnable(llm_openai, system_prompt)

        print("Runnable OpenAI (CRM) criado. Invocando...")
        response = agent_runnable.invoke({"messages": state['messages']})

        print(f"Nó OpenAI (CRM) Obteve Resposta: Tipo={type(response)}, Conteúdo='{response.content[:50]}...'")
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"Nó OpenAI (CRM) está chamando a ferramenta: {response.tool_calls}")
        
        return {"messages": [response]}

    except Exception as e:
        print(f"!!! ERRO NO NÓ OpenAI (CRM): {e} !!!")
        st.error(f"Ocorreu um erro ao contactar a API OpenAI: {e}")
        error_msg = AIMessage(content=f"[ERRO INTERNO OPENAI]: Não foi possível processar com OpenAI. Detalhe: {e}", name="ErroOpenAI")

        return {"messages": [error_msg]}

def route_junction_node(state: AgentState) -> dict:
    """Função para criação do nó de roteamento - grafo onde ocorre a decisão central"""
    print("--- Nó de Junção de Roteamento (Sem Mudança de Estado) ---")
    return {}

def router_logic(state: AgentState) -> str:
    print("\n--- Função Lógica de Roteamento (Decidindo Próximo Passo) ---")

    messages = state['messages']
    last_message = messages[-1] if messages else None
    if not last_message:
        print("Decisão Lógica: Sem mensagens no estado, terminando.")
        return "__end__"

    print(f"Roteador analisando última mensagem: Tipo={type(last_message).__name__}, Conteúdo='{last_message.content[:80]}...'")

    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print("Decisão Lógica: Última mensagem AI tem 'tool_calls'. Roteando para Ferramentas.")
        return "tools"
    if isinstance(last_message, AIMessage):
        print("Decisão Lógica: Resposta final da IA recebida (sem tool_calls). Terminando o ciclo atual.")
        return "__end__"

    if isinstance(last_message, HumanMessage):
        user_input_current = last_message.content.lower()
        print(f"Analisando última mensagem humana para menções: '{user_input_current}'")
        if "@openai" in user_input_current:
            print("Decisão Lógica: Roteando para OpenAI (menção explícita na última mensagem)")
            return "openai_agent"
        elif "@groq" in user_input_current:
            print("Decisão Lógica: Roteando para Groq (menção explícita na última mensagem)")
            return "groq_agent"

    if isinstance(last_message, ToolMessage):
        print("Decisão Lógica: Resultado da ferramenta recebido, roteando para um agente (via alternância)...")

    ai_message_count = sum(1 for msg in messages if isinstance(msg, AIMessage))
    print(f"Contagem atual de mensagens AI para alternância: {ai_message_count}")

    if ai_message_count % 2 == 0:
        print(f"Decisão Lógica: Roteando para Groq (padrão/alternado)")
        return "groq_agent"
    else:
        print(f"Decisão Lógica: Roteando para OpenAI (padrão/alternado)")
        return "openai_agent"
    
def compila_grafo():

    workflow = StateGraph(AgentState)
    workflow.add_node("openai_agent", openai_agent_node)
    workflow.add_node("groq_agent", groq_agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("router", route_junction_node)
    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        router_logic,
        {
            "tools": "tools",
            "groq_agent": "groq_agent",
            "openai_agent": "openai_agent",
            "__end__": END
        },
    )
    
    workflow.add_edge("openai_agent", "router")
    workflow.add_edge("groq_agent", "router")
    workflow.add_edge("tools", "router")
    app = workflow.compile()

    print("Grafo Compilado com Sucesso!")

    return app

if "app" not in st.session_state:

    if not os.path.exists(DB_FILE):
        st.error(f"Erro: O arquivo do banco de dados '{DB_FILE}' não foi encontrado.")
        st.info("Por favor, execute o script 'create_crm_db.py' no mesmo diretório para criar o banco de dados e depois recarregue esta página.")
        st.stop()

    st.write("Inicializando o grafo pela primeira vez...")

    try:
        st.session_state.app = compila_grafo()
        st.session_state.thread_id = "streamlit_thread_crm"

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Olá! Sou seu assistente de CRM. Pergunte-me sobre clientes ou interações (ex: 'Quais clientes estão ativos?', 'Mostre as interações de João Silva').")
            ]
        st.success("Grafo CRM inicializado.")
    
    except Exception as e:
        st.error(f"Erro crítico ao construir o grafo CRM: {e}")
        st.exception(e)
        st.stop()

st.sidebar.title("Memória")

with st.sidebar.expander("📜 Ver Histórico Completo da Conversa", expanded=False):
    if st.session_state.chat_history:
        for i, msg in enumerate(st.session_state.chat_history):
            role = "ai" if isinstance(msg, AIMessage) else ("tool" if isinstance(msg, ToolMessage) else "user")
            sender_display = "Usuário"
            if role == "ai":
                ai_message_index = sum(1 for m in st.session_state.chat_history[:i] if isinstance(m, AIMessage))
                is_groq_explicit = "@groq" in msg.content.lower()
                is_openai_explicit = "@openai" in msg.content.lower()
                msg_name = getattr(msg, 'name', None)
                
                if is_groq_explicit or (not is_openai_explicit and ai_message_index % 2 == 0 and not msg_name):
                    sender_display = "AI (Groq/Llama3)"
                elif is_openai_explicit or (not is_groq_explicit and ai_message_index % 2 != 0 and not msg_name):
                    sender_display = "AI (OpenAI/GPT)"
                elif msg_name:
                    sender_display = f"AI ({msg_name})"
                else:
                    sender_display = "AI (Assistente)"
            
            elif role == "tool":
                tool_name = getattr(msg, 'name', 'query_crm_database')
                sender_display = f"Ferramenta ({tool_name})"
            st.markdown(f"**{sender_display}:**")
            
            st.text_area(label=f"msg_{i}", value=msg.content, height=100, disabled=True, label_visibility="collapsed")
            
            if isinstance(msg, AIMessage) and getattr(msg, 'tool_calls', None):
                st.write("*Chamada(s) de Ferramenta:*")
                st.json([{'name': tc.get('name', 'N/A'), 'args': tc.get('args', {})} for tc in msg.tool_calls])
            
            if isinstance(msg, ToolMessage) and hasattr(msg, 'tool_call_id'):
                st.caption(f"ID da Chamada: {msg.tool_call_id}")
            
            st.divider()
    
    else:
        st.write("Nenhuma mensagem no histórico ainda.")

st.markdown("### Chat Ativo")
container_chat = st.container(height = 500)

with container_chat:
    for i, msg in enumerate(st.session_state.chat_history):
        role = "ai" if isinstance(msg, AIMessage) else ("tool" if isinstance(msg, ToolMessage) else "user")
        
        avatar_icon = "👤"
        sender_name = "Usuário"
        message_role_for_streamlit = "user"

        if role == "ai":
            message_role_for_streamlit = "assistant"
            ai_message_index = sum(1 for m in st.session_state.chat_history[:i] if isinstance(m, AIMessage))
            is_groq_explicit = "@groq" in msg.content.lower()
            is_openai_explicit = "@openai" in msg.content.lower()
            msg_name = getattr(msg, 'name', None)
            
            if is_groq_explicit or (not is_openai_explicit and ai_message_index % 2 == 0 and not msg_name):
                 avatar_icon = "🦙"
                 sender_name = "Groq (Llama3)"
            
            elif is_openai_explicit or (not is_groq_explicit and ai_message_index % 2 != 0 and not msg_name):
                 avatar_icon = "🤔"
                 sender_name = "OpenAI (GPT)"
            
            elif msg_name:
                 avatar_icon = "⚠️"
                 sender_name = f"Sistema ({msg_name})"
            
            else:
                 avatar_icon = "🤖"
                 sender_name = "Assistente"

        elif role == "tool":
            message_role_for_streamlit = "assistant"
            avatar_icon = "🛠️"
            sender_name = "Ferramenta"

        with st.chat_message(message_role_for_streamlit, avatar=avatar_icon):
            if role == "tool":
                tool_name = getattr(msg, 'name', 'query_crm_database')
                st.markdown(f"**Resultado Ferramenta ({tool_name})**:")
                st.code(f"{msg.content}", language=None)
                st.caption(f"ID Chamada: {msg.tool_call_id}")
            
            elif role == "ai":
                st.markdown(f"**{sender_name}:**")
                if getattr(msg, 'tool_calls', None):
                    st.write(f"*Chamando ferramenta(s):*")
                    st.json([{'name': tc.get('name', 'N/A'), 'args': tc.get('args', {})} for tc in msg.tool_calls])
                st.markdown(msg.content)
            else:
                st.markdown(msg.content)

if prompt := st.chat_input("Faça uma pergunta sobre o CRM..."):
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    st.rerun()

if st.session_state.chat_history and isinstance(st.session_state.chat_history[-1], HumanMessage):
    last_human_message = st.session_state.chat_history[-1]
    if not st.session_state.get("processing_lock", False):
        st.session_state["processing_lock"] = True
        current_state = {"messages": st.session_state.chat_history}

        with st.spinner("Consultando CRM e pensando..."):
            final_state = None

            try:
                final_state = st.session_state.app.invoke(current_state)
                if final_state and "messages" in final_state:
                    new_messages = final_state["messages"][len(current_state["messages"]):]
                    if new_messages:
                        st.session_state.chat_history.extend(new_messages)
                    else:
                        st.toast("O grafo não retornou novas mensagens desta vez.", icon="🤔")
                else:
                    st.toast("O grafo retornou um estado inválido.", icon="error")
                    
                    st.session_state.chat_history.append(AIMessage(content="Desculpe, ocorreu um erro interno no estado do grafo."))
            
            except Exception as e:
                st.error(f"Erro durante a execução do grafo: {e}")
                st.session_state.chat_history.append(AIMessage(content=f"Desculpe, ocorreu um erro: {e}"))
            
            finally:
                st.session_state["processing_lock"] = False
                st.rerun()

st.sidebar.divider()
st.sidebar.title("Instruções")

st.sidebar.markdown("""
Digite sua pergunta ao lado para conversar com os Agentes de IA.

Os Agentes são capazes de consultar o banco de dados de CRM para extrair as respostas.

Tipos de perguntas:
- **Quais clientes estão ativos?**
- **Qual interação foi feita com João Silva?**
- **Cite o nome de um dos clientes listados anteriormente.**
- **Quais clientes tiveram interação por e-mail?**
- **Algum cliente foi lead capturado com interação via formulário do site?**
- **Quais interações ocorreram em 29-04-2025?**

IA Generativa comete erros. **SEMPRE** use seu conhecimento para verificar as respostas.
""")


