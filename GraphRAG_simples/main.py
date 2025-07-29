from classic_rag import ClassicRAG
from graph_definition import build_graph

if __name__ == "__main__":
    rag = ClassicRAG()
    query = "Qual o valor da multa do documento?"

    graph = build_graph()
    state = {
        "query": query,
        "rag_instance": rag
    }

    resultado = graph.invoke(state)
    print("\n📣 Resposta Final:\n")
    print(resultado["resposta"])
