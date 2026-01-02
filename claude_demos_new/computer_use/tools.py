from langchain_core.tools import tool
from typing import Dict, Any, Optional, Literal

@tool
def computer_tool(
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"],
    text: Optional[str] = None,
    coordinate: Optional[list[int]] = None,
    **kwargs
):
    """
    Use a computer.
    """
    print(f"[MOCK] Computer Tool Action: {action}, Text: {text}, Coordinate: {coordinate}")
    if action == "screenshot":
        return "base64_image_placeholder"
    return "Action executed"

@tool
def bash_tool(command: str, **kwargs):
    """
    Run a bash command.
    """
    print(f"[MOCK] Bash Tool Command: {command}")
    return "Command executed"

@tool
def edit_tool(
    command: Literal["view", "create", "str_replace", "insert", "undo_edit"],
    path: str,
    file_text: Optional[str] = None,
    view_range: Optional[list[int]] = None,
    old_str: Optional[str] = None,
    new_str: Optional[str] = None,
    insert_line: Optional[int] = None,
    **kwargs
):
    """
    Edit a file.
    """
    print(f"[MOCK] Edit Tool Command: {command}, Path: {path}")
    return "File edited"
