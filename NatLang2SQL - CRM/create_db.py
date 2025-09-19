import os
import sqlite3
from datetime import datetime, timedelta

DB_FILE = "crm_database.db"

def create_database():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print(f"Conectado ao banco de dados: {DB_FILE}")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_clientes (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            company TEXT,
            status TEXT CHECK(status IN ('Lead', 'Active', 'Inactive', 'Prospect')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        print("Tabela 'tb_clientes' verificada/criada.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_interacoes (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            interaction_date TIMESTAMP NOT NULL,
            type TEXT CHECK(type IN ('Email', 'Call', 'Meeting', 'Note')) NOT NULL,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES tb_clientes (customer_id)
        )
        """)

        print("Tabela 'tb_interacoes' verificada/criada.")

        conn.commit()

        print("Estrutura do banco de dados pronta.")

        return conn, cursor

    except sqlite3.Error as e:
        print(f"Erro ao criar/conectar ao banco de dados: {e}")
        if conn:
            conn.close()

        return None, None

def popula_tabelas(conn, cursor):

    print("Populando com dados de exemplo...")
    try:
        tb_clientes_data = [
            ('João Silva', 'joao.silva@email.com', '11-9999-0001', 'Empresa Alpha', 'Active'),
            ('Maria Oliveira', 'maria.o@sample.net', '21-8888-0002', 'Serviços Beta', 'Active'),
            ('Pedro Souza', 'pedro.souza@example.org', '31-7777-0003', 'Consultoria Gama', 'Lead'),
            ('Ana Costa', 'ana.costa@email.com', '41-6666-0004', 'Empresa Alpha', 'Inactive'),
            ('Carlos Lima', 'carlos.lima@sample.net', '51-5555-0005', 'Tec Delta', 'Prospect')
        ]

        inserted_tb_clientes = 0

        for customer in tb_clientes_data:
            try:
                cursor.execute("""
                INSERT INTO tb_clientes (name, email, phone, company, status)
                VALUES (?, ?, ?, ?, ?)
                """, customer)
                
                inserted_tb_clientes += 1

            except sqlite3.IntegrityError:
                print(f"Cliente com email {customer[1]} já existe. Ignorando.")

        print(f"{inserted_tb_clientes} novos clientes inseridos.")

        cursor.execute("SELECT customer_id, email FROM tb_clientes")
        customer_map = {email: cid for cid, email in cursor.fetchall()}

        today = datetime.now()

        tb_interacoes_data = [
            (customer_map.get('joao.silva@email.com'), (today - timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'), 'Call', 'Primeira ligação, mostrou interesse.'),
            (customer_map.get('joao.silva@email.com'), (today - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'), 'Email', 'Enviou proposta comercial.'),
            (customer_map.get('maria.o@sample.net'), (today - timedelta(days=20)).strftime('%Y-%m-%d %H:%M:%S'), 'Meeting', 'Reunião inicial de apresentação.'),
            (customer_map.get('maria.o@sample.net'), (today - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), 'Email', 'Follow-up pós reunião.'),
            (customer_map.get('pedro.souza@example.org'), (today - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), 'Note', 'Lead capturado via formulário do site.'),
            (customer_map.get('carlos.lima@sample.net'), (today - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'), 'Email', 'Contato inicial enviado.')
        ]

        valid_tb_interacoes = [inter for inter in tb_interacoes_data if inter[0] is not None]

        if valid_tb_interacoes:

            cursor.executemany("""
            INSERT INTO tb_interacoes (customer_id, interaction_date, type, notes)
            VALUES (?, ?, ?, ?)
            """, valid_tb_interacoes)

            print(f"{len(valid_tb_interacoes)} interações inseridas.")
        else:
            print("Nenhuma interação válida para inserir (verifique se os clientes foram inseridos).")

        conn.commit()
        print("Dados de exemplo inseridos com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados de exemplo: {e}")
        conn.rollback()

def main():

    if os.path.exists(DB_FILE):
        print(f"Banco de dados '{DB_FILE}' já existe.")

    conn, cursor = create_database()

    if conn and cursor:
        popula_tabelas(conn, cursor)
        conn.close()
        print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    print("\nIniciando a criação do banco de dados de CRM.\n")
    main()
    print("\nBanco de dados criado com sucesso.\n")
