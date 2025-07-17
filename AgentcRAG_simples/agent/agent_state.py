from typing import  TypedDict, Sequence

class AgentState(TypedDict):
    question: str
    documents: Sequence[dict]
    context: str
    answer: str