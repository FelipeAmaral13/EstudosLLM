from database.data_base import DatabaseManager
from database.dados import clientes, advogados, casos, audiencias

data_base = DatabaseManager()

# Criar o banco de dados
data_base.create_tables()

# Inserção dos dados
data_base.cursor.executemany("""
    INSERT INTO clientes (id, nome, cpf, telefone, email) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (id) DO NOTHING;
""", clientes)

data_base.cursor.executemany("""
    INSERT INTO advogados (id, nome, oab, especialidade) 
    VALUES (%s, %s, %s, %s) 
    ON CONFLICT (id) DO NOTHING;
""", advogados)

data_base.cursor.executemany("""
    INSERT INTO casos (id, titulo, descricao, cliente_id, advogado_id, data_abertura, status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT (id) DO NOTHING;
""", casos)

data_base.cursor.executemany("""
    INSERT INTO audiencias (id, caso_id, data, status) 
    VALUES (%s, %s, %s, %s) 
    ON CONFLICT (id) DO NOTHING;
""", audiencias)

# Confirmar as alterações
data_base.connection.commit()

# Query para testar os dados
clientes_result = data_base.query('SELECT * FROM clientes;')
advogados_result = data_base.query('SELECT * FROM advogados;')
casos_result = data_base.query('SELECT * FROM casos;')
audiencias_result = data_base.query('SELECT * FROM audiencias;')

# Exibir resultados
print("Clientes:")
for cliente in clientes_result:
    print(cliente)

print("\nAdvogados:")
for advogado in advogados_result:
    print(advogado)

print("\nCasos:")
for caso in casos_result:
    print(caso)

print("\nAudiências:")
for audiencia in audiencias_result:
    print(audiencia)

# Fechar a conexão
data_base.close_connection()
