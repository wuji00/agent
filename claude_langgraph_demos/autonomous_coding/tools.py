"""
Autonomous Coding Demo using LangGraph
"""
import os
import shutil
import glob
from typing import Optional, List
from pathlib import Path
import subprocess

from langchain_core.tools import tool

# Configuration
# This is where the agent works. We restrict it to this directory.
# In a real app, this should be dynamic or passed as an argument.
WORKSPACE_DIR = Path("workspace").resolve()

def validate_path(path: str) -> Path:
    """Ensure the path is within the workspace directory."""
    full_path = (WORKSPACE_DIR / path).resolve()
    if not str(full_path).startswith(str(WORKSPACE_DIR)):
        raise ValueError(f"Access denied: {path} is outside the workspace.")
    return full_path

@tool
def read_file(path: str) -> str:
    """Reads the content of a file."""
    try:
        p = validate_path(path)
        if not p.exists():
            return f"Error: File {path} does not exist."
        return p.read_text()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file. Creates directories if needed."""
    try:
        p = validate_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def list_files(path: str = ".") -> str:
    """Lists files in a directory."""
    try:
        p = validate_path(path)
        if not p.exists():
             return f"Error: Directory {path} does not exist."
        # Use glob to list recursively if needed, but for now just basic ls
        files = [f.name for f in p.iterdir()]
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def delete_file(path: str) -> str:
    """Deletes a file."""
    try:
        p = validate_path(path)
        if not p.exists():
            return f"Error: File {path} does not exist."
        p.unlink()
        return f"Successfully deleted {path}"
    except Exception as e:
        return f"Error deleting file: {e}"

@tool
def run_bash_command(command: str) -> str:
    """
    Runs a bash command.
    Security Note: Only allow specific safe commands or warn about risks.
    For this demo, we allow basic commands but this is dangerous in production.
    """
    # Basic security check - in a real agent this should be much stricter
    forbidden = ["rm -rf /", "sudo", "mkfs", "dd"]
    if any(cmd in command for cmd in forbidden):
        return f"Command blocked for security reasons: {command}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=30 # Prevent hanging
        )
        output = result.stdout
        if result.stderr:
            output += f"\nStderr: {result.stderr}"
        return output
    except Exception as e:
        return f"Error running command: {e}"

TOOLS = [read_file, write_file, list_files, delete_file, run_bash_command]
