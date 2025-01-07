from core.state_graph import graph
from core.messages import START_PROMPT, QUIT_PROMPT, QUIT_MESSAGE

while True:
    print(START_PROMPT)
    user_input = input(QUIT_PROMPT).strip()
    if user_input.lower() in ["quit", "exit", "q"]:
        print(QUIT_MESSAGE)
        break
    for event in graph.stream({"messages": [("user", user_input)]}):
        pass
