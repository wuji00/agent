import os
from langchain_core.messages import HumanMessage
from .graph import create_customer_support_graph

def main():
    print("Initializing Customer Support Agent...")
    graph = create_customer_support_graph()

    print("\n--- Customer Support Demo ---")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "category": "",
            "context": "",
            "answer": ""
        }

        result = graph.invoke(initial_state)

        print(f"Category: {result.get('category')}")
        print(f"Agent: {result.get('answer')}")

if __name__ == "__main__":
    main()
