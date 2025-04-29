import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent
from typing import List, Optional
import argparse
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Agente de IA simples para recomendações de livros")
    parser.add_argument("--livro", type=str, help="Recomendação de livros")
    return parser.parse_args()

class Livro(BaseModel):
    titulo: str
    autor: str
    ano: int
    genero: str
    num_pagina: int

class Recomendacao(BaseModel):
    principal: Livro
    similares: List[Livro]
    motivo: str

agent = Agent('groq:meta-llama/llama-4-scout-17b-16e-instruct',
              deps_type=Recomendacao,
              system_prompt="Você é um especialista em livros que faz recomendações personalizadas. Forneça detalhes sobre os livros e explique por que são boas recomendações."
            )

async def main(livro: List[str]):
    """Obtém recomendações de livros baseado nas preferências do usuário"""

    try:
        try:
            logger.info("Tentando abordagem estruturada...")
            prompt = (
                f"Para alguém que gosta de {', '.join(livro)}, recomende:\n"
                "1. Três livros similares (com título, autor, ano, gênero e numero de paginas)\n"
                "2. Um motivo detalhado da recomendação\n\n"
            )

            result = await agent.run(prompt, deps=Recomendacao(
                principal=Livro(titulo="", autor="", ano=0, genero="", num_pagina=0),
                similares=[Livro(titulo="", autor="", ano=0, genero="", num_pagina=0) for _ in range(3)],
                motivo=""
            ))
            
            logger.info("Resposta recebida (estruturada):")
            logger.info(result.output)

        except Exception as e:
            logger.warning(f"Falha na abordagem estruturada: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recomendador de livros")
    parser.add_argument("--livro", nargs="+", help="Preferências para recomendação (gêneros, atores, etc.)")
    args = parser.parse_args()
    
    if not args.livro:
        print("Por favor, informe suas preferências (ex: --livro ação 'Tom Hanks')")
    else:
        asyncio.run(main(args.livro))