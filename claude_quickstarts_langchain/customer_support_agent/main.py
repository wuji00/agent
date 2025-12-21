import os
import sys
# Add parent directory to path to allow importing from graph.py if run from subfolder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from graph import app

def main():
    print("Customer Support Agent (Type 'quit' to exit)")
    print("--------------------------------------------")

    # We maintain the conversation history here
    chat_history = []

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break

        if user_input.lower() in ["quit", "exit"]:
            break

        # Create a new message
        new_message = HumanMessage(content=user_input)
        chat_history.append(new_message)

        # Invoke the graph with the current history
        inputs = {"messages": chat_history}

        try:
            result = app.invoke(inputs)

            analysis = result.get("analysis", {})
            response_text = analysis.get("response", "No response")

            print(f"\nThinking: {analysis.get('thinking', '')}")
            print(f"Agent: {response_text}")
            print(f"Mood: {analysis.get('user_mood', '')}")

            if analysis.get('redirect_to_agent', {}).get('should_redirect'):
                print("[REDIRECT RECOMMENDED]")

            # Update chat_history with the agent's response
            chat_history = result["messages"]

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
