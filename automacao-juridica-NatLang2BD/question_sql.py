import re
import uuid
from database.data_base import DatabaseManager
from flows.workflow import graph

class Question2SQL:
    def __init__(self):
        self.data_base = DatabaseManager()
        self.thread_id = None
        self.initial_state = {
            'question': '',
            'table_schemas': '',
            'database': '',
            'sql': '',
            'reflect': [],
            'accepted': False,
            'revision': 0,
            'max_revision': 3
        }

    def generate_unique_thread_id(self):
        """
        Gera um ID único para a thread.
        :return: String com o ID único da thread.
        """
        return str(uuid.uuid4())  # Gera um UUID único

    def set_question(self, question):
        """
        Define a pergunta inicial e atualiza o estado.
        :param question: Pergunta a ser processada.
        """
        self.initial_state['question'] = question

    def extract_sql(self, query_text):
        """
        Extrai a consulta SQL de um texto, buscando blocos delimitados ou instruções SELECT.
        :param query_text: Texto contendo a consulta SQL.
        :return: Consulta SQL extraída.
        """
        match = re.search(r'```sql\s*(.*?)\s*```', query_text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            match = re.search(r'(SELECT .*?);', query_text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip() + ';'
            else:
                return query_text.strip()

    def process_graph(self):
        """
        Executa o grafo de processamento baseado no estado inicial e obtém o estado final.
        :return: Estado final do grafo.
        """
        # Configura ou reutiliza o ID da thread
        if not self.thread_id:
            self.thread_id = self.generate_unique_thread_id()

        thread = {"configurable": {"thread_id": self.thread_id}}

        # Executar o grafo
        for _ in graph.stream(self.initial_state, thread):
            pass

        # Obter o estado final
        return graph.get_state(thread)

    def execute_query(self, clean_sql):
        """
        Executa a consulta SQL no banco de dados e retorna os resultados.
        :param clean_sql: Consulta SQL a ser executada.
        :return: Resultados da consulta.
        """
        try:
            self.data_base.cursor.execute(clean_sql)
            return self.data_base.cursor.fetchall()
        except Exception as e:
            print('Erro ao executar a consulta SQL:', e)
            return None
