# Classe para IA Generativa Multimodal com Agentic RAG e LangGraph Para Análise Contábil

import os
import re
import base64
import logging
from typing import TypedDict, Optional, Dict, Any
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langgraph.graph import StateGraph, END


class MultimodalGraphState(TypedDict):
    """Define o tipo de dicionário para o estado multimodal no grafo"""
    query: str | None
    image_bytes: bytes | None
    image_mime_type: str | None
    rag_context: str | None
    final_answer: str | None


class MultimodalRAGAnalyzer:
    """
    Classe para análise multimodal de notas fiscais usando RAG e LangGraph
    """
    
    def __init__(self, vectorstore_path: str = "faiss_index_contabilidade", 
                 log_level: int = logging.INFO):
        """
        Inicializa o analisador multimodal
        
        Args:
            vectorstore_path: Caminho para o índice FAISS
            log_level: Nível de logging
        """
        # Configuração de logging
        self.logger = self._setup_logging(log_level)
        
        # Configurações
        self.vectorstore_path = vectorstore_path
        
        # Inicializa componentes
        self.llm_vision = None
        self.retriever = None
        self.multimodal_app = None
        
        self.logger.info("MultimodalRAGAnalyzer inicializado com sucesso")
    
    def _setup_logging(self, log_level: int) -> logging.Logger:
        """Configura o sistema de logging"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(log_level)
        
        # Remove handlers existentes para evitar duplicação
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Configura handler do console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Formato das mensagens de log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        return logger

    def cria_vectordb(self, pdf_dir: str) -> bool:
        """
        Cria o índice vetorial FAISS a partir de documentos PDF no diretório especificado.
        """
        self.logger.info(f"Carregando PDFs do diretório: {pdf_dir}")
        if not os.path.exists(pdf_dir) or not os.listdir(pdf_dir):
            self.logger.warning(f"O diretório '{pdf_dir}' está vazio ou não existe.")
            return False

        try:
            pdf_loader = PyPDFDirectoryLoader(pdf_dir, recursive=True)
            documents = pdf_loader.load()
            if not documents:
                self.logger.warning(f"Nenhum documento carregado de '{pdf_dir}'")
                return False
            self.logger.info(f"Carregados {len(documents)} páginas/documentos PDF.")
        except Exception as e:
            self.logger.error(f"Erro ao carregar PDFs: {e}")
            return False

        self.logger.info("Dividindo documentos em chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs_split = splitter.split_documents(documents)
        self.logger.info(f"{len(docs_split)} chunks gerados.")

        self.logger.info("Inicializando modelo de embedding (FastEmbed)...")
        embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

        self.logger.info("Criando índice vetorial FAISS...")
        try:
            if not docs_split:
                self.logger.warning("Nenhum documento válido para gerar embeddings. Criando índice vazio.")
                dummy_embeddings = embedding_model.embed_documents(["dummy text"])
                dimension = len(dummy_embeddings[0])
                index = faiss.IndexFlatL2(dimension)
                vector_store = FAISS(embedding_function=embedding_model.embed_query,
                                     index=index,
                                     docstore={},
                                     index_to_docstore_id={})
            else:
                vector_store = FAISS.from_documents(docs_split, embedding_model)

            vector_store.save_local(self.vectorstore_path)
            self.logger.info(f"Índice FAISS salvo com sucesso em: {self.vectorstore_path}")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao criar ou salvar o índice FAISS: {e}")
            return False
    
    def load_llm_vision(self) -> ChatOpenAI:
        """Carrega e retorna o modelo LLM Multimodal"""
        if self.llm_vision is not None:
            return self.llm_vision
            
        self.logger.info("Carregando LLM Multimodal...")
        try:
            self.llm_vision = ChatOpenAI(model_name = "google/gemma-3-12b",
                openai_api_base = "http://172.30.64.1:1234/v1",
                openai_api_key = "lm-studio",
                temperature = 0.1,
                max_tokens = 1024)

            self.logger.info("LLM Multimodal carregado com sucesso")
            return self.llm_vision
        
        except Exception as e:
            self.logger.error(f"Erro ao carregar LLM multimodal: {e}")
            raise
    
    def load_rag_retriever(self):
        """Carrega e retorna o retriever do RAG"""
        if self.retriever is not None:
            return self.retriever
            
        self.logger.info("Carregando Retriever RAG Contabilidade...")
        
        # Verifica se o índice FAISS existe
        if not os.path.exists(self.vectorstore_path) or not os.listdir(self.vectorstore_path):
            self.logger.warning(
                f"Índice RAG '{self.vectorstore_path}' não encontrado. "
                "A análise usará apenas a imagem e a pergunta."
            )
            return None
        
        try:
            # Inicializa o modelo de embedding
            embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
            
            # Carrega o índice FAISS
            vector_store = FAISS.load_local(
                self.vectorstore_path, 
                embedding_model, 
                allow_dangerous_deserialization=True
            )
            
            # Configura o retriever
            self.retriever = vector_store.as_retriever(search_kwargs={'k': 3})
            
            self.logger.info("Retriever RAG Contabilidade carregado com sucesso")
            return self.retriever
        
        except Exception as e:
            self.logger.error(f"Erro ao carregar Retriever RAG Contabilidade: {e}")
            return None
    
    def _retrieve_rag_node(self, state: MultimodalGraphState) -> Dict[str, Any]:
        """Nó do grafo para realizar a recuperação RAG"""
        self.logger.info("--- Nó: Recuperação RAG Contabilidade ---")
        
        # Obtém o retriever
        local_retriever = self.load_rag_retriever()
        query = state.get("query")
        
        # Valor padrão para o contexto RAG
        rag_context = "Nenhum contexto RAG relevante encontrado ou RAG não disponível."
        
        if local_retriever and query:
            try:
                # Invoca o retriever com a consulta
                results = local_retriever.invoke(query)
                
                # Concatena o conteúdo dos documentos
                context = "\n\n".join([doc.page_content for doc in results])
                
                if context:
                    rag_context = context
                    self.logger.info(f"Contexto RAG encontrado ({len(context)} chars)")
                else:
                    self.logger.info("Nenhum contexto RAG encontrado para a query")
            
            except Exception as e:
                self.logger.error(f"Erro no nó RAG: {e}")
                rag_context = f"Erro ao buscar nos documentos: {e}"
        else:
            self.logger.info("Retriever não disponível ou query vazia. Pulando busca RAG")
        
        return {"rag_context": rag_context}
    
    def _analyze_invoice_node(self, state: MultimodalGraphState) -> Dict[str, Any]:
        """Nó do grafo para análise multimodal de notas fiscais"""
        self.logger.info("--- Nó: Análise Multimodal da Nota Fiscal ---")
        
        # Extrai os atributos do estado
        query = state.get("query")
        image_bytes = state.get("image_bytes")
        mime_type = state.get("image_mime_type")
        rag_context = state.get("rag_context", "Nenhum contexto adicional fornecido.")
        
        # Validações
        if not query:
            return {"final_answer": "Erro: Nenhuma pergunta foi fornecida."}
        if not image_bytes or not mime_type:
            return {"final_answer": "Erro: Nenhuma imagem válida foi fornecida."}
        
        try:
            # Carrega o LLM
            llm_vision = self.load_llm_vision()
            
            # Encode da imagem
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Constrói o prompt
            # message_content = [
            #     {
            #         "type": "text",
            #         "text": f"""Você é um assistente de contabilidade. Sua tarefa é analisar a imagem da nota fiscal anexa e responder à pergunta do usuário. Utilize também o contexto de regras de contabilidade fornecido abaixo, se for relevante para a pergunta.

            #         Contexto de Regras de Contabilidade (Manuais RAG):
            #         ---
            #         {rag_context}
            #         ---

            #         Pergunta do Usuário:
            #         {query}

            #         Responda de forma clara e objetiva, baseando-se na análise da imagem e no contexto fornecido. Se a pergunta for sobre anomalias, procure por inconsistências comuns (datas, valores, cálculos, informações obrigatórias ausentes)."""
            #     },
            #     {
            #         "type": "image_url",
            #         "image_url": f"data:{mime_type};base64,{image_base64}"
            #     }
            # ]
            
            # Cria o objeto de mensagem
            message = HumanMessage(content=[
                {
                    "type": "text",
                    "text": f"""Você é um assistente de contabilidade. Sua tarefa é analisar a imagem da nota fiscal anexa e responder à pergunta do usuário. Utilize também o contexto de regras de contabilidade fornecido abaixo, se for relevante para a pergunta.
                    Contexto de Regras de Contabilidade (Manuais RAG):
                    ---
                    {rag_context}
                    ---

                    Pergunta do Usuário:
                    {query}
                    Responda de forma clara e objetiva, baseando-se na análise da imagem e no contexto fornecido. Se a pergunta for sobre anomalias, procure por inconsistências comuns (datas, valores, cálculos, informações obrigatórias ausentes).
                    """

                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    }
                }
            ])

            
            self.logger.info(f"Enviando para análise no modelo LLM multimodal "
                           f"(imagem: {mime_type}, {len(image_bytes)} bytes)")
            
            # Envia para análise
            response = llm_vision.invoke([message])
            final_answer = response.content
            
            self.logger.info("Análise multimodal concluída com sucesso")
            return {"final_answer": final_answer}
        
        except Exception as e:
            self.logger.error(f"Erro no nó de análise multimodal: {e}")
            if "image" in str(e).lower():
                return {"final_answer": f"Erro ao processar a imagem: {e}"}
            else:
                return {"final_answer": f"Erro durante a análise multimodal: {e}"}
    
    def compile_multimodal_graph(self):
        """Compila o grafo multimodal"""
        if self.multimodal_app is not None:
            return self.multimodal_app
            
        self.logger.info("Compilando o grafo multimodal...")
        
        # Cria o construtor de grafo
        graph_builder = StateGraph(MultimodalGraphState)
        
        # Adiciona os nós
        graph_builder.add_node("retrieve_rag_node", self._retrieve_rag_node)
        graph_builder.add_node("analyze_invoice_node", self._analyze_invoice_node)
        
        # Define o fluxo do grafo
        graph_builder.set_entry_point("retrieve_rag_node")
        graph_builder.add_edge("retrieve_rag_node", "analyze_invoice_node")
        graph_builder.add_edge("analyze_invoice_node", END)
        
        try:
            # Compila o grafo
            self.multimodal_app = graph_builder.compile()
            self.logger.info("Grafo multimodal compilado com sucesso!")
            return self.multimodal_app
        
        except Exception as e:
            self.logger.error(f"Erro ao compilar o grafo multimodal: {e}")
            raise
    
    def clean_llm_output(self, text: str) -> str:
        """Limpa a saída do LLM removendo caracteres indesejados"""
        if not isinstance(text, str):
            return text
        
        # Remove caracteres especiais
        text = text.replace('\u02ca', "'")
        text = text.replace('ˊ', "'")
        text = text.replace('\xa0', ' ')
        
        # Remove caracteres invisíveis
        text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
        
        # Corrige formatação de valores monetários
        text = re.sub(r'(R\$)\s*(\d)', r'\1 \2', text)
        text = re.sub(r'\s+(,)', r'\1', text)
        
        return text.strip()
    
    def analyze_invoice(self, query: str, image_bytes: bytes, 
                       image_mime_type: str) -> Dict[str, Any]:
        """
        Analisa uma nota fiscal com base na query e imagem fornecidas
        
        Args:
            query: Pergunta sobre a nota fiscal
            image_bytes: Bytes da imagem da nota fiscal
            image_mime_type: Tipo MIME da imagem
            
        Returns:
            Dicionário com o resultado da análise
        """
        self.logger.info("Iniciando análise de nota fiscal")
        
        try:
            # Compila o grafo se necessário
            multimodal_app = self.compile_multimodal_graph()
            
            # Prepara os inputs
            inputs = {
                "query": query,
                "image_bytes": image_bytes,
                "image_mime_type": image_mime_type
            }
            
            self.logger.info("Executando análise multimodal...")
            
            # Executa o grafo
            final_state = multimodal_app.invoke(inputs)
            
            # Extrai e limpa a resposta
            final_answer_raw = final_state.get("final_answer", 
                                               "Não foi possível obter uma resposta.")
            final_answer_cleaned = self.clean_llm_output(final_answer_raw)
            
            result = {
                "success": True,
                "final_answer": final_answer_cleaned,
                "final_answer_raw": final_answer_raw,
                "rag_context": final_state.get("rag_context", 
                                               "Nenhum contexto RAG utilizado."),
                "query": query,
                "image_size": len(image_bytes),
                "image_type": image_mime_type
            }
            
            self.logger.info("Análise de nota fiscal concluída com sucesso")
            return result
        
        except Exception as e:
            self.logger.error(f"Erro durante análise da nota fiscal: {e}")
            return {
                "success": False,
                "error": str(e),
                "final_answer": f"Erro durante a análise: {e}",
                "query": query,
                "image_size": len(image_bytes) if image_bytes else 0,
                "image_type": image_mime_type
            }


# # Exemplo de uso da classe
# if __name__ == "__main__":
#     # Inicializa o analisador
#     analyzer = MultimodalRAGAnalyzer()
#     success = analyzer.cria_vectordb(pdf_dir="documentos_pdfs")
    
#     # Exemplo de uso (necessário ter uma imagem em bytes)
#     with open("recibo.png", "rb") as f:
#         image_bytes = f.read()
    
#     result = analyzer.analyze_invoice(
#         query="Me informe apenas o valor total do recibo",
#         image_bytes=image_bytes,
#         image_mime_type="image/png"
#     )
    
#     print("Resultado:", result["final_answer"])