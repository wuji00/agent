import os
from pathlib import Path
from typing import List, Optional
from langchain_core.tools import tool

# Workspace directory for safety
WORKSPACE_DIR = Path(__file__).parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

def _validate_path(path: str) -> Path:
    """Validate that the path is within the workspace."""
    full_path = (WORKSPACE_DIR / path).resolve()
    if not str(full_path).startswith(str(WORKSPACE_DIR.resolve())):
        raise ValueError(f"Access denied: {path} is outside the workspace.")
    return full_path

@tool
def read_file(filepath: str) -> str:
    """Read the content of a file."""
    try:
        path = _validate_path(filepath)
        if not path.exists():
            return f"Error: File {filepath} does not exist."
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a file."""
    try:
        path = _validate_path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def list_files(path: str = ".") -> str:
    """List files in a directory."""
    try:
        target_path = _validate_path(path)
        if not target_path.exists():
             return f"Error: Directory {path} does not exist."

        files = [f.name for f in target_path.iterdir()]
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def delete_file(filepath: str) -> str:
    """Delete a file."""
    try:
        path = _validate_path(filepath)
        if not path.exists():
            return f"Error: File {filepath} does not exist."
        os.remove(path)
        return f"Successfully deleted {filepath}"
    except Exception as e:
        return f"Error deleting file: {e}"
