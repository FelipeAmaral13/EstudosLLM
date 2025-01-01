from typing import TypedDict, List

class AgentState(TypedDict):
    """
    Representa o estado de um agente em um fluxo de trabalho para geração e validação de consultas SQL no contexto jurídico.

    Atributos:
        question (str): A pergunta ou tarefa jurídica fornecida pelo usuário que será traduzida em uma consulta SQL.
        table_schemas (str): Esquema do banco de dados jurídico, incluindo tabelas e colunas disponíveis.
        database (str): Nome do banco de dados jurídico utilizado.
        sql (str): Consulta SQL gerada pelo agente.
        reflect (List[str]): Lista de feedbacks ou reflexões para melhorar a consulta SQL.
        accepted (bool): Indica se a consulta SQL foi validada com sucesso.
        revision (int): Número de revisões realizadas na consulta SQL.
        max_revision (int): Número máximo de revisões permitidas para a consulta SQL.
    """
    question: str
    table_schemas: str
    database: str
    sql: str
    reflect: List[str]
    accepted: bool
    revision: int
    max_revision: int
