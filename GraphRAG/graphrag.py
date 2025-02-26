import numpy as np
import spacy
import faiss
import networkx as nx
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from collections import defaultdict
from collections import deque

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


load_dotenv()

class GraphRAG:
    def __init__(self):
        self.modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
        self.relacoes = []
        self.id_to_chunk = {}
        self.grafo = nx.Graph()

        self.nlp = spacy.load("pt_core_news_sm")

    def dividir_documento(self, documento: str, tamanho: int = 80, sobreposicao: int = 10) -> List[str]:
        tamanho = int(tamanho)  # Garante que o valor seja um número inteiro
        sobreposicao = int(sobreposicao)  # Garante que o valor seja um número inteiro

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=tamanho,
            chunk_overlap=sobreposicao,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(documento)


    def extrair_entidades(self, chunk: str) -> List[str]:
        doc = self.nlp(chunk)
        return [ent.text for ent in doc.ents]

    def extrair_relacoes(self, chunk: str) -> List[Tuple[str, str, str]]:
        entidades = self.extrair_entidades(chunk)
        if len(entidades) < 2:
            return []

        relacoes = [(entidades[i], "RELACIONADO_A", entidades[i+1]) for i in range(len(entidades) - 1)]

        for ent1, _, ent2 in relacoes:
            # Adiciona os nós antes de criar conexões
            if ent1 not in self.grafo:
                self.grafo.add_node(ent1)
            if ent2 not in self.grafo:
                self.grafo.add_node(ent2)

            # Adiciona a relação como uma aresta no grafo
            if not self.grafo.has_edge(ent1, ent2):
                self.grafo.add_edge(ent1, ent2, tipo="RELACIONADO_A")

        return relacoes


    def encontrar_caminhos(self, inicio: str, fim: str, max_depth: int = 3) -> List[List[str]]:
        if inicio not in self.grafo or fim not in self.grafo:
            return []

        caminhos = []
        for path in nx.all_simple_paths(self.grafo, source=inicio, target=fim, cutoff=max_depth):
            caminhos.append(path)

        return caminhos

    def construir_base_conhecimento(self, documento: str):
        print("Construindo base de conhecimento...")
        
        self.chunks = self.dividir_documento(documento)
        embeddings = self.modelo.encode(self.chunks)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.id_to_chunk = {i: chunk for i, chunk in enumerate(self.chunks)}
        
        for chunk in self.chunks:
            self.relacoes.extend(self.extrair_relacoes(chunk))
        
        print(f"Processados {len(self.chunks)} chunks e {len(self.relacoes)} relações")

    def buscar_chunks_similares(self, pergunta: str, top_k: int = 3) -> List[str]:
        emb_pergunta = self.modelo.encode([pergunta])
        D, I = self.index.search(np.array(emb_pergunta, dtype=np.float32), top_k)
        return [self.id_to_chunk[i] for i in I[0] if i != -1]

    def buscar_relacoes_relevantes(self, pergunta: str) -> List[Dict]:
        palavras = pergunta.lower().split()
        resultados = []
        entidades_pergunta = set(self.extrair_entidades(pergunta))

        # Busca direta
        for ent1, rel, ent2 in self.relacoes:
            if any(p in ent1.lower() or p in ent2.lower() for p in palavras):
                resultados.append({
                    "entidade1": ent1,
                    "relacao": rel,
                    "entidade2": ent2,
                    "tipo": "direto"
                })

        # Busca por caminhos
        chaves_grafo = list(self.grafo.nodes)  # Corrigido: Obtém os nós corretamente
        for ent1 in entidades_pergunta:
            for ent2 in chaves_grafo:
                if ent2 not in entidades_pergunta:
                    caminhos = self.encontrar_caminhos(ent1, ent2)
                    for caminho in caminhos:
                        if len(caminho) > 1:
                            resultados.append({
                                "entidade1": caminho[0],
                                "relacao": "CONECTADO_A",
                                "entidade2": caminho[-1],
                                "tipo": "caminho",
                                "caminho": " -> ".join(caminho)
                            })
        return resultados[:20]

    
    def gerar_resposta_llm(self, pergunta: str, info_vetorial: str, info_grafo: List[Dict]) -> str:
        relacoes_diretas = [r for r in info_grafo if r["tipo"] == "direto"]
        caminhos = [r for r in info_grafo if r["tipo"] == "caminho"]

        contexto_grafo = "Relações diretas encontradas:\n"
        for r in relacoes_diretas:
            contexto_grafo += f"- {r['entidade1']} --[{r['relacao']}]--> {r['entidade2']}\n"

        if caminhos:
            contexto_grafo += "\nCaminhos semânticos relevantes:\n"
            for r in caminhos:
                contexto_grafo += f"- {r['caminho']} (Confiabilidade: {len(r['caminho'])})\n"

        prompt = f"""
        Você é um assistente especialista em integração de conhecimento vetorial e conexões semânticas.

        1️⃣ TRECHOS DE TEXTO RELEVANTES:
        {info_vetorial}

        2️⃣ ESTRUTURA DE CONHECIMENTO (GRAFO SEMÂNTICO):
        {contexto_grafo}

        Com base nas informações acima, responda à pergunta "{pergunta}" de forma precisa e estruturada.
        """

        chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        try:
            response = chat_model.invoke([
                SystemMessage(content="Você é um assistente especialista que integra informações textuais e estruturais."),
                HumanMessage(content=prompt)
            ])
            return response.content.strip()
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"

