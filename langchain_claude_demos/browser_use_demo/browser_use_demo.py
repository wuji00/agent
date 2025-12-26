import os
import json
from typing import List, Dict, Any, Optional
from enum import Enum

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Mock Tools for Browser Use ---
# Usually these wrap Playwright. We will mock them.

@tool
def navigate(url: str, **kwargs):
    """Navigate to a URL."""
    print(f"[Browser Tool] Navigate to: {url}")
    return f"Navigated to {url}. Page title: 'Mock Page Title'"

@tool
def click(selector: str, **kwargs):
    """Click an element."""
    print(f"[Browser Tool] Click: {selector}")
    return "Clicked element."

@tool
def type_text(selector: str, text: str, **kwargs):
    """Type text into an element."""
    print(f"[Browser Tool] Type in {selector}: {text}")
    return "Typed text."

@tool
def scroll(direction: str, **kwargs):
    """Scroll the page."""
    print(f"[Browser Tool] Scroll: {direction}")
    return "Scrolled."

# --- Agent Setup ---

system_prompt = """You are a browser automation agent. You can use tools to navigate the web and interact with pages.
Available tools: navigate, click, type_text, scroll.
"""

def get_agent(mock_llm=None):
    if mock_llm:
        llm = mock_llm
    else:
        llm = ChatAnthropic(
            model=MODEL_NAME,
            temperature=0.5,
        )

    tools = [navigate, click, type_text, scroll]

    agent = create_react_agent(llm, tools)
    return agent

# --- Mock LLM ---
class MockBrowserChatModel(BaseChatModel):
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs) -> ChatResult:
        last_msg = messages[-1]

        if isinstance(last_msg, ToolMessage):
             return ChatResult(generations=[ChatGeneration(message=AIMessage(content="I have navigated to the website."))])

        # Mock a tool call
        tool_call = {
            "name": "navigate",
            "args": {
                "url": "https://www.anthropic.com"
            },
            "id": "call_mock_browser_123"
        }

        msg = AIMessage(content="I will go to Anthropic's website.", tool_calls=[tool_call])
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
        llm = MockBrowserChatModel()
    else:
        llm = None

    agent = get_agent(mock_llm=llm)

    queries = [
        "Go to https://www.anthropic.com",
    ]

    print("--- Starting Browser Use Demo ---")

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
