import json
from typing import Annotated, TypedDict, List, Literal, Optional, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# --- Mock Tools ---

@tool
def browser_tool(
    action: Literal["navigate", "click", "type", "scroll", "screenshot", "get_html"],
    url: Optional[str] = None,
    selector: Optional[str] = None,
    text: Optional[str] = None,
    coordinate: Optional[List[int]] = None
):
    """
    Interact with a web browser.

    actions:
    - navigate: Go to a URL.
    - click: Click on an element (by selector or coordinate).
    - type: Type text into an element.
    - scroll: Scroll the page.
    - screenshot: Take a screenshot.
    - get_html: Get the HTML content.
    """
    print(f"[MOCK TOOL] browser: action={action}, url={url}, selector={selector}")

    if action == "navigate":
        return f"Navigated to {url}"
    elif action == "get_html":
        return "<html><body><h1>Mock Page</h1></body></html>"

    return "Action executed successfully."

# --- State ---

class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---

def call_model(state: AgentState):
    messages = state["messages"]

    system_prompt = """You are an agent equipped with a browser tool. You can use it to navigate the web and extract information.

    When asked to look up something, use the `browser_tool` to navigate to relevant websites."""

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.5)
    llm_with_tools = llm.bind_tools([browser_tool])

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
tool_node = ToolNode([browser_tool])
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
