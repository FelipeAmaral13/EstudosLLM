from core.planner_state import PlannerState
from core.messages import CITY_PROMPT, INVALID_CITY

def input_city(state: PlannerState):
    while True:
        user_message = input(CITY_PROMPT).strip()
        if user_message:
            return {
                "city": user_message,
                "messages": state['messages'] + [("user", user_message)],
            }
        print(INVALID_CITY)
