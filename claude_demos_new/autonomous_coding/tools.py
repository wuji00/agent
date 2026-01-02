import os
from langchain_core.tools import tool
from typing import Optional

# Using path validation to restrict access as per memory
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "workspace"))
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

def _validate_path(filepath: str) -> str:
    """Ensure the path is within the workspace directory."""
    full_path = os.path.abspath(os.path.join(WORKSPACE_DIR, filepath))
    if not full_path.startswith(WORKSPACE_DIR):
        raise ValueError(f"Access denied: {filepath} is outside the workspace.")
    return full_path

@tool
def read_file(filepath: str):
    """Read the content of a file."""
    try:
        full_path = _validate_path(filepath)
        if not os.path.exists(full_path):
            return f"Error: File {filepath} does not exist."
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def write_file(filepath: str, content: str):
    """Write content to a file."""
    try:
        full_path = _validate_path(filepath)
        with open(full_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@tool
def list_files(path: str = "."):
    """List files in a directory."""
    try:
        full_path = _validate_path(path)
        if not os.path.exists(full_path):
             return f"Error: Directory {path} does not exist."
        return str(os.listdir(full_path))
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool
def delete_file(filepath: str):
    """Delete a file."""
    try:
        full_path = _validate_path(filepath)
        if not os.path.exists(full_path):
            return f"Error: File {filepath} does not exist."
        os.remove(full_path)
        return f"Successfully deleted {filepath}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"
