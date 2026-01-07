from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Mock Tools for Computer Use (as per memory instructions)

class ComputerToolInput(BaseModel):
    action: str = Field(..., description="The action to perform: mouse_move, left_click, type, key, screenshot")
    coordinate: Optional[List[int]] = Field(None, description="[x, y] coordinates")
    text: Optional[str] = Field(None, description="Text to type")

@tool("computer", args_schema=ComputerToolInput)
def computer_tool(action: str, coordinate: Optional[List[int]] = None, text: Optional[str] = None):
    """Use a computer. Capabilities: mouse_move, left_click, type, key, screenshot."""
    # Mock implementation
    print(f"** MOCK COMPUTER TOOL ** Action: {action}, Coords: {coordinate}, Text: {text}")
    if action == "screenshot":
        return {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "MOCK_BASE64_IMAGE"}}
    return "Action executed."

class BashToolInput(BaseModel):
    command: str

@tool("bash", args_schema=BashToolInput)
def bash_tool(command: str):
    """Run a bash command."""
    print(f"** MOCK BASH TOOL ** Command: {command}")
    return "Command executed successfully (mock)."

class EditToolInput(BaseModel):
    path: str
    command: str
    file_text: Optional[str] = None
    view_range: Optional[List[int]] = None

@tool("str_replace_editor", args_schema=EditToolInput)
def edit_tool(path: str, command: str, file_text: Optional[str] = None, view_range: Optional[List[int]] = None):
    """View or edit a file."""
    print(f"** MOCK EDIT TOOL ** Path: {path}, Command: {command}")
    return "File edited (mock)."


# State
class ComputerUseState(TypedDict):
    messages: List[BaseMessage]

# Graph
def agent_node(state: ComputerUseState):
    # Enable computer use beta features if available in library, or pass as tools
    # ChatAnthropic automatically handles binding if we pass the tools,
    # but for "computer use" specifically, Anthropic API has specific beta headers and tool definitions.
    # LangChain's ChatAnthropic supports `model_kwargs` for betas.

    model = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        model_kwargs={"betas": ["computer-use-2024-10-22"]}
    )

    # We bind our mock tools.
    # Note: Real computer use requires specific tool definitions that map to the API.
    # Since we are mocking, we just provide standard tools that LOOK like computer use tools.
    model_with_tools = model.bind_tools([computer_tool, bash_tool, edit_tool])

    return {"messages": [model_with_tools.invoke(state["messages"])]}

def should_continue(state: ComputerUseState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

from langgraph.prebuilt import ToolNode

workflow = StateGraph(ComputerUseState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode([computer_tool, bash_tool, edit_tool]))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

app = workflow.compile()

def run_computer_agent(instruction: str):
    print(f"User: {instruction}")
    initial_state = {"messages": [HumanMessage(content=instruction)]}
    for event in app.stream(initial_state):
        for key, value in event.items():
            print(f"Node: {key}")
            if "messages" in value:
                msg = value["messages"][-1]
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    print(f"Tool Call: {msg.tool_calls[0]['name']}")

if __name__ == "__main__":
    run_computer_agent("Open the calculator and calculate 55 + 10.")
