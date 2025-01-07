from typing import TypedDict, Annotated, List
from langgraph.graph.message import AnyMessage, add_messages


class PlannerState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    city: str
    interests: List[str]
    itinerary: str