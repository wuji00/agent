import os
import subprocess
from pathlib import Path
from typing import Optional, List
from langchain_core.tools import tool

# Global configuration for the workspace
# Initialize relative to this file to avoid hardcoding absolute paths that might break
# However, this tool module might be imported from anywhere.
# The 'set_workspace' function is crucial.
WORKSPACE_DIR: Path = Path("./autonomous_workspace").resolve()

def set_workspace(path: Path):
    global WORKSPACE_DIR
    WORKSPACE_DIR = path.resolve()
    # Ensure it exists
    if not WORKSPACE_DIR.exists():
        try:
             WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create workspace dir {WORKSPACE_DIR}: {e}")

def validate_path(filepath: str) -> Path:
    """
    Validates that the given filepath is within the workspace directory.
    Returns the resolved absolute path.
    """
    try:
        # Handle absolute paths that might be inside the workspace
        path = Path(filepath)
        if path.is_absolute():
            resolved_path = path.resolve()
        else:
            resolved_path = (WORKSPACE_DIR / filepath).resolve()

        # Security check: Ensure the resolved path starts with the workspace path
        if not str(resolved_path).startswith(str(WORKSPACE_DIR)):
            raise ValueError(f"Access denied: {filepath} is outside the workspace {WORKSPACE_DIR}")
        return resolved_path
    except Exception as e:
        raise ValueError(f"Invalid path: {filepath}. Error: {e}")

@tool
def read_file(filepath: str) -> str:
    """
    Reads the content of a file.

    Args:
        filepath: The path to the file to read, relative to the workspace.
    """
    try:
        path = validate_path(filepath)
        if not path.exists():
            return f"Error: File {filepath} does not exist."
        return path.read_text()
    except Exception as e:
        return f"Error reading file {filepath}: {e}"

@tool
def write_file(filepath: str, content: str) -> str:
    """
    Writes content to a file. Overwrites the file if it exists.

    Args:
        filepath: The path to the file to write, relative to the workspace.
        content: The content to write to the file.
    """
    try:
        path = validate_path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing to file {filepath}: {e}"

@tool
def list_files(path: str = ".") -> str:
    """
    Lists files and directories in the given path.

    Args:
        path: The directory to list, relative to the workspace. Defaults to root.
    """
    try:
        target_path = validate_path(path)
        if not target_path.exists():
            return f"Error: Path {path} does not exist."
        if not target_path.is_dir():
            return f"Error: Path {path} is not a directory."

        items = []
        for item in target_path.iterdir():
            name = item.name
            if item.is_dir():
                name += "/"
            items.append(name)

        return "\n".join(sorted(items))
    except Exception as e:
        return f"Error listing files in {path}: {e}"

@tool
def delete_file(filepath: str) -> str:
    """
    Deletes a file.

    Args:
        filepath: The path to the file to delete, relative to the workspace.
    """
    try:
        path = validate_path(filepath)
        if not path.exists():
            return f"Error: File {filepath} does not exist."
        if path.is_dir():
            return f"Error: {filepath} is a directory. Use a different tool to remove directories."
        path.unlink()
        return f"Successfully deleted {filepath}"
    except Exception as e:
        return f"Error deleting file {filepath}: {e}"

@tool
def run_bash_command(command: str) -> str:
    """
    Runs a bash command in the workspace directory.

    Args:
        command: The bash command to run.
    """
    try:
        # Basic security check - this is a demo, so we won't implement full sandboxing
        # but we should block obvious dangerous commands if possible.
        # For this implementation, we rely on the fact that we are running inside the workspace dir.
        # But we should be careful about commands that leave the directory.

        # We also need to be careful about blocking calls.

        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=120 # 2 minute timeout
        )

        output = result.stdout
        if result.stderr:
            output += f"\nStderr: {result.stderr}"

        if result.returncode != 0:
            output += f"\nExit code: {result.returncode}"

        return output
    except subprocess.TimeoutExpired:
        return "Error: Command timed out."
    except Exception as e:
        return f"Error running command: {e}"

ALL_TOOLS = [read_file, write_file, list_files, delete_file, run_bash_command]
