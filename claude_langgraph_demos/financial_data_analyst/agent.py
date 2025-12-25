import json
from typing import Annotated, TypedDict, List, Optional, Dict, Any, Union
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# --- Tools ---

@tool
def generate_graph_data(
    chartType: str,
    config: Dict[str, Any],
    data: List[Dict[str, Any]],
    chartConfig: Dict[str, Any]
):
    """
    Generate structured JSON data for creating financial charts and graphs.

    Args:
        chartType: The type of chart to generate. Allowed values: "bar", "multiBar", "line", "pie", "area", "stackedArea".
        config: Configuration for the chart (title, description, trend, footer, totalLabel, xAxisKey).
        data: The actual data points for the chart.
        chartConfig: Configuration for chart labels and stacking.
    """
    # In a real app, this might store data or do some processing.
    # Here we just return it so the agent sees it "generated" successfully.
    return {
        "status": "success",
        "chart_data": {
            "chartType": chartType,
            "config": config,
            "data": data,
            "chartConfig": chartConfig
        }
    }

# --- State ---

class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---

def call_model(state: AgentState):
    messages = state["messages"]

    # System prompt
    system_prompt = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using generate_graph_data tool:

Here are the chart types available and their ideal use cases:

1. LINE CHARTS ("line") - Time series data showing trends
2. BAR CHARTS ("bar") - Single metric comparisons
3. MULTI-BAR CHARTS ("multiBar") - Multiple metrics comparison
4. AREA CHARTS ("area") - Volume or quantity over time
5. STACKED AREA CHARTS ("stackedArea") - Component breakdowns over time
6. PIE CHARTS ("pie") - Distribution analysis

When generating visualizations:
1. Structure data correctly based on the chart type
2. Use descriptive titles and clear descriptions
3. Include trend information when relevant (percentage and direction)
4. Add contextual footer notes
5. Use proper data keys that reflect the actual metrics

Always:
- Generate real, contextually appropriate data
- Use proper financial formatting
- Include relevant trends and insights
- Structure data exactly as needed for the chosen chart type
- Choose the most appropriate visualization for the data

Focus on clear financial insights and let the visualization enhance understanding."""

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    llm_with_tools = llm.bind_tools([generate_graph_data])

    # Ensure system prompt is first
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
tool_node = ToolNode([generate_graph_data])
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    print("Financial Data Analyst (Type 'quit' to exit)")
    import sys

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
                elif key == "tools":
                    # Tool output is internal, but we can inspect if needed
                    pass
