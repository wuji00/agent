import platform
from typing import Annotated, TypedDict, List, Literal, Optional, Union, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
import asyncio

# --- Mock Tools ---
# Since we are not in a full desktop environment (or at least one we can easily control via X11 in this sandbox properly),
# we will mock the computer use tools to demonstrate the agent loop.
# The memory says: "Computer Use capabilities should be demonstrated using mock tools (logging actions without execution) in environments where a real GUI is unavailable."

@tool
def computer(
    action: Literal["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "screenshot", "cursor_position"],
    text: Optional[str] = None,
    coordinate: Optional[List[int]] = None
):
    """
    Control the computer (mouse and keyboard).

    actions:
    - key: Press a key or key combination.
    - type: Type a string of text.
    - mouse_move: Move cursor to coordinate (x, y).
    - left_click, right_click, etc.: Click mouse buttons.
    - screenshot: Take a screenshot.
    - cursor_position: Get current cursor position.
    """
    print(f"[MOCK TOOL] computer: action={action}, text={text}, coordinate={coordinate}")

    if action == "screenshot":
        # Return a blank or dummy base64 image if real screenshot impossible
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGNiAAAABgADNjd8qAAAAABJRU5ErkJggg==" # 1x1 pixel
            }
        }
    elif action == "cursor_position":
        return {"x": 100, "y": 100}

    return "Action executed successfully."

@tool
def bash(command: str):
    """
    Run a bash command.
    """
    print(f"[MOCK TOOL] bash: {command}")
    return "Command executed successfully (mock)."

@tool
def str_replace_editor(
    command: Literal["view", "create", "str_replace", "insert", "undo_edit"],
    path: str,
    file_text: Optional[str] = None,
    view_range: Optional[List[int]] = None,
    old_str: Optional[str] = None,
    new_str: Optional[str] = None
):
    """
    View or edit files.
    """
    print(f"[MOCK TOOL] editor: {command} on {path}")
    return "Editor action executed successfully (mock)."

# --- State ---

class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---

def call_model(state: AgentState):
    messages = state["messages"]

    system_prompt = f"""<SYSTEM_CAPABILITY>
* You are utilizing an Ubuntu virtual machine using {platform.machine()} architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.
</SYSTEM_CAPABILITY>

<IMPORTANT>
* This is a MOCK environment. The tools will log actions but not actually control a desktop.
</IMPORTANT>
"""

    # We need to enable the "computer-use-2024-10-22" beta.
    # ChatAnthropic supports 'model_kwargs' which can include 'extra_headers' or 'betas'??
    # Actually, ChatAnthropic has a `model` parameter, and we can pass `extra_body` or similar.
    # But `langchain-anthropic` handles beta headers if we use the right model?
    # No, we usually need to specify it.

    # In langchain-anthropic, we can pass `model_kwargs`.

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.0,
        model_kwargs={
            "extra_headers": {
                "anthropic-beta": "computer-use-2024-10-22"
            }
        }
    )

    # Bind tools. Note: For computer use, the structure is specific.
    # However, since we defined standard tools, we can just bind them.
    # But wait, the 'computer' tool has a special shape in the API.
    # The `computer` tool definition we wrote uses `type`, `coordinate` etc.
    # If we use `bind_tools`, LangChain converts Python function to tool schema.
    # This might differ slightly from the official "computer" tool spec Anthropic expects.
    # But for a demo using LangChain, using standard tool calling is the way to go unless we manually construct the tool definition.
    # The prompt caching and specific image handling might be complex to replicate exactly in standard LangGraph without more custom logic.
    # For this demo, we use standard LangChain tool binding which maps to "tool_use".

    llm_with_tools = llm.bind_tools([computer, bash, str_replace_editor])

    from langchain_core.messages import SystemMessage
    prompt_messages = [SystemMessage(content=system_prompt)] + messages

    response = llm_with_tools.invoke(prompt_messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# --- Graph ---

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
tool_node = ToolNode([computer, bash, str_replace_editor])
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    print("Computer Use Demo (Mock) - Type 'quit' to exit")
    messages = []
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        messages.append(HumanMessage(content=user_input))
        state = {"messages": messages}

        print("... thinking ...")
        try:
            for event in app.stream(state):
                for key, value in event.items():
                    if key == "agent":
                        msg = value["messages"][0]
                        if msg.tool_calls:
                            print(f"Tool Call: {msg.tool_calls[0]['name']}")
                        else:
                            print(f"Assistant: {msg.content}")
                            messages.append(msg)
        except Exception as e:
            print(f"Error: {e}")
