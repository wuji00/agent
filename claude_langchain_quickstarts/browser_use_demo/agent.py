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

class BrowserToolInput(BaseModel):
    action: Literal["navigate", "read_page", "get_page_text", "find", "form_input", "scroll_to", "execute_js",
                    "left_click", "right_click", "middle_click", "double_click", "triple_click", "hover",
                    "left_click_drag", "left_mouse_down", "left_mouse_up", "type", "key", "hold_key",
                    "screenshot", "scroll", "zoom", "wait"]
    url: Optional[str] = None
    ref: Optional[int] = None
    text: Optional[str] = None
    value: Optional[str] = None
    coordinate: Optional[List[int]] = None
    # ... add other fields as needed

@tool("browser", args_schema=BrowserToolInput)
def browser_tool(action: str, **kwargs):
    """Interact with a web browser."""
    print(f"[Mock Browser] Action: {action}, Args: {kwargs}")
    if action == "read_page":
        return """
        <html>
        <body>
        <h1>Welcome to Example.com</h1>
        <a href="/login" ref="1">Login</a>
        <input type="text" ref="2" placeholder="Search">
        </body>
        </html>
        """
    if action == "screenshot":
        return {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="}}
    return "Action completed (mock)"

tools = [browser_tool]
tool_node = ToolNode(tools)

# --- State ---
class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---
def agent_node(state: AgentState):
    messages = state["messages"]

    system_prompt = """You are an agent capable of using a browser tool to navigate the web.
    """

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

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
        user_input = "Navigate to google.com and search for 'LangChain'."
        print(f"User: {user_input}")

        try:
            final_state = app.invoke({"messages": [HumanMessage(content=user_input)]})

            for msg in final_state["messages"]:
                if isinstance(msg, AIMessage) and msg.tool_calls:
                    print("\nTool Call Generated:")
                    print(json.dumps(msg.tool_calls[0]["args"], indent=2))
        except Exception as e:
            print(f"Error: {e}")
