from langchain_core.messages import HumanMessage
from .agent import create_computer_use_agent

def main():
    print("Initializing Computer Use Agent...")
    agent = create_computer_use_agent()

    print("\n--- Computer Use Demo ---")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }

        result = agent.invoke(initial_state)

        messages = result["messages"]
        last_message = messages[-1]
        print(f"Agent: {last_message.content}")

if __name__ == "__main__":
    main()
