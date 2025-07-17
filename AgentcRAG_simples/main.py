import os
from agentic_RAG import AgenticRAG
from LLM.workflow import agent_app

# --- Configurações ---
PDF_FOLDER_PATH = "documentos"
VECTOR_STORE_PATH = "dsavectordb"

# --- Inicialização ---
print("\n--- Inicializando o Agente de Contratos ---")

if not os.path.exists(PDF_FOLDER_PATH) or not os.listdir(PDF_FOLDER_PATH):
    print(f"\n❌ Erro: a pasta de PDFs '{PDF_FOLDER_PATH}' está ausente ou vazia.")
    print("💡 Por favor, crie a pasta e adicione seus arquivos PDF de contrato.")
    exit()

# Instancia o sistema RAG
rag = AgenticRAG(pdf_folder_path=PDF_FOLDER_PATH, vector_store_path=VECTOR_STORE_PATH)

# Verifica se precisa carregar e dividir os PDFs
docs_for_store = []

if not os.path.exists(VECTOR_STORE_PATH):
    print("\n🔄 Criando novo store vetorial...")
    docs_for_store = rag.carrega_pdfs()

    if not docs_for_store:
        print("\n❌ Saindo: Nenhum documento foi processado para criar o store vetorial.")
        exit()
else:
    print(f"\n✅ Store vetorial encontrado em '{VECTOR_STORE_PATH}'. Pulando carregamento/divisão de PDFs.")
    print("ℹ️ Se os contratos foram alterados, exclua a pasta do store vetorial e execute novamente.")

# Inicializa o FAISS
try:
    vector_store = rag.criar_vectordb(docs_for_store)
except ValueError as e:
    print(f"\n❌ Erro ao inicializar o store vetorial: {e}")
    exit()

print("\n✅ Sistema pronto. Agente de contratos inicializado com sucesso.")

# --- Loop interativo ---
print("\n--- Executando Agente de Contratos ---")

while True:
    user_query = input("\nDigite sua pergunta sobre os contratos (ou digite 'sair' para encerrar): \n> ")

    if user_query.lower() == 'sair':
        break

    if not user_query.strip():
        continue

    print("\n⏳ Processando consulta...")
    inputs = {"question": user_query.strip()}
    final_state = agent_app.invoke(inputs)

    print("\n✅ --- Resposta Final ---")
    print(final_state.get("answer", "⚠️ Nenhuma resposta gerada."))
    
    print("\n📚 --- Fontes dos Documentos Recuperados (para contexto) ---")
    if final_state.get("documents"):
        sources = {doc.metadata.get('source', 'Desconhecida') for doc in final_state["documents"]}
        print("📄 " + ", ".join(sources))
    else:
        print("⚠️ Nenhum documento foi recuperado para esta consulta.")

    print("-" * 60)

print("\n👋 Agente finalizado. Até a próxima.")
