from core.planner_state import PlannerState

def input_interests(state: PlannerState) -> dict:
    while True:
        user_message = input(
            f"Por favor, insira seus interesses para a viagem para {state['city']} (separados por vírgulas): "
        ).strip()
        if user_message:
            return {
                "interests": [interest.strip() for interest in user_message.split(',')],
                "messages": state['messages'] + [("user", user_message)],
            }
        print("Entrada inválida. Por favor, insira pelo menos um interesse.")
