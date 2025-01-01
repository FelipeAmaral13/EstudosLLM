import streamlit as st
from question_sql import Question2SQL

# Inicializar o sistema
question_to_sql = Question2SQL()

# Configurar a interface do Streamlit
st.title("Consulta Jurídica usando linguagem natural no SQL")
st.write("Digite sua pergunta jurídica e obtenha os resultados diretamente do banco de dados.")

# Inicializar memória para histórico de interações e thread ID
if "history" not in st.session_state:
    st.session_state.history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Input de pergunta
user_input = st.chat_input("Faça sua pergunta jurídica...")

# Processar a entrada do usuário
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    # Configurar e processar a pergunta
    question_to_sql.set_question(user_input)

    # Configurar thread_id, se necessário
    if not st.session_state.thread_id:
        st.session_state.thread_id = question_to_sql.thread_id

    state = question_to_sql.process_graph()

    # Extrair e executar a consulta SQL
    clean_sql = question_to_sql.extract_sql(state.values['sql'])
    results = question_to_sql.execute_query(clean_sql)

    response = "\n".join(
        [f"- {', '.join([f'{key}: {value}' for key, value in result.items()])}" for result in results]
    ) if results else "Nenhum resultado encontrado ou houve um erro ao processar sua consulta."

    st.session_state.history.append({"role": "assistant", "content": response})

# Exibir histórico de interações
for message in st.session_state.history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])
