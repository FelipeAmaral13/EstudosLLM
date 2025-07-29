from typing import TypedDict, Sequence, Optional
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from classic_rag import ClassicRAG

class AgentState(TypedDict, total=False):
    rag_instance: ClassicRAG
    query: str
    retriever: VectorStoreRetriever
    docs: Sequence[Document]
    context: str
    resposta: str
