import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from financial_analyst.agent import build_agent
from langchain_core.messages import HumanMessage

load_dotenv()

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY in .env or environment variables.")
        return

    agent = build_agent()

    print("Financial Data Analyst (Type 'quit' to exit)")
    print("Example: 'What is the price of AAPL and its PE ratio?'")

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
            # The agent expects a list of messages or a dictionary with 'messages'
            state = {"messages": [HumanMessage(content=query)]}
            result = agent.invoke(state)

            # The result contains the state history. The last message is the answer.
            last_message = result["messages"][-1]
            print(f"\nAnalyst: {last_message.content}")
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
