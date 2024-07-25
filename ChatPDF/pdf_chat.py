import os
import tempfile
import langchain
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.chains import LLMChain, SequentialChain

langchain.debug = True

load_dotenv(dotenv_path=".config")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def process_pdf(file_path):
    loader = PyPDFLoader(file_path=file_path)
    docs = loader.load_and_split()

    if not docs or not docs[0].page_content:
        raise ValueError("Documento vazio ou não encontrado")
    
    task_description = " ".join([doc.page_content for doc in docs])

    prompt_curso = ChatPromptTemplate(
        messages=[
            SystemMessage(content=(
                """Você tera acesso a um pdf de certificado de um curso.\n"
                "Estruture a saida, com os dados estraídos, em formato JSON:"
                {
                    "Instituicao": "",
                    "Nome_aluno": "",
                    "Curso": "",
                    "Carga_horario": ""
                }"""
            )),
            HumanMessagePromptTemplate.from_template("{certificado_info}")
        ]
    )

    chain_curso = LLMChain(
        llm=llm,
        prompt=prompt_curso,
        output_key="result"
    )

    chain = SequentialChain(
        chains=[chain_curso],
        input_variables=["certificado_info"],
        output_variables=["result"]
    )

    resposta = chain.invoke(
        {
            "certificado_info": f"Dado o texto: {task_description}. Qual a instituição de ensino do curso? Qual o nome do aluno? Qual o curso feito? Qual a carga horaria?"
        }
    )

    return resposta["result"]


st.title("Extrator de informações de Certificados PDF")

uploaded_files = st.file_uploader("Faça upload de um ou mais certificados em PDF", type=["pdf"], accept_multiple_files=True)

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

        try:
            course_result = process_pdf(uploaded_file.name)
            
            st.subheader(f"Curso Identificado em '{uploaded_file.name}':")
            st.json(course_result)

            os.remove(uploaded_file.name)
            
        except Exception as e:
            st.error(f"Erro ao processar o PDF '{uploaded_file.name}': {e}")
