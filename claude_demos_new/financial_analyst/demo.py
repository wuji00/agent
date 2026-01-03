from langchain_core.messages import HumanMessage
from .agent import create_financial_agent

def main():
    print("Initializing Financial Data Analyst...")
    agent = create_financial_agent()

    print("\n--- Financial Data Analyst Demo ---")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }

        result = agent.invoke(initial_state)

        # The result of create_react_agent is a dict with 'messages'
        messages = result["messages"]
        last_message = messages[-1]
        print(f"Agent: {last_message.content}")

if __name__ == "__main__":
    main()
