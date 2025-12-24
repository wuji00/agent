from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Mock Tools for Browser Use
# The reference implementation uses Playwright. We will mock the actions.

class BrowserToolInput(BaseModel):
    action: str = Field(..., description="Action: mouse_click, keyboard_type, navigate, screenshot")
    url: Optional[str] = None
    coordinate: Optional[List[int]] = None
    text: Optional[str] = None

@tool("browser_tool", args_schema=BrowserToolInput)
def browser_tool(action: str, url: Optional[str] = None, coordinate: Optional[List[int]] = None, text: Optional[str] = None):
    """Interact with a web browser."""
    print(f"** MOCK BROWSER TOOL ** Action: {action}, URL: {url}, Coords: {coordinate}, Text: {text}")
    return "Browser action executed (mock)."

# State
class BrowserAgentState(TypedDict):
    messages: List[BaseMessage]

# Graph
def agent_node(state: BrowserAgentState):
    model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
    model_with_tools = model.bind_tools([browser_tool])
    return {"messages": [model_with_tools.invoke(state["messages"])]}

def should_continue(state: BrowserAgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

from langgraph.prebuilt import ToolNode

workflow = StateGraph(BrowserAgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode([browser_tool]))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

app = workflow.compile()

def run_browser_agent(task: str):
    print(f"User: {task}")
    initial_state = {"messages": [HumanMessage(content=task)]}
    for event in app.stream(initial_state):
        for key, value in event.items():
            print(f"Node: {key}")
            if "messages" in value:
                msg = value["messages"][-1]
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    print(f"Tool Call: {msg.tool_calls[0]['name']}")

if __name__ == "__main__":
    run_browser_agent("Go to google.com and search for 'LangChain'.")
