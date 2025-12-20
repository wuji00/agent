import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from agent import build_agent
from langchain_core.messages import HumanMessage

load_dotenv()

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY in .env or environment variables.")
        return

    agent = build_agent()

    print("Autonomous Coding Agent")
    print("Files will be created in 'workspace/' directory.")
    print("Example: 'Create a python script that prints hello world and save it as hello.py'")

    while True:
        try:
            query = input("User: ")
        except EOFError:
            break

        if query.lower() in ["quit", "exit"]:
            break

        if not query.strip():
            continue

        print("Processing...")
        try:
            state = {"messages": [HumanMessage(content=query)]}
            result = agent.invoke(state)

            last_message = result["messages"][-1]
            print(f"\nAgent: {last_message.content}")
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
