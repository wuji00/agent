
import os
import sys
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

# Check for required computer use header/beta
# Memory: "Implementations using Anthropic's Computer Use features via `ChatAnthropic` require the `betas` parameter to include `computer-use-2024-10-22`."

# Mock tools for Computer Use
# Memory: "Computer Use capabilities should be demonstrated using mock tools (logging actions without execution) in environments where a real GUI is unavailable."

@tool
def computer_mouse_move(x: int, y: int):
    """Moves the mouse cursor to the specified (x, y) coordinates."""
    print(f"[MOCK] Mouse moved to ({x}, {y})")
    return f"Moved mouse to ({x}, {y})"

@tool
def computer_left_click():
    """Performs a left mouse click at the current cursor position."""
    print(f"[MOCK] Left click")
    return "Left clicked"

@tool
def computer_type(text: str):
    """Types the specified text."""
    print(f"[MOCK] Typed text: '{text}'")
    return f"Typed '{text}'"

@tool
def computer_screenshot():
    """Takes a screenshot of the current screen."""
    print(f"[MOCK] Screenshot taken")
    # In a real scenario, this would return a base64 image.
    return "Screenshot taken (mock)"

tools = [computer_mouse_move, computer_left_click, computer_type, computer_screenshot]

class AgentState(TypedDict):
    messages: List[BaseMessage]

# Initialize the model with the beta flag
# Note: In a real "Computer Use" scenario, Anthropic models have a specific `computer` tool definition.
# When using ChatAnthropic, we might need to pass `model_kwargs` or configure it specifically if we were using the *actual* computer use API.
# However, since we are mocking the tools and the prompt asks for "implementing these four demos using langchain",
# and standard tool calling works with Claude, we will use standard tool calling with the mocks.
# BUT, to respect the memory about the beta flag, I will include it.

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022", # Computer use model
    temperature=0,
    model_kwargs={
        "betas": ["computer-use-2024-10-22"]
    }
)

llm_with_tools = llm.bind_tools(tools)

def assistant(state: AgentState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

if __name__ == "__main__":
    print("Computer Use Agent initialized (Mock Mode).")
    print("Try commands like: 'Move mouse to 100, 200 and click' or 'Type hello world'.")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["q", "quit", "exit"]:
                break

            initial_state = {"messages": [HumanMessage(content=user_input)]}

            print("Assistant: ", end="", flush=True)
            for event in graph.stream(initial_state):
                for key, value in event.items():
                    if "messages" in value:
                        last_msg = value["messages"][-1]
                        if isinstance(last_msg, AIMessage):
                            if last_msg.tool_calls:
                                for tc in last_msg.tool_calls:
                                    print(f"\n[Calling tool: {tc['name']}]")
                            elif last_msg.content:
                                print(last_msg.content)
            print()

        except KeyboardInterrupt:
            break
