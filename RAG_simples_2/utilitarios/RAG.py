import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class RAGModel:
    def __init__(self):
        model_name = "BAAI/bge-base-en"
        self.model = HuggingFaceEmbeddings(model_name = model_name)
        self.embedding = self._get_embedding_model()
        self.documents = []
        self.vector_store = None
    
    def _get_embedding_model(self):
        return self.model
    
    def carrega_documentos(self, documents_path):
        for filename in os.listdir(documents_path):
            if filename.endswith(".pdf"):
                loader = PyMuPDFLoader(os.path.join(documents_path, filename))
                loaded_docs = loader.load()
                self.documents.extend(loaded_docs)

    def cria_vectordb(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        docs_split = splitter.split_documents(self.documents)
        self.vector_store = FAISS.from_documents(docs_split, self.embedding)

    def retrieve(self, query, k = 5):
        if not self.vector_store:
            raise ValueError("Vector store não está inicializada.")
        docs = self.vector_store.similarity_search(query, k = k)
        return docs