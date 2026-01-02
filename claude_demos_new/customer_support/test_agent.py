import os
import sys

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from claude_demos_new.customer_support.graph import CustomerSupportAgent
from dotenv import load_dotenv

load_dotenv()

def test_agent():
    # Ensure ANTHROPIC_API_KEY is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return

    agent = CustomerSupportAgent()

    # Test case 1: General question
    print("\n--- Test Case 1: General Question ---")
    messages = [{"role": "user", "content": "What is Claude 3 Haiku?"}]
    result = agent.invoke(messages)
    print(result["response"].model_dump_json(indent=2))

    # Test case 2: Off-topic (should potentially redirect or say unknown)
    print("\n--- Test Case 2: Off-topic ---")
    messages = [{"role": "user", "content": "How do I bake a cake?"}]
    result = agent.invoke(messages)
    print(result["response"].model_dump_json(indent=2))

if __name__ == "__main__":
    test_agent()
