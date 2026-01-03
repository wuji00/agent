from langchain_core.messages import HumanMessage
from .agent import create_coding_agent

def main():
    print("Initializing Autonomous Coding Agent...")
    agent = create_coding_agent()

    print("\n--- Autonomous Coding Demo ---")
    print("The agent works in the 'workspace' directory.")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }

        # Stream the output to see intermediate steps
        print("Agent is working...")
        result = agent.invoke(initial_state)

        messages = result["messages"]
        last_message = messages[-1]
        print(f"Agent: {last_message.content}")

if __name__ == "__main__":
    main()
