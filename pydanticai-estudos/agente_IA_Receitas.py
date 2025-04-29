import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Optional
import argparse

load_dotenv()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Agente de IA simples para criação de receitas")
    parser.add_argument("--receita", type=str, help="Qual receita a ser criada")
    return parser.parse_args()


class Ingrediente(BaseModel):
    nome: str
    quantidade: str
    substituto: Optional[str] = Field(None, description="Substituto comum para restrições alimentares")

class PassoReceita(BaseModel):
    numero: int
    instrucao: str
    tempo: Optional[str] = Field(None, description="Tempo estimado para este passo")

class Receita(BaseModel):
    nome: str
    ingredientes: List[Ingrediente]
    passos: List[PassoReceita]
    tempo_total: str
    porcoes: int
    dicas: Optional[List[str]] = None

# Criando o agente
agent = Agent('groq:meta-llama/llama-4-scout-17b-16e-instruct', 
             deps_type=Ingrediente, 
             system_prompt="Seja conciso nas respostas.")

async def chef_ai(nome_receita: str):
 
    result = await agent.run(
        f"Por favor, forneça uma receita detalhada para: {nome_receita}",
        deps=Receita(
            nome=nome_receita,
            ingredientes=[],
            passos=[],
            tempo_total="",
            porcoes=4
        )
    )
    
    print("Resposta:", result.output)

if __name__ == "__main__":
    args = parse_arguments()

    asyncio.run(chef_ai(args.receita))