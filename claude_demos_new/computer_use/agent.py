import os
import sys
import base64
from typing import Annotated, TypedDict, List, Dict, Any, Union, Optional, Literal
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"
BETA_FLAG = "computer-use-2024-10-22"

# --- Mock Computer Tool ---
# Since we are not in a real VM with xdotool and display, we mock the tool to return success or a static image.

@tool
def computer_tool(
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"],
    text: Optional[str] = None,
    coordinate: Optional[List[int]] = None,
    **kwargs
):
    """
    Use a computer.
    Action strings: "key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position".
    """
    print(f"DEBUG: computer_tool called with action={action}, text={text}, coordinate={coordinate}")

    if action == "screenshot":
        # Return a 1x1 pixel base64 image (black)
        # In a real scenario this would be the screenshot
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            }
        }

    if action == "cursor_position":
        return "X=100,Y=200"

    return "Action executed successfully."

@tool
def bash_tool(command: str):
    """
    Run a bash command.
    """
    print(f"DEBUG: bash_tool called with command={command}")
    return f"Mock output for: {command}"

@tool
def edit_tool(
    command: Literal["view", "create", "str_replace", "insert", "undo_edit"],
    path: str,
    file_text: Optional[str] = None,
    view_range: Optional[List[int]] = None,
    old_str: Optional[str] = None,
    new_str: Optional[str] = None,
    insert_line: Optional[int] = None
):
    """
    Edit a file.
    """
    print(f"DEBUG: edit_tool called with command={command}, path={path}")
    return "Edit action executed successfully."

tools = [computer_tool, bash_tool, edit_tool]

# --- System Prompt ---
SYSTEM_PROMPT = """You are a computer use agent. You can control a computer to accomplish tasks.
You have access to tools: computer_tool, bash_tool, edit_tool.
The environment is Linux.
"""

# --- Agent Construction ---
def create_computer_use_agent():
    # We need to pass the beta header
    llm = ChatAnthropic(
        model=MODEL_NAME,
        temperature=0.7,
        model_kwargs={"extra_headers": {"anthropic-beta": BETA_FLAG}}
    )

    # create_react_agent automatically handles tool calling and execution
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    return agent

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Take a screenshot of the screen."

    print(f"User Query: {user_query}")

    agent = create_computer_use_agent()

    try:
        result = agent.invoke({"messages": [HumanMessage(content=user_query)]})

        print("\n--- Final Messages ---")
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                if msg.tool_calls:
                     print(f"Agent used tool: {msg.tool_calls[0]['name']}")
                else:
                     print(f"Agent: {msg.content}")
            elif isinstance(msg, ToolMessage):
                print(f"Tool Output: [Result from {msg.name}]")
    except Exception as e:
        print(f"Error: {e}")
