from langgraph.graph import StateGraph, END, START

from core.planner_state import PlannerState
from modules.create_itinerary import create_itinerary
from modules.input_city import input_city
from modules.input_interests import input_interests

builder = StateGraph(PlannerState)

builder.add_edge(START, "input_city")
builder.add_node("input_city", input_city)
builder.add_node("input_interests", input_interests)
builder.add_node("create_itinerary", create_itinerary)

builder.add_edge("input_city", "input_interests")
builder.add_edge("input_interests", "create_itinerary")
builder.add_edge("create_itinerary", END)

graph = builder.compile(debug=True)