import sys
import os

# Add parent directory to path so we can import customer_support
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from customer_support.graph import app
from langchain_core.messages import HumanMessage

def main():
    print("Customer Support Agent (Type 'quit' to exit)")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return

    chat_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        chat_history.append(HumanMessage(content=user_input))

        state = {
            "messages": chat_history,
            "context": "",
            "response": None
        }

        result = app.invoke(state)
        response = result["response"]

        # Add assistant response to history
        chat_history.append(AIMessage(content=response.response))

        print(f"\nAssistant: {response.response}")
        print(f"Thinking: {response.thinking}")
        print(f"Mood: {response.user_mood}")
        if response.redirect_to_agent and response.redirect_to_agent.should_redirect:
            print(f"[REDIRECT] Reason: {response.redirect_to_agent.reason}")

if __name__ == "__main__":
    main()
