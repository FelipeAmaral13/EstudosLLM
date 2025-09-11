from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
import uuid
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agentes.agent import DocumentAgent, ReasoningAgent, MetaAgent
from utilitarios.RAG import RAGModel
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Inicializar o RAG uma vez
try:
    rag_retriever = RAGModel()
    rag_retriever.carrega_documentos("dados/documentos/")
    rag_retriever.cria_vectordb()
    print("✅ RAG Model inicializado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao inicializar RAG Model: {e}")
    rag_retriever = None

class AgentState(TypedDict):
    query: str
    documents: List[str]
    summary: str
    reasoning: str
    final_answer: str

# Dicionário para armazenar o progresso das consultas
query_progress = {}

def node_document_agent(state: AgentState, session_id: str) -> dict:
    """Nó responsável por recuperar e resumir documentos"""
    query_progress[session_id]['status'] = 'Analisando documentos...'
    query_progress[session_id]['progress'] = 25
    
    agent = DocumentAgent()
    documents = rag_retriever.retrieve(state['query'])
    summary = agent.sumariza_documentos(documents, state['query'])
    
    query_progress[session_id]['summary'] = summary
    return {'documents': documents, 'summary': summary}

def node_reasoning_agent(state: AgentState, session_id: str) -> dict:
    """Nó responsável por realizar o raciocínio com base no resumo"""
    query_progress[session_id]['status'] = 'Processando raciocínio lógico...'
    query_progress[session_id]['progress'] = 60
    
    agent = ReasoningAgent()
    reasoning = agent.gera_raciocinio(state['summary'], state['query'])
    
    query_progress[session_id]['reasoning'] = reasoning
    return {'reasoning': reasoning}

def node_meta_agent(state: AgentState, session_id: str) -> dict:
    """Nó responsável por gerar a resposta final integrando resumo e raciocínio"""
    query_progress[session_id]['status'] = 'Gerando resposta final...'
    query_progress[session_id]['progress'] = 85
    
    agent = MetaAgent()
    final_answer = agent.gera_resposta_final(state['summary'], state['reasoning'], state['query'])
    
    query_progress[session_id]['final_answer'] = final_answer
    query_progress[session_id]['status'] = 'Concluído!'
    query_progress[session_id]['progress'] = 100
    
    return {'final_answer': final_answer}

def process_query_async(query: str, session_id: str):
    """Processa a query de forma assíncrona"""
    try:
        # Configurar o workflow
        workflow = StateGraph(AgentState)
        
        def document_node(state):
            return node_document_agent(state, session_id)
        
        def reasoning_node(state):
            return node_reasoning_agent(state, session_id)
        
        def meta_node(state):
            return node_meta_agent(state, session_id)
        
        workflow.add_node("document_agent", document_node)
        workflow.add_node("reasoning_agent", reasoning_node)
        workflow.add_node("meta_agent", meta_node)
        
        workflow.set_entry_point("document_agent")
        workflow.add_edge("document_agent", "reasoning_agent")
        workflow.add_edge("reasoning_agent", "meta_agent")
        workflow.add_edge("meta_agent", END)
        
        app_workflow = workflow.compile()
        
        # Estado inicial
        initial_state = AgentState(
            query=query,
            documents=[],
            summary="",
            reasoning="",
            final_answer=""
        )
        
        # Executar o workflow
        query_progress[session_id]['status'] = 'Iniciando processamento...'
        query_progress[session_id]['progress'] = 10
        
        result = app_workflow.invoke(initial_state)
        
    except Exception as e:
        query_progress[session_id]['status'] = f'Erro: {str(e)}'
        query_progress[session_id]['progress'] = 0
        query_progress[session_id]['error'] = str(e)

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    if not rag_retriever:
        return jsonify({'error': 'Sistema não inicializado. Verifique os documentos.'}), 500
    
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Pergunta não pode estar vazia.'}), 400
    
    session_id = session.get('session_id', str(uuid.uuid4()))
    session['session_id'] = session_id
    
    # Inicializar progresso
    query_progress[session_id] = {
        'query': query,
        'status': 'Preparando...',
        'progress': 0,
        'summary': '',
        'reasoning': '',
        'final_answer': '',
        'error': None
    }
    
    # Iniciar processamento assíncrono
    thread = threading.Thread(target=process_query_async, args=(query, session_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'session_id': session_id, 'status': 'started'})

@app.route('/progress')
def get_progress():
    session_id = session.get('session_id')
    if not session_id or session_id not in query_progress:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    return jsonify(query_progress[session_id])

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'rag_initialized': rag_retriever is not None,
        'documents_loaded': len(rag_retriever.documents) if rag_retriever else 0
    })

if __name__ == '__main__':
    print("\n🚀 Iniciando Interface Web para Análise de Contratos")
    print("📊 Sistema Multi-Agentes com RAG")
    print("🔗 Acesse: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)