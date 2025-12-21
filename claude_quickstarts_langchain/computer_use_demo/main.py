import os
import sys
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from graph import app

def main():
    print("Computer Use Demo (Mock Environment)")
    print("------------------------------------")
    print("Note: This demo uses mock tools that print actions but do not execute them on a real screen.")

    chat_history = []

    while True:
        try:
            user_input = input("\nUser: ")
        except EOFError:
            break

        if user_input.lower() in ["quit", "exit"]:
            break

        chat_history.append(HumanMessage(content=user_input))
        inputs = {"messages": chat_history}

        print("\nAgent is working...")
        try:
            result = app.invoke(inputs)
            chat_history = result["messages"]

            # Print tool calls for better visibility
            # We want to print tool calls that happened after our user input.
            last_user_idx = -1
            for i, msg in enumerate(chat_history):
                if msg.type == "human":
                    last_user_idx = i

            if last_user_idx != -1:
                new_msgs = chat_history[last_user_idx+1:]
                for msg in new_msgs:
                    if msg.type == "ai":
                        if msg.tool_calls:
                            for tc in msg.tool_calls:
                                 print(f"\n[Tool Call]: {tc['name']}")
                                 print(f"  Args: {tc['args']}")
                        if msg.content:
                            print(f"\nAgent: {msg.content}")
                    elif msg.type == "tool":
                        print(f"\n[Tool Output]: {msg.content}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
