import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from enum import Enum
from typing import List, Optional
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Categoria(str, Enum):
    ALIMENTACAO = "Alimentação"
    TRANSPORTE = "Transporte"
    MORADIA = "Moradia"
    LAZER = "Lazer"

class TipoAlerta(str, Enum):
    GASTO_EXCESSIVO = "Gasto excessivo"
    RECEITA_INCOMUM = "Receita incomum"
    SALDO_NEGATIVO = "Saldo negativo"
    PADRAO_ATIPICO = "Padrão atípico"
    CATEGORIA_CRITICA = "Categoria crítica"

class Transacao(BaseModel):
    data: int
    valor: float
    categoria: str
    descricao: str

class MetricasFinanceiras(BaseModel):
    saldo: float
    receita: float
    despesa: float

class Alertas(BaseModel):
    tipo: TipoAlerta
    severidade: int = Field(..., ge=1, le=5)  # 1-5 escala de severidade
    transacao_relacionada: Optional[Transacao] = None
    categoria: Optional[Categoria] = None
    valor: Optional[float] = None
    periodo: Optional[str] = None  # Ex: "2023-04"
    descricao: str = Field(..., max_length=200)
    acao_recomendada: str
    
    @validator('severidade')
    def validar_severidade(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Severidade deve ser entre 1 e 5")
        return v

agent = Agent('groq:meta-llama/llama-4-scout-17b-16e-instruct',
              deps_type=MetricasFinanceiras,
              system_prompt="""
Você é um analista financeiro AI especializado em identificar padrões, anomalias e oportunidades de otimização. Siga estas diretrizes:

1. **Análise Técnica**:
   - Calcule métricas precisas (médias, medianas, tendências)
   - Identifique transações fora do padrão (2σ do desvio padrão)
   - Compare períodos mensais/anuais
   - Destaque categorias com maior variação

2. **Interpretação**:
   - Explique padrões em linguagem acessível
   - Relacione gastos com eventos relevantes
   - Contextualize números ( da renda, comparação com benchmarks)

3. **Recomendações**:
   - Sugira 3 ações concretas para otimização
   - Priorize por impacto potencial (alto/médio/baixo)
   - Inclua exemplos específicos

4. **Formato**:
   ```json
   {
     "insights": [
       {
         "tipo": "padrão|anomalia|oportunidade",
         "descricao": "Explicação técnica",
         "impacto": "alto/médio/baixo",
         "exemplo": "Dados concretos"
       }
     ],
     "alertas": [
       {
         "tipo": "gasto excessivo|receita atípica...",
         "transacao": "Referência",
         "severidade": 1-5
       }
     ]
   }
Exemplo de resposta para gastos em Alimentação:

    Padrão: "Gastos com alimentação aumentaram 25% no mês (R50→R50→R62.5/dia)"

    Causa provável: "Correlação com dias de home office (3x/semana)"

    Recomendação: "Planejar refeições semanais (economia estimada: R$15/dia)"

Mantenha respostas técnicas mas acessíveis, com dados concretos e ações acionáveis.
""")

async def analisar_transacoes(transacoes: List[Transacao]) -> str:
    """Processa transações e retorna relatório com métricas e alertas"""
    try:
        pass
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")