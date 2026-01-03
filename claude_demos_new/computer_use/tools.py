from typing import Any, Dict
from langchain_core.tools import tool

@tool
def computer_tool(action: str, coordinate: tuple = None, text: str = None) -> str:
    """
    Simulates computer interaction (mouse/keyboard).
    Actions: 'click', 'type', 'key', 'screenshot'.
    """
    print(f"[Computer Tool] Action: {action}, Coordinate: {coordinate}, Text: {text}")
    return "Action executed successfully (mock)."

@tool
def bash_tool(command: str) -> str:
    """
    Executes a bash command.
    """
    print(f"[Bash Tool] Command: {command}")
    return "Command executed successfully (mock)."

@tool
def edit_tool(path: str, command: str, content: str = None) -> str:
    """
    Edits a file.
    """
    print(f"[Edit Tool] Path: {path}, Command: {command}")
    return "File edited successfully (mock)."
