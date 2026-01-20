import sqlite3

# Conecta ao banco de dados (será criado se não existir)
conn = sqlite3.connect('soc_ia.db')
cursor = conn.cursor()

# 1. Criação da Tabela de Usuários (Colaboradores)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    user_id TEXT PRIMARY KEY,
    nome TEXT,
    departamento TEXT,
    nivel_acesso TEXT,
    localizacao_habitual TEXT,
    dispositivo_padrao TEXT
)
''')

# 2. Criação da Tabela de Reputação de Rede
cursor.execute('''
CREATE TABLE IF NOT EXISTS reputacao_ip (
    ip TEXT PRIMARY KEY,
    score_reputacao INTEGER,
    blacklisted BOOLEAN,
    tentativas_falhas_24h INTEGER
)
''')

# 3. Criação da Tabela de Eventos de Segurança
cursor.execute('''
CREATE TABLE IF NOT EXISTS eventos (
    event_id TEXT PRIMARY KEY,
    user_id TEXT,
    tipo_evento TEXT,
    recurso TEXT,
    source_ip TEXT,
    dispositivo TEXT,
    localizacao TEXT,
    FOREIGN KEY (user_id) REFERENCES usuarios(user_id),
    FOREIGN KEY (source_ip) REFERENCES reputacao_ip(ip)
)
''')

# --- Inserção de Dados ---

usuarios_data = [
    ("USR_ID_001", "Carlos Alberto", "Financeiro", "Médio", "São Paulo, SP", "Notebook-Corp-01"),
    ("USR_ID_002", "Beatriz Silva", "TI / DevOps", "Crítico", "Curitiba, PR", "Workstation-Dev-05"),
    ("USR_ID_003", "Amanda Oliveira", "Vendas", "Baixo", "Belo Horizonte, MG", "Smartphone-Sales-12"),
    ("USR_ID_004", "Ricardo Menezes", "RH", "Médio", "Rio de Janeiro, RJ", "Notebook-Corp-22"),
    ("USR_ID_005", "Mariana Souza", "Diretoria", "Crítico", "São Paulo, SP", "MacBook-CEO")
]

reputacao_data = [
    ("192.168.1.50", 95, 0, 0),
    ("10.0.0.122", 100, 0, 1),
    ("177.45.12.99", 20, 1, 45),
    ("201.18.55.21", 85, 0, 2),
    ("45.122.10.5", 10, 1, 150),
    ("189.12.33.44", 70, 0, 5),
    ("13.52.1.88", 40, 0, 12),
    ("8.8.8.8", 98, 0, 0)
]

eventos_data = [
    ("EVT101", "USR_ID_001", "Login SSH", "Servidor-Pagamentos", "192.168.1.50", "Notebook-Corp-01", "São Paulo, SP"),
    ("EVT102", "USR_ID_002", "Acesso DB", "PostgreSQL-Prod", "10.0.0.122", "Workstation-Dev-05", "Curitiba, PR"),
    ("EVT103", "USR_ID_002", "Brute Force", "Gateway-VPN", "177.45.12.99", "Desconhecido", "Moscou, Rússia"),
    ("EVT104", "USR_ID_003", "Login Web", "Portal-Vendas", "201.18.55.21", "Smartphone-Sales-12", "Belo Horizonte, MG"),
    ("EVT105", "USR_ID_005", "Download Massa", "OneDrive-Corp", "45.122.10.5", "Desconhecido", "Pequim, China"),
    ("EVT106", "USR_ID_004", "Login Web", "Portal-RH", "189.12.33.44", "Notebook-Corp-22", "Rio de Janeiro, RJ"),
    ("EVT107", "USR_ID_001", "Escalação Privilégio", "Servidor-Financeiro", "192.168.1.50", "Notebook-Corp-01", "São Paulo, SP"),
    ("EVT108", "USR_ID_002", "Acesso Negado", "S3-Bucket-Backup", "13.52.1.88", "Cloud-Shell", "Ashburn, EUA"),
    ("EVT109", "USR_ID_003", "Login Web", "Portal-Vendas", "201.18.55.21", "Tablet-Home", "Belo Horizonte, MG"),
    ("EVT110", "USR_ID_005", "Login Admin", "Console-AWS", "8.8.8.8", "MacBook-CEO", "São Paulo, SP"),
    ("EVT111", "USR_ID_004", "Exclusão Arquivo", "Sharepoint-RH", "189.12.33.44", "Notebook-Corp-22", "Rio de Janeiro, RJ"),
    ("EVT112", "USR_ID_002", "Alteração DNS", "Core-Router", "10.0.0.122", "Workstation-Dev-05", "Curitiba, PR"),
    ("EVT113", "USR_ID_001", "Transferência FTP", "FTP-Externo", "45.122.10.5", "Desconhecido", "Kiev, Ucrânia"),
    ("EVT114", "USR_ID_003", "Login Falho", "Portal-Vendas", "177.45.12.99", "Mobile-Unknown", "Madrid, Espanha"),
    ("EVT115", "USR_ID_005", "Acesso API", "API-Gateway", "192.168.1.50", "MacBook-CEO", "São Paulo, SP")
]

# Executa as inserções
cursor.executemany("INSERT INTO usuarios VALUES (?,?,?,?,?,?)", usuarios_data)
cursor.executemany("INSERT INTO reputacao_ip VALUES (?,?,?,?)", reputacao_data)
cursor.executemany("INSERT INTO eventos VALUES (?,?,?,?,?,?,?)", eventos_data)

# Salva e fecha
conn.commit()
conn.close()

print("Banco de dados 'soc_ia.db' criado e populado com sucesso!")