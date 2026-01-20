import os
from groq import Groq
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada.")
    return Groq(api_key=api_key)

def get_embeddings():
    return HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def setup_vector_store():
    embeddings = get_embeddings()
    loader = DirectoryLoader("dados/", glob="**/*.txt")
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documentos)
    
    return FAISS.from_documents(docs, embeddings)


class AuditAgent:
    def __init__(self):
        self.client = get_groq_client()
        self.vector_store = setup_vector_store()

    def _retrieve_context(self, query: str):
        docs = self.vector_store.similarity_search(query, k=4)
        return "\n\n".join([doc.page_content for doc in docs])

    def ask(self, question: str):
        context = self._retrieve_context(question)
        
        # Prompt corrigido para uso direto com a API
        system_prompt = f"""Você é um assistente de auditoria inteligente e rigoroso.
            Sua função é verificar conformidade baseada estritamente no CONTEXTO fornecido.

            CONTEXTO:
            {context}

            REGRAS:
            1. Resumo inicial: "Em conformidade" ou "Não está em conformidade".
            2. Use '*' para listas e '**' para valores financeiros.
            3. Responda em PORTUGUÊS. Garanta espaços entre as palavras.
        """

        # Chamada direta da lib groq
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0,
        )

        return chat_completion.choices[0].message.content


if __name__ == "__main__":
    agent = AuditAgent()
    resposta = agent.ask("Analise o reembolso de transporte de R$ 450 do consultor X.")
    print(resposta)