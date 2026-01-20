import sqlite3
from langchain_core.tools import tool

def executar_consulta(sql: str, params: tuple) -> dict:
    """Função auxiliar para conectar ao banco e retornar um resultado como dicionário."""
    try:
        conn = sqlite3.connect('soc_ia.db')
        # Configura o row_factory para retornar resultados acessíveis por nome de coluna
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return None

@tool
def buscar_dados_evento(event_id: str) -> str:
    """Busca e retorna os detalhes de um evento de segurança específico pelo seu ID."""
    
    print(f"--- Ferramenta: Buscando logs para o evento {event_id} ---")
    
    sql = "SELECT * FROM eventos WHERE event_id = ?"
    resultado = executar_consulta(sql, (event_id,))
    
    if resultado:
        return f"Dados do Evento: {resultado}"
    return "Evento não encontrado no banco de dados."

@tool
def buscar_historico_usuario(user_id: str) -> str:
    """Busca e retorna o perfil e o nível de acesso de um colaborador pelo seu ID."""
    
    print(f"--- Ferramenta: Buscando perfil do usuário {user_id} ---")
    
    sql = "SELECT * FROM usuarios WHERE user_id = ?"
    resultado = executar_consulta(sql, (user_id,))
    
    if resultado:
        return f"ID do Usuário: {user_id}. Dados do Perfil: {resultado}"
    return "Usuário não encontrado."

@tool
def buscar_reputacao_ip(ip: str) -> str:
    """Busca e retorna o score de reputação e histórico de ameaças de um endereço IP."""
    
    print(f"--- Ferramenta: Buscando reputação para o IP {ip} ---")
    
    sql = "SELECT * FROM reputacao_ip WHERE ip = ?"
    resultado = executar_consulta(sql, (ip,))
    
    if resultado:
        return f"Dados de Reputacao de Rede: {resultado}"
    return "Dados de reputação não disponíveis para este IP."