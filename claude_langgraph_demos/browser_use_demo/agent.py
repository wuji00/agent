"""
Browser Use Demo (Mock)
=======================

A demonstration of browser automation using mock tools.
"""

from typing import Annotated, TypedDict, List, Literal, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# --- Mock Tools ---

@tool
def navigate_browser(url: str):
    """
    Navigate the browser to a specific URL.
    """
    print(f"[MOCK TOOL] Navigating to: {url}")
    return f"Navigated to {url}. Page loaded."

@tool
def click_element(selector: str):
    """
    Click an element on the page identified by a CSS selector.
    """
    print(f"[MOCK TOOL] Clicking element: {selector}")
    return f"Clicked {selector}."

@tool
def type_text(selector: str, text: str):
    """
    Type text into an input field identified by a CSS selector.
    """
    print(f"[MOCK TOOL] Typing '{text}' into {selector}")
    return f"Typed '{text}' into {selector}."

@tool
def read_page_content():
    """
    Read the text content of the current page.
    """
    print("[MOCK TOOL] Reading page content")
    return "This is the content of the page. It contains a form with a username and password field."

# --- State ---

class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---

def call_model(state: AgentState):
    messages = state["messages"]

    system_prompt = """You are a browser automation agent. You can navigate the web, click elements, type text, and read content.
    Since this is a demo, you are operating in a simulated environment where tools just log their actions.

    Your goal is to help the user perform tasks on the web.
    """

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    llm_with_tools = llm.bind_tools([navigate_browser, click_element, type_text, read_page_content])

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
tool_node = ToolNode([navigate_browser, click_element, type_text, read_page_content])
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    print("Browser Use Demo (Mock) - Type 'quit' to exit")
    messages = []
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break

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
