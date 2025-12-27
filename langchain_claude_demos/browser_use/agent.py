
import os
import sys
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

# Mock tools for Browser Use
# Memory: "Browser automation demos should use mock tools to log actions without execution when running in environments without a GUI/browser."

@tool
def navigate_to_url(url: str):
    """Navigates the browser to the specified URL."""
    print(f"[MOCK] Navigating to {url}")
    return f"Navigated to {url}"

@tool
def click_element(selector: str):
    """Clicks an element on the page identified by the CSS selector."""
    print(f"[MOCK] Clicking element: {selector}")
    return f"Clicked {selector}"

@tool
def fill_input(selector: str, value: str):
    """Fills an input field identified by the CSS selector with the given value."""
    print(f"[MOCK] Filling {selector} with '{value}'")
    return f"Filled {selector} with '{value}'"

@tool
def extract_text(selector: str):
    """Extracts text from an element identified by the CSS selector."""
    print(f"[MOCK] Extracting text from {selector}")
    return f"Text content of {selector} (mock)"

tools = [navigate_to_url, click_element, fill_input, extract_text]

class AgentState(TypedDict):
    messages: List[BaseMessage]

# Using a standard Claude model
llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
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
    print("Browser Use Agent initialized (Mock Mode).")
    print("Try commands like: 'Go to google.com and search for langchain'.")

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
