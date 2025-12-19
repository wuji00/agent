from langchain_core.tools import tool
from typing import Literal, Optional, List

@tool
def computer_tool(
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"],
    text: Optional[str] = None,
    coordinate: Optional[List[int]] = None,
):
    """
    Use a computer.
    action: The action to perform.
    text: The text to type (for 'type' action).
    coordinate: The [x, y] coordinates (for mouse actions).
    """
    if action == "screenshot":
        # In a real app, this returns base64 image data
        return "Screenshot taken (mock data)"

    if action == "mouse_move":
        return f"Moved mouse to {coordinate}"

    if action == "type":
        return f"Typed: {text}"

    return f"Executed action: {action}"

@tool
def bash_tool(command: str):
    """
    Run a bash command.
    """
    # For security in this demo, we just echo the command
    return f"Executed bash command: {command}"

@tool
def edit_tool(
    command: Literal["view", "create", "str_replace", "insert", "undo_edit"],
    path: str,
    file_text: Optional[str] = None,
    view_range: Optional[List[int]] = None,
    old_str: Optional[str] = None,
    new_str: Optional[str] = None,
    insert_line: Optional[int] = None,
):
    """
    View or edit a file.
    """
    return f"File operation '{command}' on {path} simulated."
