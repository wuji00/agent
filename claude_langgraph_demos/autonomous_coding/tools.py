import os
import shlex
import shutil
import asyncio
from pathlib import Path
from typing import List, Optional, Union
import subprocess
from langchain_core.tools import tool

# Workspace setup
WORKSPACE_DIR = Path("./workspace").resolve()
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

# Allowed commands for development tasks
ALLOWED_COMMANDS = {
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep",
    # File operations
    "cp", "mkdir", "chmod", "mv", "rm",
    # Directory
    "pwd",
    # Node.js development
    "npm", "node", "npx",
    # Version control
    "git",
    # Process management
    "ps", "lsof", "sleep", "pkill",
    # Script execution
    "init.sh", "./init.sh"
}

COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod", "init.sh"}

def _validate_path(filepath: str) -> Path:
    """Validate that the filepath is within the workspace directory."""
    try:
        # Handle absolute paths that start with the workspace dir
        path = Path(filepath).resolve()
        if not str(path).startswith(str(WORKSPACE_DIR)):
            # If it's a relative path, resolve it relative to workspace
            path = (WORKSPACE_DIR / filepath).resolve()

        if not str(path).startswith(str(WORKSPACE_DIR)):
            raise ValueError(f"Access denied: {filepath} is outside the workspace directory.")
        return path
    except Exception as e:
        raise ValueError(f"Invalid path: {filepath}. Error: {str(e)}")

def _validate_command(command_string: str) -> None:
    """Validate that the command is safe to run."""
    # This is a simplified validation compared to the full security.py,
    # but captures the essence for this demo.

    # Split on common separators
    import re
    # Simplified splitting logic
    segments = re.split(r'[;&|]+', command_string)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        try:
            tokens = shlex.split(segment)
        except ValueError:
            raise ValueError(f"Could not parse command: {segment}")

        if not tokens:
            continue

        # Ignore env vars settings like VAR=val
        cmd_idx = 0
        while cmd_idx < len(tokens) and '=' in tokens[cmd_idx]:
            cmd_idx += 1

        if cmd_idx >= len(tokens):
            continue

        base_cmd = os.path.basename(tokens[cmd_idx])

        if base_cmd not in ALLOWED_COMMANDS:
             raise ValueError(f"Command '{base_cmd}' is not allowed.")

@tool
def read_file(filepath: str) -> str:
    """Read the content of a file."""
    try:
        path = _validate_path(filepath)
        if not path.exists():
            return f"Error: File {filepath} does not exist."
        return path.read_text()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a file. Creates directories if they don't exist."""
    try:
        path = _validate_path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@tool
def list_files(path: str = ".") -> str:
    """List files in a directory."""
    try:
        target_path = _validate_path(path)
        if not target_path.exists():
             return f"Error: Path {path} does not exist."

        # Use ls -R like output or just simple list
        # For simplicity, using os.walk or just glob
        files = []
        for p in target_path.glob("*"):
            files.append(f"{p.name}{'/' if p.is_dir() else ''}")
        return "\n".join(sorted(files))
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool
def delete_file(filepath: str) -> str:
    """Delete a file."""
    try:
        path = _validate_path(filepath)
        if not path.exists():
            return f"Error: File {filepath} does not exist."
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return f"Successfully deleted {filepath}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"

@tool
def run_bash_command(command: str) -> str:
    """Run a bash command in the workspace directory. Only allowed commands can be executed."""
    try:
        _validate_command(command)

        # Run command
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        output = result.stdout
        if result.stderr:
            output += f"\nStderr: {result.stderr}"

        return output
    except Exception as e:
        return f"Error running command: {str(e)}"

ALL_TOOLS = [read_file, write_file, list_files, delete_file, run_bash_command]
