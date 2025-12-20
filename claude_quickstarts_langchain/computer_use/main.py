import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from computer_use.graph import get_app
from langchain_core.messages import HumanMessage

def main():
    print("Computer Use Demo (Simulated)")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return

    app = get_app()

    chat_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        chat_history.append(HumanMessage(content=user_input))

        result = app.invoke({"messages": chat_history})
        chat_history = result["messages"]

        last_msg = chat_history[-1]
        print(f"\nAgent: {last_msg.content}")

if __name__ == "__main__":
    main()
