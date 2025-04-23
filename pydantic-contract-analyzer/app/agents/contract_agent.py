from pydantic_ai import Agent, RunContext
from app.models.contract_models import ContractInput, ContractAnalysis
from app.tools.vector_search import query_normas

with open("app/prompts/contract_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

contract_agent = Agent(
    model='groq:llama-3.3-70b-versatile',
    deps_type=ContractInput,
    output_type=ContractAnalysis,
    system_prompt=SYSTEM_PROMPT
)

@contract_agent.tool()
async def retrieve_normas(ctx: RunContext[ContractInput], contract_text: str) -> list[str]:
    return query_normas(contract_text)

# Função de execução isolada (usada em `main.py`)
async def analyze_contract_text(contract: str):
    deps = ContractInput(contract_text=contract)
    result = await contract_agent.run(contract, deps=deps)
    return result.output
