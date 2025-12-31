import os
import sys
import shutil
from typing import Annotated, TypedDict, List, Dict, Any, Union, Optional, Literal
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"
WORKSPACE_DIR = os.path.join(os.getcwd(), "workspace")

# Ensure workspace exists
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def validate_path(path: str) -> str:
    """Ensure path is within the workspace."""
    full_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    if not full_path.startswith(os.path.abspath(WORKSPACE_DIR)):
        raise ValueError(f"Access denied: {path} is outside the workspace.")
    return full_path

# --- Tools ---
@tool
def list_files(path: str = ".") -> List[str]:
    """List files in the directory."""
    try:
        target_path = validate_path(path)
        if not os.path.exists(target_path):
             return []
        return os.listdir(target_path)
    except Exception as e:
        return f"Error: {e}"

@tool
def read_file(path: str) -> str:
    """Read the content of a file."""
    try:
        target_path = validate_path(path)
        with open(target_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        target_path = validate_path(path)
        with open(target_path, "w") as f:
            f.write(content)
        return f"File {path} written successfully."
    except Exception as e:
        return f"Error: {e}"

@tool
def delete_file(path: str) -> str:
    """Delete a file."""
    try:
        target_path = validate_path(path)
        if os.path.exists(target_path):
            os.remove(target_path)
            return f"File {path} deleted successfully."
        return f"File {path} not found."
    except Exception as e:
        return f"Error: {e}"

tools = [list_files, read_file, write_file, delete_file]

# --- System Prompt ---
SYSTEM_PROMPT = """You are an autonomous coding agent. You can read, write, list, and delete files in the workspace.
Your goal is to complete the user's coding request.
"""

# --- Agent Construction ---
def create_autonomous_coding_agent():
    llm = ChatAnthropic(model=MODEL_NAME, temperature=0.7)
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    return agent

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Create a hello world python script and a README.md explaining it."

    print(f"User Query: {user_query}")
    print(f"Workspace: {WORKSPACE_DIR}")

    agent = create_autonomous_coding_agent()

    try:
        result = agent.invoke({"messages": [HumanMessage(content=user_query)]})

        print("\n--- Final Messages ---")
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                if msg.tool_calls:
                     print(f"Agent used tool: {msg.tool_calls[0]['name']}")
                else:
                     print(f"Agent: {msg.content}")
            elif isinstance(msg, ToolMessage):
                print(f"Tool Output: [Result from {msg.name}]")
    except Exception as e:
        print(f"Error: {e}")
