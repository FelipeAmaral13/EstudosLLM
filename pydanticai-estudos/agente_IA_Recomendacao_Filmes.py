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
    parser = argparse.ArgumentParser(description="Agente de IA simples para recomendações de filmes")
    parser.add_argument("--filmes", type=str, help="Recomendação filmes")
    return parser.parse_args()

class Filme(BaseModel):
    titulo: str
    ano: int
    genero: str
    duracao: int
    elenco: List[str]

class Plataforma(BaseModel):
    nome: str
    tipo: str = "streaming"

class Recomendacao(BaseModel):
    filme_principal: Filme
    similares: List[Filme]
    motivo: str
    plataformas: Optional[List[Plataforma]] = None

agent = Agent('groq:meta-llama/llama-4-scout-17b-16e-instruct',
              deps_type=Recomendacao,
              system_prompt="Você é um especialista em cinema que faz recomendações personalizadas. Forneça detalhes sobre os filmes e explique por que são boas recomendações."
            )

async def main(preferencias: List[str]):
    """Obtém recomendações de filmes baseado nas preferências do usuário"""
    try:
        try:
            logger.info("Tentando abordagem estruturada...")
            prompt = (
                f"Para alguém que gosta de {', '.join(preferencias)}, recomende:\n"
                "1. Um filme principal (com título, ano, gênero, duração em minutos e elenco principal)\n"
                "2. Três filmes similares (com título, ano, gênero, duração em minutos e elenco principal)\n"
                "3. Um motivo detalhado da recomendação\n\n"
            )

            result = await agent.run(prompt, deps=Recomendacao(
                filme_principal=Filme(titulo="", ano=0, genero="", duracao=0, elenco=[]),
                similares=[Filme(titulo="", ano=0, genero="", duracao=0, elenco=[]) for _ in range(3)],
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
    parser = argparse.ArgumentParser(description="Recomendador de filmes")
    parser.add_argument("--preferencias", nargs="+", help="Preferências para recomendação (gêneros, atores, etc.)")
    args = parser.parse_args()
    
    if not args.preferencias:
        print("Por favor, informe suas preferências (ex: --preferencias ação 'Tom Hanks')")
    else:
        asyncio.run(main(args.preferencias))