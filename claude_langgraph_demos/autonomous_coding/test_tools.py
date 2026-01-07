
import pytest
import os
from pathlib import Path
from claude_langgraph_demos.autonomous_coding.tools import read_file, write_file, list_files, delete_file, run_bash_command, WORKSPACE_DIR

# Set up a clean workspace for testing
@pytest.fixture(autouse=True)
def clean_workspace():
    # Ensure workspace exists
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    # Clean up
    for item in WORKSPACE_DIR.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            import shutil
            shutil.rmtree(item)
    yield

def test_file_operations():
    # Test write
    assert "Successfully wrote" in write_file.invoke({"filepath": "test.txt", "content": "hello world"})
    assert (WORKSPACE_DIR / "test.txt").read_text() == "hello world"

    # Test read
    assert read_file.invoke({"filepath": "test.txt"}) == "hello world"

    # Test list
    files = list_files.invoke({"path": "."})
    assert "test.txt" in files

    # Test delete
    assert "Successfully deleted" in delete_file.invoke({"filepath": "test.txt"})
    assert not (WORKSPACE_DIR / "test.txt").exists()

def test_bash_command():
    # Test allowed command
    output = run_bash_command.invoke({"command": "echo 'hello'"})
    # Echo is not in allowed list in my tools implementation, wait.
    # checking allowed commands... "ls", "cat", etc. "echo" is NOT in allowed commands in my code.
    # Let's try "ls"
    output = run_bash_command.invoke({"command": "ls"})
    assert "Error" not in output

    # Test disallowed command
    output = run_bash_command.invoke({"command": "whoami"})
    assert "Error" in output or "not allowed" in output

def test_path_traversal():
    # Test writing outside workspace
    result = write_file.invoke({"filepath": "../outside.txt", "content": "bad"})
    assert "Access denied" in result or "outside the workspace" in result
