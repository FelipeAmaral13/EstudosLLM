from typing import List, Optional
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.docstore.document import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import RetrievalQA


class RAGSystem:
    def __init__(
        self,
        path_file: str,
        model_name: str = "meta-llama-3.1-8b-instruct@Q4_k_M",
        api_base: str = "http://192.168.0.27:1234/v1",
        api_key: str = "lm-studio",
        k_retrieval: int = 2
    ):
        self.path_file = path_file
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key
        self.k_retrieval = k_retrieval

        # Embeddings compartilhado por chunks e FAISS
        self.embedder = HuggingFaceEmbeddings()

        # Inicializa os atributos para reuso posterior
        self.retriever: Optional[VectorStoreRetriever] = None
        self.qa_chain: Optional[RetrievalQA] = None


    def load_documents(self) -> List[Document]:
        """Carrega documentos PDF usando PDFPlumber."""
        loader = PDFPlumberLoader(self.path_file)
        return loader.load()


    def chunk_documents(self, docs: List[Document]) -> List[Document]:
        """Aplica o SemanticChunker aos documentos."""
        splitter = SemanticChunker(self.embedder)
        return splitter.split_documents(docs)


    def build_vectorstore(self, docs: List[Document]) -> VectorStoreRetriever:
        """Cria e retorna um retriever FAISS."""
        vectordb = FAISS.from_documents(docs, self.embedder)
        return vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.k_retrieval}
        )


    def build_llm_chain(self) -> StuffDocumentsChain:
        """Cria o LLMChain e StuffDocumentsChain com o modelo configurado."""
        llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_base=self.api_base,
            openai_api_key=self.api_key,
            temperature=0.0,
            max_tokens=1024
        )

        system_prompt = (
            "1. Use os seguintes pedaços de contexto para responder à pergunta no final, sempre em Português do Brasil.\n"
            "2. Se você não sabe a resposta, apenas diga 'Eu não sei', mas não invente uma resposta.\n"
            "3. Mantenha a resposta concisa e limitada a 3 ou 4 parágrafos.\n"
            "Contexto: {context}\n"
            "Pergunta: {question}\n"
            "Resposta:"
        )
        prompt_template = PromptTemplate.from_template(system_prompt)

        llm_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

        # Template para representar cada documento
        document_prompt = PromptTemplate(
            input_variables=["page_content", "source"],
            template="Contexto:\n{page_content}\nFonte: {source}"
        )

        return StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="context",
            document_prompt=document_prompt,
            verbose=True
        )


    def build_pipeline(self):
        """Constrói toda a cadeia do RAG: retriever + QA Chain."""
        docs = self.load_documents()
        chunks = self.chunk_documents(docs)
        self.retriever = self.build_vectorstore(chunks)
        documents_chain = self.build_llm_chain()

        self.qa_chain = RetrievalQA(
            combine_documents_chain=documents_chain,
            retriever=self.retriever,
            verbose=True,
            return_source_documents=True
        )


    def run_query(self, question: str):
        """Executa a pergunta usando a cadeia completa."""
        if not self.qa_chain:
            raise RuntimeError("O pipeline não foi construído. Execute `build_pipeline()` primeiro.")
        return self.qa_chain.run(question)
