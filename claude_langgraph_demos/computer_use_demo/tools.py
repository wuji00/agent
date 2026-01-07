from langchain_core.tools import tool

@tool
def computer_tool(action: str, coordinate: tuple[int, int] = None, text: str = None):
    """
    Simulates computer interaction.
    Args:
        action: The action to perform (click, type, scroll, etc.)
        coordinate: (x, y) coordinates for click/move
        text: Text to type
    """
    return f"Executed {action} at {coordinate} with text '{text}'"

@tool
def bash_tool(command: str):
    """
    Simulates running a bash command.
    """
    return f"Executed bash command: {command}"

@tool
def edit_tool(filepath: str, content: str):
    """
    Simulates editing a file.
    """
    return f"Edited file {filepath}"
