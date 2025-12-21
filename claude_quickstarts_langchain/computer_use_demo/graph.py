import os
from typing import Annotated, TypedDict, List, Literal, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# Mock Computer Tool
class ComputerToolInput(BaseModel):
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"]
    coordinate: Optional[List[int]] = None
    text: Optional[str] = None

@tool("computer", args_schema=ComputerToolInput)
def computer_tool(action: str, coordinate: Optional[List[int]] = None, text: Optional[str] = None):
    """
    Use a computer.
    actions:
    - key: Press a key or key-combination.
    - type: Type a string of text.
    - mouse_move: Move cursor to coordinate (x, y).
    - left_click: Click the left mouse button.
    - left_click_drag: Click and drag.
    - right_click: Click the right mouse button.
    - middle_click: Click the middle mouse button.
    - double_click: Double click.
    - screenshot: Take a screenshot of the screen.
    - cursor_position: Get the current cursor position.
    """
    output = f"Action: {action}"
    if coordinate:
        output += f", Coordinate: {coordinate}"
    if text:
        output += f", Text: {text}"

    return output

@tool("bash")
def bash_tool(command: str):
    """
    Run a bash command.
    """
    return f"Executed: {command}"

@tool("str_replace_editor")
def editor_tool(command: str, path: str, file_text: Optional[str] = None, view_range: Optional[List[int]] = None, old_str: Optional[str] = None, new_str: Optional[str] = None):
    """
    View or edit files.
    commands: view, create, str_replace, insert, undo_edit
    """
    return f"Editor Action: {command} on {path}"

tools = [computer_tool, bash_tool, editor_tool]
tool_node = ToolNode(tools)

# System Prompt
SYSTEM_PROMPT = """<SYSTEM_CAPABILITY>
* You are utilising an Ubuntu virtual machine with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.
* When using your computer function calls, they take a while to run and send back to you.
* The current date is {datetime.today().strftime("%A, %B %-d, %Y")}.
</SYSTEM_CAPABILITY>

<IMPORTANT>
* When using Firefox, if a startup wizard appears, IGNORE IT.
* If the item you are looking at is a pdf, determine the URL, use curl to download the pdf, install and use pdftotext.
</IMPORTANT>"""

# State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Node
def agent_node(state: AgentState):
    messages = state["messages"]

    # We use the computer use model and beta header
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.0,
        max_tokens=4096,
        model_kwargs={
            "extra_headers": {
                "anthropic-beta": "computer-use-2024-10-22"
            }
        }
    )

    llm_with_tools = llm.bind_tools(tools)

    # Prepend system prompt
    # Note: We should ideally replace {datetime} in system prompt
    from datetime import datetime
    formatted_system = SYSTEM_PROMPT.replace('{datetime.today().strftime("%A, %B %-d, %Y")}', datetime.today().strftime("%A, %B %-d, %Y"))

    prompt_messages = [SystemMessage(content=formatted_system)] + messages

    response = llm_with_tools.invoke(prompt_messages)
    return {"messages": [response]}

# Graph
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
