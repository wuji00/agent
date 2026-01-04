import os
from typing import Annotated, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Tools ---

# In a real secure environment, we should sandbox these.
# For this demo, we will restrict them to a specific "workspace" directory.

WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "workspace")
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

def _get_safe_path(filepath: str) -> str:
    """Ensure filepath is within workspace."""
    # This is a basic check. In production, use more robust path validation.
    base = os.path.abspath(WORKSPACE_DIR)
    target = os.path.abspath(os.path.join(WORKSPACE_DIR, filepath))
    if not target.startswith(base):
        raise ValueError(f"Access denied: {filepath} is outside workspace.")
    return target

@tool
def read_file(filepath: str):
    """Read content of a file."""
    try:
        path = _get_safe_path(filepath)
        if not os.path.exists(path):
            return "Error: File not found."
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def write_file(filepath: str, content: str):
    """Write content to a file."""
    try:
        path = _get_safe_path(filepath)
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def list_files(path: str = "."):
    """List files in a directory."""
    try:
        target_path = _get_safe_path(path)
        if not os.path.isdir(target_path):
             return "Error: Not a directory."
        return str(os.listdir(target_path))
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def delete_file(filepath: str):
    """Delete a file."""
    try:
        path = _get_safe_path(filepath)
        if not os.path.exists(path):
            return "Error: File not found."
        os.remove(path)
        return f"Successfully deleted {filepath}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- Agent ---

def create_autonomous_coding_agent():
    llm = ChatAnthropic(model=MODEL_NAME)
    tools = [read_file, write_file, list_files, delete_file]

    system_prompt = f"""You are an autonomous coding agent.
You can read, write, list, and delete files in the workspace directory.
The workspace directory is located at: {WORKSPACE_DIR}
Use these tools to accomplish coding tasks.
"""

    return create_react_agent(llm, tools, prompt=system_prompt)

# --- Entry Point ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Create a file named hello.py that prints 'Hello World', then read it back."

    print(f"Processing query: {user_query}")
    agent = create_autonomous_coding_agent()

    # Run the agent
    response = agent.invoke({"messages": [HumanMessage(content=user_query)]})

    print("\n--- Response ---")
    for message in response["messages"]:
        if message.type == "ai":
             print(f"AI: {message.content}")
