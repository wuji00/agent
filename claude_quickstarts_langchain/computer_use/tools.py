from typing import Literal, Optional
from langchain_core.tools import tool

@tool
def computer(
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"],
    text: Optional[str] = None,
    coordinate: Optional[list[int]] = None
):
    """
    Use a computer.
    action: The action to perform.
    text: The text to type (for 'type' action) or key sequence (for 'key' action).
    coordinate: [x, y] coordinates for mouse actions.
    """
    if action == "screenshot":
        # In a real app, this returns base64 image.
        # Here we return a placeholder.
        return "Screenshot taken (simulated)."

    return f"Performed {action} with text='{text}' at {coordinate}"

@tool
def bash(command: str):
    """Run a bash command."""
    return f"Executed: {command} (simulated)"

@tool
def str_replace_editor(command: str, path: str, file_text: Optional[str] = None, view_range: Optional[list[int]] = None, old_str: Optional[str] = None, new_str: Optional[str] = None):
    """
    View or edit a file.
    command: view, create, str_replace, insert, undo_edit.
    """
    return f"Editor command {command} on {path} (simulated)"
