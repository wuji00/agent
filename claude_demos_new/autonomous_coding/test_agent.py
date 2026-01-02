import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from claude_demos_new.autonomous_coding.agent import AutonomousCodingAgent
from dotenv import load_dotenv

load_dotenv()

def test_autonomous_coding():
    # Ensure ANTHROPIC_API_KEY is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return

    agent = AutonomousCodingAgent()

    print("\n--- Test Case 1: Create a python script ---")
    messages = [{"role": "user", "content": "Create a python script named 'hello.py' that prints 'Hello World' and then read it back to me."}]

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
    test_autonomous_coding()
