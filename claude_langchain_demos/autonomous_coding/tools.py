import os
from langchain_core.tools import tool

# Ensure workspace exists
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "workspace"))
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

def _is_safe_path(base_dir: str, path: str) -> bool:
    """Ensure path is within base_dir."""
    match_path = os.path.abspath(path)
    return match_path.startswith(base_dir)

@tool
def list_files():
    """List files in the workspace."""
    return os.listdir(WORKSPACE_DIR)

@tool
def read_file(filename: str):
    """Read content of a file in the workspace."""
    filepath = os.path.join(WORKSPACE_DIR, filename)

    if not _is_safe_path(WORKSPACE_DIR, filepath):
        return "Error: Access outside workspace denied."

    if not os.path.exists(filepath):
        return "File not found."

    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(filename: str, content: str):
    """Write content to a file in the workspace."""
    filepath = os.path.join(WORKSPACE_DIR, filename)

    if not _is_safe_path(WORKSPACE_DIR, filepath):
        return "Error: Access outside workspace denied."

    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"File {filename} written."
    except Exception as e:
        return f"Error writing file: {e}"
