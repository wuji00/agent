import platform
import os
import sys
from typing import Annotated, TypedDict, List, Literal, Optional, Union, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
import asyncio

# --- Mock Tools ---

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

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.0,
        model_kwargs={
            "extra_headers": {
                "anthropic-beta": "computer-use-2024-10-22"
            }
        }
    )

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
    from langchain_core.runnables import RunnableLambda

    # Fake LLM for testing
    class FakeLLM:
        def bind_tools(self, tools, **kwargs):
            return self

        def invoke(self, input, config=None):
             messages = input if isinstance(input, list) else input.get("messages", [])
             last_msg = messages[-1]
             if "screenshot" in last_msg.content.lower():
                 return AIMessage(content="Taking a screenshot.", tool_calls=[
                     {"name": "computer", "args": {
                         "action": "screenshot"
                     }, "id": "call_1"}
                 ])
             elif isinstance(last_msg, ToolMessage):
                 return AIMessage(content="Here is the result.")
             else:
                 return AIMessage(content="Ready.")

    # Mock ChatAnthropic for test mode
    if os.environ.get("TEST_MODE"):
        print("Running in TEST MODE")
        global ChatAnthropic
        ChatAnthropic = lambda **kwargs: FakeLLM()

    print("Computer Use Demo (Mock) - Type 'quit' to exit")
    messages = []

    # Non-interactive mode handling
    import select
    if select.select([sys.stdin,],[],[],0.0)[0]:
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                user_input = line.strip()
                if not user_input or user_input.lower() in ["quit", "exit"]:
                    break

                print(f"User: {user_input}")
                messages.append(HumanMessage(content=user_input))
                state = {"messages": messages}

                print("... thinking ...")
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
    else:
        while True:
            try:
                user_input = input("User: ")
            except EOFError:
                break
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
