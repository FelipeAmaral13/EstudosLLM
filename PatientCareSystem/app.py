import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv(dotenv_path='.config')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)

def db_conn():
    conn = sqlite3.connect(os.path.join("bd_llm_analise_sintoma", "db", "db_pacientes.db"))
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    with db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_dados_pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                nome_paciente TEXT NOT NULL,
                idade INTEGER NOT NULL,
                genero TEXT NOT NULL,
                sintomas TEXT NOT NULL
            );
        ''')
        conn.commit()
    conn.close()

def insert_data(cpf, nome, idade, genero, sintomas):
    with db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tb_dados_pacientes (cpf, nome_paciente, idade, genero, sintomas)
            VALUES (?, ?, ?, ?, ?)
        ''', (cpf, nome, idade, genero, sintomas))
        conn.commit()
    conn.close()

def search_pacientes_by_option(option, query):
    conn = db_conn()
    cursor = conn.cursor()
    
    if option == "CPF":
        cursor.execute('SELECT * FROM tb_dados_pacientes WHERE cpf LIKE ?', ('%' + query + '%',))
    elif option == "Nome":
        cursor.execute('SELECT * FROM tb_dados_pacientes WHERE nome_paciente LIKE ?', ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def delete_data(cpf):
    conn = sqlite3.connect(os.path.join("bd_llm_analise_sintoma", "db", "db_pacientes.db"))
    c = conn.cursor()
    c.execute('DELETE FROM tb_dados_pacientes WHERE cpf = ?', (cpf,))
    conn.commit()
    conn.close()

def update_data(cpf, nome, idade, genero, sintomas):
    conn = sqlite3.connect(os.path.join("bd_llm_analise_sintoma", "db", "db_pacientes.db"))
    cursor = conn.cursor()
    cursor.execute('''
            UPDATE tb_dados_pacientes
            SET nome_paciente = ?, idade = ?, genero = ?, sintomas = ?
            WHERE cpf = ?
        ''', (nome, idade, genero, sintomas, cpf))
    conn.commit()
    conn.close()


def llm_recomendar_tratamento(cpf):
    with db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_dados_pacientes WHERE cpf = ?", (cpf,))
        paciente = cursor.fetchone()
    conn.close()

    if paciente:
        template = PromptTemplate.from_template(
            """Você é um especialista médico capaz de recomendar tratamentos personalizados. 
            Por favor forneça recomendações de tratamento, baseado nos seguintes dados: {dados}"""
        )
        prompt = template.format(
            dados=f"""Paciente: {paciente['nome_paciente']}
            \nSintomas: {paciente['sintomas']}
            \nIdade: {paciente['idade']}
            \nGênero: {paciente['genero']}
            \nPor favor forneça recomendações de tratamento."""
        )
        
        response = llm.invoke(prompt)
        
        return response.content
    else:
        return None

def main():
    st.title("Sistema de Gerenciamento de Pacientes")

    # Sidebar navigation
    menu = ["Home", "Cadastrar Paciente", "Pesquisar Paciente", "Deletar Paciente", "Atualizar Paciente", "Recomendar Tratamento"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Bem-vindo ao Sistema de Gerenciamento de Pacientes")

        st.write("""
            Este sistema foi desenvolvido para ajudar na gestão eficiente das informações dos pacientes e na recomendação personalizada de tratamentos.
            Use as funcionalidades abaixo para interagir com o sistema:
        """)

        st.write("### Funcionalidades Disponíveis:")
        st.write("- **Cadastrar Paciente**: Adicione novos pacientes ao sistema preenchendo suas informações básicas.")
        st.write("- **Pesquisar Paciente**: Busque pacientes no banco de dados usando CPF ou Nome para consultar seus detalhes.")
        st.write("- **Atualizar Paciente**: Modifique as informações de um paciente existente utilizando o CPF.")
        st.write("- **Deletar Paciente**: Remova um paciente do sistema usando seu CPF.")
        st.write("- **Recomendar Tratamento**: Receba recomendações de tratamento baseadas nos sintomas do paciente.")

        st.write("### Instruções de Uso:")
        st.write("""
            1. **Cadastrar Paciente**: Acesse a aba 'Cadastrar Paciente', insira o CPF, Nome, Idade, Gênero e Sintomas do paciente e clique em 'Cadastrar'.
            2. **Pesquisar Paciente**: Vá para a aba 'Pesquisar Paciente', selecione o critério de busca (CPF ou Nome), insira a informação desejada e clique em 'Pesquisar'.
            3. **Atualizar Paciente**: Na aba 'Atualizar Paciente', informe o CPF do paciente cujas informações você deseja modificar, preencha os novos dados e clique em 'Atualizar'.
            4. **Deletar Paciente**: Acesse a aba 'Deletar Paciente', informe o CPF do paciente a ser excluído e clique em 'Deletar'.
            5. **Recomendar Tratamento**: Vá para a aba 'Recomendar Tratamento', insira o CPF do paciente e clique em 'Recomendar Tratamento' para receber sugestões de tratamento baseadas em seus sintomas.
        """)

        st.write("### Contato e Suporte:")
        st.write("Se você tiver alguma dúvida ou precisar de assistência, entre em contato com nossa equipe de suporte através do e-mail [suporte@exemplo.com](mailto:suporte@exemplo.com).")

        st.write("### Novidades e Atualizações:")
        st.write("Fique atento às últimas novidades e melhorias do sistema. Atualizações regulares trazem novas funcionalidades e aprimoramentos para melhor atender suas necessidades.")


    elif choice == "Cadastrar Paciente":
        st.subheader("Cadastrar Paciente")

        with st.form(key='paciente_form'):
            cpf = st.text_input("CPF")
            nome = st.text_input("Nome do Paciente")
            idade = st.number_input("Idade", min_value=0)
            genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
            sintomas = st.text_area("Sintomas")
            submit_button = st.form_submit_button(label="Cadastrar")

        if submit_button:
            if cpf and nome and idade > 0 and genero and sintomas:
                insert_data(cpf, nome, idade, genero, sintomas)
                st.success("Paciente cadastrado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos corretamente.")

    elif choice == "Pesquisar Paciente":
        st.subheader("Pesquisar Paciente")

        search_option = st.selectbox("Buscar por", ["CPF", "Nome"])
        search_query = st.text_input(f"Insira o {search_option}")

        search_button = st.button("Pesquisar")

        if search_button:
            if search_query:
                results = search_pacientes_by_option(search_option, search_query)
                if results:
                    for row in results:
                        st.write(f"ID: {row['id']}")
                        st.write(f"CPF: {row['cpf']}")
                        st.write(f"Nome: {row['nome_paciente']}")
                        st.write(f"Idade: {row['idade']}")
                        st.write(f"Gênero: {row['genero']}")
                        st.write(f"Sintomas: {row['sintomas']}")
                        st.write("---")
                else:
                    st.write(f"Nenhum paciente encontrado com {search_option} igual a {search_query}.")
            else:
                st.error(f"Por favor, insira um {search_option} válido.")

    elif choice == "Recomendar Tratamento":
        st.subheader("Recomendar Tratamento")

        cpf = st.text_input("CPF do Paciente")
        recomendacao_button = st.button("Recomendar Tratamento")

        if recomendacao_button:
            if cpf:
                recomendacao = llm_recomendar_tratamento(cpf)
                if recomendacao:
                    st.write(f"Recomendações de Tratamento para {cpf}:")
                    st.write(recomendacao)
                else:
                    st.write("Paciente não encontrado.")
            else:
                st.error("Por favor, insira um CPF válido.")

    elif choice == "Deletar Paciente":
        st.subheader("Deletar Paciente")

        cpf = st.text_input("CPF do Paciente a ser Deletado")
        delete_button = st.button("Deletar Paciente")

        if delete_button:
            if cpf:
                with db_conn() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM tb_dados_pacientes WHERE cpf = ?", (cpf,))
                    paciente = cursor.fetchone()
                conn.close()

                if paciente:
                    delete_data(cpf)
                    st.success(f"Paciente com CPF {cpf} deletado com sucesso!")
                else:
                    st.write("Paciente não encontrado.")
            else:
                st.error("Por favor, insira um CPF válido.")

    elif choice == "Atualizar Paciente":
        st.subheader("Atualizar Paciente")

        cpf = st.text_input("CPF do Paciente")
        with st.form(key='update_form'):
            nome = st.text_input("Novo Nome do Paciente")
            idade = st.number_input("Nova Idade", min_value=0)
            genero = st.selectbox("Novo Gênero", ["Masculino", "Feminino", "Outro"])
            sintomas = st.text_area("Novos Sintomas")
            update_button = st.form_submit_button(label="Atualizar")

        if update_button:
            if cpf and nome and idade > 0 and genero and sintomas:
                # Check if patient exists
                with db_conn() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM tb_dados_pacientes WHERE cpf = ?", (cpf,))
                    paciente = cursor.fetchone()
                conn.close()

                if paciente:
                    update_data(cpf, nome, idade, genero, sintomas)
                    st.success(f"Dados do paciente com CPF {cpf} atualizados com sucesso!")
                else:
                    st.write("Paciente não encontrado.")
            else:
                st.error("Por favor, preencha todos os campos corretamente.")

if __name__ == "__main__":
    create_table()
    main()
