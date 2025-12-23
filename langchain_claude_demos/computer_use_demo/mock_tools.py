from langchain_core.tools import tool
import json

@tool
def computer(action: str, coordinate: list[int] = None, text: str = None):
    """
    Simulates computer interaction.
    Actions:
    - click: requires coordinate [x, y]
    - type: requires text
    - screenshot: returns a mock screenshot description
    - scroll: requires coordinate [x, y] (optional)
    """
    if action == "screenshot":
        return "Screenshot: [Desktop with a browser window open showing Google homepage]"
    elif action == "click":
        return f"Clicked at {coordinate}"
    elif action == "type":
        return f"Typed: '{text}'"
    elif action == "scroll":
        return f"Scrolled at {coordinate}"
    else:
        return f"Unknown action: {action}"

@tool
def bash(command: str):
    """
    Simulates a bash shell.
    """
    return f"Executed: {command}\nOutput: [Mock Output]"

@tool
def str_replace_editor(command: str, path: str, file_text: str = None, view_range: list[int] = None, old_str: str = None, new_str: str = None):
    """
    Simulates a text editor.
    """
    return f"Editor command {command} on {path} executed."

tools = [computer, bash, str_replace_editor]
