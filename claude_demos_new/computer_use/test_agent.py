import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from claude_demos_new.computer_use.agent import ComputerUseAgent
from dotenv import load_dotenv

load_dotenv()

def test_computer_use():
    # Ensure ANTHROPIC_API_KEY is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return

    agent = ComputerUseAgent()

    print("\n--- Test Case 1: Click something ---")
    messages = [{"role": "user", "content": "Click on the start button."}]

    # Iterate through the stream to show tool calls
    for event in agent.agent.stream({"messages": messages}, stream_mode="values"):
        message = event["messages"][-1]
        print(f"\nRole: {message.type}")
        print(f"Content: {message.content}")
        if hasattr(message, "tool_calls") and message.tool_calls:
            print("Tool Calls:")
            for tc in message.tool_calls:
                print(f"  - {tc['name']}: {tc['args']}")

if __name__ == "__main__":
    test_computer_use()
