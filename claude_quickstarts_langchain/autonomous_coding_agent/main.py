import os
import sys
import time
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from graph import app, WORKSPACE_DIR

def main():
    print("Autonomous Coding Agent")
    print(f"Workspace: {WORKSPACE_DIR}")
    print("-----------------------")

    # Check if feature_list.json exists
    feature_list_path = os.path.join(WORKSPACE_DIR, "feature_list.json")

    if not os.path.exists(feature_list_path):
        print("Starting Initializer Agent...")
        stage = "initializer"
        initial_message = "Please initialize the project based on app_spec.txt."
    else:
        print("Starting Coding Agent...")
        stage = "coding"
        initial_message = "Please continue working on the project. Check feature_list.json and implement the next feature."

    messages = [HumanMessage(content=initial_message)]
    state = {"messages": messages, "stage": stage}

    print(f"Stage: {stage}")
    print("Agent is working... (this may take a while)")

    try:
        # Use invoke to run the graph until END
        result = app.invoke(state)

        # Print the final response
        last_msg = result["messages"][-1]
        print(f"\nFinal Response:\n{last_msg.content}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
