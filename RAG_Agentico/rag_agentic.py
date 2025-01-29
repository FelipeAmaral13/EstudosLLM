from typing_extensions import List
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, END, MessagesState, StateGraph, MessageGraph

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

loader = PyPDFDirectoryLoader("RAG_Agentico\\documents")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=50
)

doc_splits = text_splitter.split_documents(pages)

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_invoice_info",  # Nome mais específico da ferramenta
    "Busque e analise informações específicas de contratos."  # Descrição mais detalhada
)


class State(MessagesState):
    context: List[Document]

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Recuperar informações relacionadas a uma consulta."""
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


def query_or_respond(state: State) -> dict:
    """Gere a ferramenta para recuperar ou responder."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tools = ToolNode([retrieve])


def generate(state: MessagesState):
    """Gerar resposta"""
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "Você é um assistente especializado em análise de contratos. "
        "Use o contexto fornecido para analisar cláusulas contratuais, "
        "identificar termos importantes, obrigações, direitos, prazos e condições. "
        "Se encontrar termos legais complexos, forneça explicações claras. "
        "Se não encontrar a informação específica, indique claramente. "
        "Mantenha as respostas objetivas e precisas.\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    context = []
    for tool_message in tool_messages:
        context.extend(tool_message.artifact)
    return {"messages": [response], "context": context}

graph_builder = StateGraph(MessagesState)

graph_builder.add_node(query_or_respond)
graph_builder.add_node(tools)
graph_builder.add_node(generate)

graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

graph = graph_builder.compile()


png_graph = graph.get_graph().draw_mermaid_png()
with open("graph_RAG_Agentic_2.png", "wb") as f:
    f.write(png_graph)


input_message = "Existem cláusulas de confidencialidade em algum contrato, se sim, me informe o arquivo?"

for step in graph.stream(
    {"messages": [{"role": "user", "content": input_message}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()