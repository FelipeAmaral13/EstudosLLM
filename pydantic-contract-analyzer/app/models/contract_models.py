from typing import List, Optional
from pydantic import BaseModel, Field

class ContractInput(BaseModel):
    contract_text: str = Field(..., description="Texto completo do contrato recebido")

class ClauseEvaluation(BaseModel):
    clause: str
    risk_level: str  # ex: 'baixo', 'médio', 'alto'
    suggestion: Optional[str]

class ContractAnalysis(BaseModel):
    overall_risk: str
    evaluated_clauses: List[ClauseEvaluation]
