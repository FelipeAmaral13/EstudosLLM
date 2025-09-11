from groq import Groq
from dotenv import load_dotenv
load_dotenv()

class MetaAgent:

    def __init__(self):
        self.client = Groq()

    def gera_resposta_final(self, summary, reasoning, query):

        messages = [
            {"role": "system", "content": "Você gera respostas claras e detalhadas consolidando informações."},
            {"role": "user", "content": f"Pergunta original: {query}\n\nResumo: {summary}\n\nRaciocínio lógico: {reasoning}\n\nForneça a resposta consolidada e detalhada:"}
        ]

        completion = self.client.chat.completions.create(model = "qwen/qwen3-32b",
                                                         messages = messages,
                                                         temperature = 0.7,
                                                         max_tokens = 1024,
                                                         stream = True)

        resposta_final = ""

        for chunk in completion:
            chunk_content = chunk.choices[0].delta.content or ""
            print(chunk_content, end="", flush = True)
            resposta_final += chunk_content

        return resposta_final

class ReasoningAgent:
    def __init__(self):
        self.client = Groq()

    def gera_raciocinio(self, summary, query):
        messages = [
            {"role": "system", "content": "Você é especialista em raciocínio lógico sobre textos."},
            {"role": "user", "content": f"Com base no resumo: {summary}\n\nFaça uma análise crítica para responder à pergunta: {query}"}
        ]

        completion = self.client.chat.completions.create(model = "llama-3.3-70b-versatile",
                                                         messages = messages,
                                                         temperature = 0.7,
                                                         max_tokens = 1024)

        return completion.choices[0].message.content.strip()

class DocumentAgent:
    def __init__(self):
        self.client = Groq()

    def sumariza_documentos(self, documents, query):
        context = "\n\n".join([doc.page_content for doc in documents])

        messages = [
            {"role": "system", "content": "Você resume documentos com precisão."},
            {"role": "user", "content": f"Documentos: {context}\n\nResponda brevemente à pergunta: {query}"}
        ]

        completion = self.client.chat.completions.create(model = "llama-3.3-70b-versatile",
                                                         messages = messages,
                                                         temperature = 0.7,
                                                         max_tokens = 1024)

        return completion.choices[0].message.content.strip()
