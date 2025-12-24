from typing import TypedDict, List, Optional, Any, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
import json
from pydantic import BaseModel, Field

# 1. State Definition
class AnalystState(TypedDict):
    messages: List[BaseMessage]
    chart_data: Optional[dict]

# 2. Tool Definition (Pydantic models for structured output/tool call)
class ChartTrend(BaseModel):
    percentage: float
    direction: str = Field(pattern="^(up|down)$")

class ChartConfig(BaseModel):
    title: str
    description: str
    trend: Optional[ChartTrend] = None
    footer: Optional[str] = None
    totalLabel: Optional[str] = None
    xAxisKey: Optional[str] = None

class ChartDataPoint(BaseModel):
    # Flexible dict to allow any keys
    data: dict

class ChartConfigItem(BaseModel):
    label: str
    stacked: Optional[bool] = None

# We can define the tool input schema.
# LangChain's @tool decorator is easy, but for complex nested structures like in the reference,
# defining a Pydantic model for the tool input is best.

class GenerateGraphInput(BaseModel):
    chartType: str = Field(description="Type of chart: bar, multiBar, line, pie, area, stackedArea")
    config: ChartConfig
    data: List[dict]
    chartConfig: dict[str, ChartConfigItem]

@tool("generate_graph_data", args_schema=GenerateGraphInput)
def generate_graph_data(chartType: str, config: ChartConfig, data: List[dict], chartConfig: dict):
    """Generate structured JSON data for creating financial charts and graphs."""
    # In a real app, this might validate or process the data.
    # For the agent, this is the 'tool' that produces the artifact.
    # We just return the data so the agent knows it 'executed'.
    return {
        "chartType": chartType,
        "config": config.dict(),
        "data": data,
        "chartConfig": {k: v.dict() for k, v in chartConfig.items()}
    }

# 3. Graph Logic

def agent_node(state: AnalystState):
    model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.7)

    # Bind the tool
    model_with_tools = model.bind_tools([generate_graph_data])

    messages = state["messages"]
    system_prompt = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using generate_graph_data tool.
    ... (Include the full system prompt from the reference here if strictly needed, abbreviated for brevity) ...
    Use the generate_graph_data tool to create charts.
    """

    # Ensure system prompt is first
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system_prompt)] + messages

    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AnalystState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 4. Graph Construction
from langgraph.prebuilt import ToolNode

workflow = StateGraph(AnalystState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode([generate_graph_data]))

workflow.set_entry_point("agent")

workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent") # Loop back to agent to confirm or explain

app = workflow.compile()

# 5. Runnable Function
def run_analyst(query: str):
    print(f"User: {query}")
    initial_state = {"messages": [HumanMessage(content=query)]}
    # We iterate to handle the tool call loop
    final_state = None
    for event in app.stream(initial_state):
        for key, value in event.items():
            print(f"Node: {key}")
            if "messages" in value:
                msg = value["messages"][-1]
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    print(f"Tool Call: {msg.tool_calls[0]['name']}")
                    # Store chart data if found (hacky extraction for demo)
                    # In a real app, the tool output would be stored in state properly or processed by frontend

    print("Analyst finished.")

if __name__ == "__main__":
    run_analyst("Show me a line chart of Apple's revenue over the last 4 quarters: Q1 100B, Q2 110B, Q3 105B, Q4 120B.")
