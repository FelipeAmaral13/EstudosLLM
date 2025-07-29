import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document 

class ClassicRAG:
    def __init__(self, pdf_folder_path: str = "documentos", vector_store_path: str = "dsavectordb"):
        self.pdf_folder_path = pdf_folder_path
        self.vector_store_path = vector_store_path
        self.embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.vector_store = None

    def carrega_pdfs(self) -> List[Document]:
        if not os.path.exists(self.pdf_folder_path):
            raise FileNotFoundError(f"O diretório {self.pdf_folder_path} não existe.")

        print(f"Carregando PDFs de: {self.pdf_folder_path}")
        documents = []

        for filename in os.listdir(self.pdf_folder_path):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.pdf_folder_path, filename)
                try:
                    loader = PyPDFLoader(file_path)
                    loaded_docs = loader.load()
                    for doc in loaded_docs:
                        doc.metadata['source'] = filename
                    documents.extend(loaded_docs)
                    print(f" - {filename} carregado")
                except Exception as e:
                    print(f"   - Erro ao carregar {filename}: {e}")

        if not documents:
            print("Nenhum documento PDF encontrado ou carregado.")
            return []

        print(f"\nDividindo {len(documents)} páginas de documentos em fragmentos...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        split_docs = text_splitter.split_documents(documents)
        print(f"Criados {len(split_docs)} fragmentos de texto.")
        return split_docs

    def criar_vectordb(self, documents: List[Document] = None) -> FAISS:
        if self.vector_store:
            print("Store vetorial já em memória. Reutilizando.")
            return self.vector_store

        if os.path.exists(self.vector_store_path):
            print(f"\nCarregando store vetorial existente de: {self.vector_store_path}")
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings_model,
                allow_dangerous_deserialization=True
            )
            print("Store vetorial carregado com sucesso.")
        else:
            if documents is None:
                print("Nenhum vetor encontrado. Carregando PDFs para criar store vetorial...")
                documents = self.carrega_pdfs()

            if not documents:
                raise ValueError("Nenhum documento disponível para criação do store vetorial.")

            print(f"\nCriando novo store vetorial em: {self.vector_store_path}")
            self.vector_store = FAISS.from_documents(documents, self.embeddings_model)
            self.vector_store.save_local(self.vector_store_path)
            print("Store vetorial criado e salvo com sucesso.")

        return self.vector_store

    def formata_docs_metadados(self, docs: List[Document]) -> str:
        return "\n\n---\n\n".join(
            f"Fonte: {doc.metadata.get('source', 'Desconhecida')} (Página: {doc.metadata.get('page', 'N/D')})\n\n{doc.page_content}"
            for doc in docs
        )