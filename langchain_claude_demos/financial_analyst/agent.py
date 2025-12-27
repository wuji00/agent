
import json
import random
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

# Mock financial data tool
@tool
def get_stock_price(symbol: str) -> str:
    """Get the current stock price and historical data for a given symbol."""
    print(f"DEBUG: Fetching data for {symbol}")
    base_price = random.uniform(100, 200)
    history = []
    for i in range(30):
        price = base_price + random.uniform(-10, 10)
        history.append({"day": i, "price": round(price, 2)})

    data = {
        "symbol": symbol.upper(),
        "current_price": round(base_price, 2),
        "history": history
    }
    return json.dumps(data)

# State definition
class AgentState(TypedDict):
    messages: List[BaseMessage]

# Model setup
# Memory instruction: "Financial Data Analyst agents should utilize tools to generate structured JSON output compatible with charting libraries (e.g., Recharts) to simulate frontend visualization capabilities."
llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)

# We can tell the model to use the tool, and potentially we could have another tool for "rendering" but here the model's text response will likely explain the data.
# However, if we want to simulate frontend visualization, maybe we want a tool that "generates a chart config".

@tool
def generate_chart_config(data_json: str, chart_type: str = "line") -> str:
    """Generates a JSON configuration for a charting library (like Recharts) based on the provided data."""
    try:
        data = json.loads(data_json)
        # Simplify for demo
        chart_config = {
            "type": chart_type,
            "data": data.get("history", []),
            "xKey": "day",
            "yKey": "price",
            "title": f"Stock Price History for {data.get('symbol', 'Unknown')}"
        }
        return json.dumps(chart_config, indent=2)
    except Exception as e:
        return f"Error generating chart: {e}"

tools = [get_stock_price, generate_chart_config]
llm_with_tools = llm.bind_tools(tools)

# Nodes
def assistant(state: AgentState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Graph
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

if __name__ == "__main__":
    print("Financial Analyst Agent initialized. Ask for stock prices (e.g., 'Analyze AAPL stock').")

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
                            # Print tool calls if present to show what's happening
                            if last_msg.tool_calls:
                                for tc in last_msg.tool_calls:
                                    print(f"\n[Calling tool: {tc['name']}]")
                            elif last_msg.content:
                                print(last_msg.content)
            print()

        except KeyboardInterrupt:
            break
