import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autonomous_coding.graph import app

def main():
    print("Autonomous Coding Agent")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return

    request = input("What would you like to build? ")

    state = {
        "request": request,
        "features": [],
        "completed_features": [],
        "current_task": None,
        "messages": []
    }

    print("Starting agent loop...")
    for output in app.stream(state):
        for key, value in output.items():
            print(f"Output from {key}:")
            if key == "planner" and value.get("current_task"):
                 print(f"--> Next Task: {value.get('current_task')}")
            if key == "coder":
                 print(f"--> Finished Task.")

    print("All tasks completed.")

if __name__ == "__main__":
    main()
