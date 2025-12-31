import json
import os
import sys
from typing import Annotated, TypedDict, List, Dict, Any, Union, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Tool Definition ---
@tool
def generate_graph_data(
    chartType: str,
    config: Dict[str, Any],
    data: List[Dict[str, Any]],
    chartConfig: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate structured JSON data for creating financial charts and graphs.

    Args:
        chartType: The type of chart to generate. Allowed values: "bar", "multiBar", "line", "pie", "area", "stackedArea".
        config: Configuration object containing title, description, trend (percentage, direction), footer, totalLabel, xAxisKey.
        data: Array of data points.
        chartConfig: Configuration for chart labels and stacking.

    Returns:
        The input data structured for visualization (simulated).
    """
    # In a real app, this might do some validation or transformation.
    # Here we just echo back the structured data which the frontend would use to render.
    return {
        "chartType": chartType,
        "config": config,
        "data": data,
        "chartConfig": chartConfig
    }

tools = [generate_graph_data]

# --- State Definition ---
class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- System Prompt ---
SYSTEM_PROMPT = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using the generate_graph_data tool.

Here are the chart types available and their ideal use cases:
1. LINE CHARTS ("line"): Time series data showing trends.
2. BAR CHARTS ("bar"): Single metric comparisons.
3. MULTI-BAR CHARTS ("multiBar"): Multiple metrics comparison.
4. AREA CHARTS ("area"): Volume or quantity over time.
5. STACKED AREA CHARTS ("stackedArea"): Component breakdowns over time.
6. PIE CHARTS ("pie"): Distribution analysis.

When generating visualizations:
1. Structure data correctly based on the chart type.
2. Use descriptive titles and clear descriptions.
3. Include trend information when relevant.
4. Add contextual footer notes.
5. Use proper data keys.

Always generate real, contextually appropriate data (simulated for this demo if needed) and use proper financial formatting.
NEVER SAY you are using the generate_graph_data tool, just execute it when needed.
"""

# --- Agent Construction ---
def create_financial_analyst():
    llm = ChatAnthropic(model=MODEL_NAME, temperature=0.7)
    # create_react_agent automatically handles tool calling and execution
    # In recent versions, state_modifier might be named differently or we can pass the system message in prompt
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    return agent

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Show me a comparison of Apple and Microsoft revenue for the last 4 quarters."

    print(f"User Query: {user_query}")

    agent = create_financial_analyst()

    # We use a simple in-memory saver for the graph state if needed, but create_react_agent handles it.
    # invoke returns the final state
    result = agent.invoke({"messages": [HumanMessage(content=user_query)]})

    print("\n--- Final Messages ---")
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            if msg.tool_calls:
                 print(f"Agent used tool: {msg.tool_calls[0]['name']}")
                 # In a real scenario, we might print the args nicely
                 # print(json.dumps(msg.tool_calls[0]['args'], indent=2))
            else:
                 print(f"Agent: {msg.content}")
        elif isinstance(msg, ToolMessage):
            print(f"Tool Output: [Data generated for {msg.name}]")
