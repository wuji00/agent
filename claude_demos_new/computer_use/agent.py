from typing import Annotated, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# --- Configuration ---
# Computer use requires a specific model and beta header
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Mock Tools ---
# In a real scenario, these would interact with the OS/Browser.
# For this headless demo, we just log the actions.

@tool
def computer_tool(action: Literal["key", "type", "mouse_move", "left_click", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"],
                  text: str = None,
                  coordinate: list[int] = None):
    """
    Simulates interacting with a computer.
    supported actions: key, type, mouse_move, left_click, right_click, middle_click, double_click, screenshot, cursor_position.
    """
    if action == "screenshot":
        return "Screenshot taken (mock_screenshot_base64_data)"
    if action == "cursor_position":
        return {"x": 500, "y": 500}

    return f"Executed computer action: {action} with text='{text}' and coordinate={coordinate}"

@tool
def bash_tool(command: str):
    """
    Simulates executing a bash command.
    """
    return f"Executed bash command: {command}\nOutput: (Mock output for {command})"

@tool
def edit_tool(command: Literal["create", "str_replace", "insert", "undo_edit"],
              path: str,
              file_text: str = None,
              view_range: list[int] = None,
              old_str: str = None,
              new_str: str = None,
              insert_line: int = None):
    """
    Simulates editing a file.
    """
    return f"Executed edit command: {command} on {path}"

# --- Agent ---

def create_computer_use_agent():
    # Note: To use real computer use features via Anthropic API, we need:
    # model_kwargs={"betas": ["computer-use-2024-10-22"]}
    # However, ChatAnthropic might not expose `betas` directly in all versions or expects it in extra_headers.
    # We will pass it via model_kwargs.

    llm = ChatAnthropic(
        model=MODEL_NAME,
        model_kwargs={"extra_headers": {"anthropic-beta": "computer-use-2024-10-22"}}
    )

    tools = [computer_tool, bash_tool, edit_tool]

    system_prompt = """You are an agent capable of using a computer.
You have access to tools that simulate computer interaction:
- computer_tool: for keyboard and mouse control.
- bash_tool: for running shell commands.
- edit_tool: for editing files.

Since this is a demo environment, these tools are MOCKED and will only return logs of what they would do.
Assume you are on a Linux Ubuntu desktop.
"""

    return create_react_agent(llm, tools, prompt=system_prompt)

# --- Entry Point ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Take a screenshot of the desktop and then list files in the current directory."

    print(f"Processing query: {user_query}")
    agent = create_computer_use_agent()

    # Run the agent
    response = agent.invoke({"messages": [HumanMessage(content=user_query)]})

    print("\n--- Response ---")
    for message in response["messages"]:
        if message.type == "ai":
             print(f"AI: {message.content}")
