import os
import json
import base64
from typing import List, Dict, Any, Optional
from enum import Enum

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration

# --- Configuration ---
# Use the model that supports computer use
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Mock Tools for Computer Use ---
class Action(str, Enum):
    key = "key"
    type = "type"
    mouse_move = "mouse_move"
    left_click = "left_click"
    left_click_drag = "left_click_drag"
    right_click = "right_click"
    middle_click = "middle_click"
    double_click = "double_click"
    screenshot = "screenshot"
    cursor_position = "cursor_position"

@tool
def computer(action: str, text: Optional[str] = None, coordinate: Optional[List[int]] = None, **kwargs):
    """
    Use a computer.
    actions:
    - key: Press a key or key-combination.
    - type: Type a string of text.
    - mouse_move: Move the cursor to a coordinate (x, y).
    - left_click: Click the left mouse button.
    - left_click_drag: Click and drag the cursor to a coordinate (x, y).
    - right_click: Click the right mouse button.
    - middle_click: Click the middle mouse button.
    - double_click: Double click the left mouse button.
    - screenshot: Take a screenshot of the screen.
    - cursor_position: Get the current cursor position.
    """
    print(f"[Computer Tool] Action: {action}, Text: {text}, Coords: {coordinate}")

    if action == "screenshot":
        # Return a dummy base64 image
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
            }
        }
    if action == "cursor_position":
        return {"x": 500, "y": 300}

    return "Action completed successfully."

@tool
def bash(command: str, restart: bool = False, **kwargs):
    """
    Run a bash command.
    """
    print(f"[Bash Tool] Command: {command}")
    return f"Executed: {command}\nOutput: (Mock output)"

@tool
def str_replace_editor(command: str, path: str, file_text: Optional[str] = None, view_range: Optional[List[int]] = None, old_str: Optional[str] = None, new_str: Optional[str] = None, **kwargs):
    """
    View or edit files.
    """
    print(f"[Editor Tool] Command: {command}, Path: {path}")
    return "File edited/viewed successfully."

# --- Agent Setup ---

system_prompt = """You have access to a computer with a screen resolution of 1024x768.
You can use the 'computer' tool to interact with the screen, keyboard, and mouse.
You can use the 'bash' tool to run commands.
You can use the 'str_replace_editor' tool to edit files.
"""

def get_agent(mock_llm=None):
    if mock_llm:
        llm = mock_llm
    else:
        # Important: 'betas' parameter is required for computer use
        llm = ChatAnthropic(
            model=MODEL_NAME,
            temperature=0.5,
            model_kwargs={"betas": ["computer-use-2024-10-22"]}
        )

    tools = [computer, bash, str_replace_editor]

    # Use simple create_react_agent without modifier arguments that are failing in this environment's version
    agent = create_react_agent(llm, tools)
    return agent

# --- Mock LLM ---
class MockComputerChatModel(BaseChatModel):
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs) -> ChatResult:
        last_msg = messages[-1]

        if isinstance(last_msg, ToolMessage):
             return ChatResult(generations=[ChatGeneration(message=AIMessage(content="I have taken a screenshot."))])

        # Mock a tool call to take a screenshot
        tool_call = {
            "name": "computer",
            "args": {
                "action": "screenshot"
            },
            "id": "call_mock_comp_123"
        }

        msg = AIMessage(content="I will look at the screen.", tool_calls=[tool_call])
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self) -> str:
        return "mock"

    def bind_tools(self, tools, **kwargs):
        return self

# --- Main Execution ---

if __name__ == "__main__":
    # Check for API Key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    use_mock = not api_key or api_key == "dummy_key_for_now_since_i_cant_set_real_one"

    if use_mock:
        print("⚠️  No valid ANTHROPIC_API_KEY found. Using Mock LLM for demonstration.")
        llm = MockComputerChatModel()
    else:
        llm = None

    agent = get_agent(mock_llm=llm)

    queries = [
        "Take a screenshot of the desktop.",
    ]

    print("--- Starting Computer Use Demo ---")

    for q in queries:
        print(f"\nUser Query: {q}")
        # Manually prepend system prompt
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=q)
        ]
        inputs = {"messages": messages}

        for event in agent.stream(inputs, stream_mode="values"):
            message = event["messages"][-1]
            if isinstance(message, AIMessage):
                if message.tool_calls:
                    print(f"Tool Call: {message.tool_calls[0]['name']}")
                elif message.content:
                    print(f"Agent: {message.content}")
            elif isinstance(message, ToolMessage):
                print("Tool Output Received")
