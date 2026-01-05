import os
import sys

# Add project root to sys.path so we can import modules if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from customer_support.agent import build_graph

load_dotenv()

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY in .env or environment variables.")
        return

    try:
        graph = build_graph()
    except Exception as e:
        print(f"Error initializing graph: {e}")
        return

    print("Customer Support Agent (Type 'quit' to exit)")
    print("This demo uses a local knowledge base about Anthropic.")

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
            result = graph.invoke({"query": query})
            resp = result["response"]

            print(f"\nAgent (Thinking: {resp.get('thinking')})")
            print(f"Response: {resp.get('response')}")
            print(f"Categories: {resp.get('matched_categories')}")
            print(f"Mood: {resp.get('user_mood')}")
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
