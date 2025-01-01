import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, Optional, List, Dict
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DatabaseManager:
    def __init__(self, dbname: str = "sistema_juridico", host: str = "localhost", port: str = "5432"):
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=host,
                port=port,
                options="-c client_encoding=utf-8"
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            logger.info("Conexão com o banco de dados estabelecida.")
        except psycopg2.Error as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def create_tables(self) -> None:
        """Criação das tabelas."""
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cpf VARCHAR(11) UNIQUE NOT NULL,
                telefone VARCHAR(15),
                email VARCHAR(100)
            );

            CREATE TABLE IF NOT EXISTS advogados (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                oab VARCHAR(15) UNIQUE NOT NULL,
                especialidade VARCHAR(50)
            );

            CREATE TABLE IF NOT EXISTS casos (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(100) NOT NULL,
                descricao TEXT NOT NULL,
                cliente_id INT REFERENCES clientes(id),
                advogado_id INT REFERENCES advogados(id),
                data_abertura DATE NOT NULL,
                status VARCHAR(50) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audiencias (
                id SERIAL PRIMARY KEY,
                caso_id INT REFERENCES casos(id),
                data DATE NOT NULL,
                status VARCHAR(50) NOT NULL
            );
            """)
            self.connection.commit()
            logger.info("Tabelas criadas com sucesso.")
        except psycopg2.Error as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            self.connection.rollback()

    def query(self, sql: str, params: Optional[List[Any]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Método genérico para executar consultas no banco de dados.

        :param sql: Consulta SQL a ser executada.
        :param params: Parâmetros para a consulta (opcional).
        :return: Resultado da consulta ou None.
        """
        try:
            self.cursor.execute(sql, params)
            if sql.strip().lower().startswith("select"):
                result = self.cursor.fetchall()
                logger.info(f"Consulta SELECT executada: {sql}")
                return result
            else:
                self.connection.commit()
                logger.info(f"Consulta não-SELECT executada: {sql}")
                return self.cursor.rowcount
        except psycopg2.Error as e:
            logger.error(f"Erro ao executar a query: {e}")
            self.connection.rollback()
            return None

    def get_database_schema(self) -> str:
        """
        Retorna o esquema do banco de dados atual.

        :return: String contendo o esquema do banco de dados.
        """
        schema = ''
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = self.cursor.fetchall()
            for table in tables:
                table_name = table['table_name']
                schema += f"Table: {table_name}\n"
                schema += "Columns:\n"
                self.cursor.execute(
                    "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;",
                    (table_name,)
                )
                columns = self.cursor.fetchall()
                for column in columns:
                    schema += f" - {column['column_name']} ({column['data_type']})\n"
                schema += '\n'
            logger.info("Esquema do banco de dados recuperado com sucesso.")
        except psycopg2.Error as e:
            logger.error(f"Erro ao obter o esquema do banco de dados: {e}")
        return schema

    def close_connection(self) -> None:
        """Fecha a conexão com o banco de dados."""
        try:
            self.cursor.close()
            self.connection.close()
            logger.info("Conexão com o banco de dados fechada.")
        except psycopg2.Error as e:
            logger.error(f"Erro ao fechar a conexão com o banco de dados: {e}")
