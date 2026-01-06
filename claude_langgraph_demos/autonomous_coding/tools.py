from langchain_core.tools import tool
import os
import glob
import shutil
from typing import List, Optional, Literal

@tool
def read_file(filepath: str) -> str:
    """Reads the content of a file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(filepath: str, content: str) -> str:
    """Writes content to a file."""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def list_files(path: str = ".") -> str:
    """Lists files in a directory."""
    try:
        files = glob.glob(os.path.join(path, "*"))
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def delete_file(filepath: str) -> str:
    """Deletes a file."""
    try:
        os.remove(filepath)
        return f"Successfully deleted {filepath}"
    except Exception as e:
        return f"Error deleting file: {e}"

@tool
def browser_tool(
    action: Literal["navigate", "click", "type", "scroll", "screenshot", "get_html"],
    url: Optional[str] = None,
    selector: Optional[str] = None,
    text: Optional[str] = None,
    coordinate: Optional[List[int]] = None
):
    """
    Interact with a web browser (Mock).

    actions:
    - navigate: Go to a URL.
    - click: Click on an element (by selector or coordinate).
    - type: Type text into an element.
    - scroll: Scroll the page.
    - screenshot: Take a screenshot.
    - get_html: Get the HTML content.
    """
    print(f"[MOCK TOOL] browser: action={action}, url={url}, selector={selector}")

    if action == "navigate":
        return f"Navigated to {url}"
    elif action == "get_html":
        return "<html><body><h1>Mock Page</h1></body></html>"
    elif action == "screenshot":
        return "Screenshot taken (mock)"

    return "Action executed successfully."
