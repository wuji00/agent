import os
import json
from typing import List, Dict, Any, TypedDict, Union, Literal, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# --- Mock Tools ---

class ComputerToolInput(BaseModel):
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"]
    coordinate: Optional[List[int]] = None
    text: Optional[str] = None

@tool("computer", args_schema=ComputerToolInput)
def computer_tool(action: str, coordinate: Optional[List[int]] = None, text: Optional[str] = None):
    """Use a computer.
    action: The action to perform.
    coordinate: The coordinate to perform the action at (x, y).
    text: The text to type or key to press.
    """
    print(f"[Mock Computer] Action: {action}, Coordinate: {coordinate}, Text: {text}")
    if action == "screenshot":
        # Return a blank base64 image
        return {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="}}
    return "Action completed"

class BashToolInput(BaseModel):
    command: str

@tool("bash", args_schema=BashToolInput)
def bash_tool(command: str):
    """Run a bash command."""
    print(f"[Mock Bash] Command: {command}")
    return "Command executed successfully (mock)"

class EditToolInput(BaseModel):
    command: Literal["view", "create", "str_replace", "insert", "undo_edit"]
    path: str
    file_text: Optional[str] = None
    view_range: Optional[List[int]] = None
    old_str: Optional[str] = None
    new_str: Optional[str] = None
    insert_line: Optional[int] = None

@tool("str_replace_editor", args_schema=EditToolInput)
def edit_tool(command: str, path: str, **kwargs):
    """View, create, and edit files."""
    print(f"[Mock Edit] Command: {command}, Path: {path}, Args: {kwargs}")
    return "File operation completed (mock)"

tools = [computer_tool, bash_tool, edit_tool]
tool_node = ToolNode(tools)

# --- State ---
class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---
def agent_node(state: AgentState):
    messages = state["messages"]

    system_prompt = """<SYSTEM_CAPABILITY>
* You are utilizing an Ubuntu virtual machine using x86_64 architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon.  Note, firefox-esr is what is installed on your system.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example "(DISPLAY=:1 xterm &)". GUI apps run with bash tool will appear within your desktop environment, but they may take some time to appear. Take a screenshot to confirm it did.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file and use str_replace_based_edit_tool or `grep -n -B <lines before> -A <lines after> <query> <filename>` to confirm output.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* When using your computer function calls, they take a while to run and send back to you.  Where possible/feasible, try to chain multiple of these calls all into one function calls request.
* The current date is Tuesday, October 24, 2024.
</SYSTEM_CAPABILITY>
"""

    # We use a recent model that supports computer use
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

    llm_with_tools = llm.bind_tools(tools)

    # System prompt handling
    final_messages = [SystemMessage(content=system_prompt)] + messages

    response = llm_with_tools.invoke(final_messages)
    return {"messages": [response]}

# --- Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# --- Demo Run ---
if __name__ == "__main__":
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Please set ANTHROPIC_API_KEY env var.")
    else:
        user_input = "Take a screenshot of the desktop."
        print(f"User: {user_input}")

        try:
            final_state = app.invoke({"messages": [HumanMessage(content=user_input)]})

            for msg in final_state["messages"]:
                if isinstance(msg, AIMessage) and msg.tool_calls:
                    print("\nTool Call Generated:")
                    print(json.dumps(msg.tool_calls[0]["args"], indent=2))
        except Exception as e:
            print(f"Error: {e}")
