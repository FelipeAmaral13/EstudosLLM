from langchain_openai import ChatOpenAI


model_name = "meta-llama-3.1-8b-instruct@Q4_K_M"
api_key = "lm-studio"
api_base = "http://172.30.64.1:1234/v1"

llm = ChatOpenAI(
    model_name=model_name,
    openai_api_base=api_base,
    openai_api_key=api_key,
    temperature=0.0,
    max_tokens=1024
)