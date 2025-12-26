from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import ShellTool
from pathlib import Path
import os
from langchain_core.tools import tool

WORKSPACE_DIR = Path("./autonomous_coding/workspace").resolve()
if not WORKSPACE_DIR.exists():
    # If running from root
    WORKSPACE_DIR = Path("claude_quickstarts_langchain/autonomous_coding/workspace").resolve()

WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

def get_tools():
    # Restrict file access to workspace
    toolkit = FileManagementToolkit(root_dir=str(WORKSPACE_DIR))
    file_tools = toolkit.get_tools()

    shell_tool = ShellTool()

    @tool
    def run_shell_command(command: str):
        """Run a shell command in the workspace directory."""
        full_command = f"cd {WORKSPACE_DIR} && {command}"
        return shell_tool.run(full_command)

    return file_tools + [run_shell_command]
