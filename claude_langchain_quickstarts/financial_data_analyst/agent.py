import os
import json
from typing import List, Dict, Any, TypedDict, Union, Literal, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# --- Tool Definition ---

class Trend(BaseModel):
    percentage: float
    direction: Literal["up", "down"]

class ChartConfigItem(BaseModel):
    label: str
    stacked: bool = False

class ChartConfig(BaseModel):
    title: str
    description: str
    trend: Optional[Trend] = None
    footer: Optional[str] = None
    totalLabel: Optional[str] = None
    xAxisKey: Optional[str] = None

class GenerateGraphDataInput(BaseModel):
    chartType: Literal["bar", "multiBar", "line", "pie", "area", "stackedArea"] = Field(description="The type of chart to generate")
    config: ChartConfig
    data: List[Dict[str, Any]]
    chartConfig: Dict[str, ChartConfigItem]

@tool("generate_graph_data", args_schema=GenerateGraphDataInput)
def generate_graph_data(chartType: str, config: ChartConfig, data: List[Dict[str, Any]], chartConfig: Dict[str, ChartConfigItem]):
    """Generate structured JSON data for creating financial charts and graphs."""
    # In a real app, this would return the data to the frontend to render.
    # Here we just return the structure as confirmation.
    return {
        "chartType": chartType,
        "config": config.dict(),
        "data": data,
        "chartConfig": {k: v.dict() for k, v in chartConfig.items()}
    }

# --- State ---
class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---
def agent_node(state: AgentState):
    messages = state["messages"]

    system_prompt = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using generate_graph_data tool:

Here are the chart types available and their ideal use cases:

1. LINE CHARTS ("line")
   - Time series data showing trends
   - Financial metrics over time
   - Market performance tracking

2. BAR CHARTS ("bar")
   - Single metric comparisons
   - Period-over-period analysis
   - Category performance

3. MULTI-BAR CHARTS ("multiBar")
   - Multiple metrics comparison
   - Side-by-side performance analysis
   - Cross-category insights

4. AREA CHARTS ("area")
   - Volume or quantity over time
   - Cumulative trends
   - Market size evolution

5. STACKED AREA CHARTS ("stackedArea")
   - Component breakdowns over time
   - Portfolio composition changes
   - Market share evolution

6. PIE CHARTS ("pie")
   - Distribution analysis
   - Market share breakdown
   - Portfolio allocation

When generating visualizations:
1. Structure data correctly based on the chart type
2. Use descriptive titles and clear descriptions
3. Include trend information when relevant (percentage and direction)
4. Add contextual footer notes
5. Use proper data keys that reflect the actual metrics

Data Structure Examples:

For Time-Series (Line/Bar/Area):
{
  data: [
    { period: "Q1 2024", revenue: 1250000 },
    { period: "Q2 2024", revenue: 1450000 }
  ],
  config: {
    xAxisKey: "period",
    title: "Quarterly Revenue",
    description: "Revenue growth over time"
  },
  chartConfig: {
    revenue: { label: "Revenue ($)" }
  }
}

For Comparisons (MultiBar):
{
  data: [
    { category: "Product A", sales: 450000, costs: 280000 },
    { category: "Product B", sales: 650000, costs: 420000 }
  ],
  config: {
    xAxisKey: "category",
    title: "Product Performance",
    description: "Sales vs Costs by Product"
  },
  chartConfig: {
    sales: { label: "Sales ($)" },
    costs: { label: "Costs ($)" }
  }
}

For Distributions (Pie):
{
  data: [
    { segment: "Equities", value: 5500000 },
    { segment: "Bonds", value: 3200000 }
  ],
  config: {
    xAxisKey: "segment",
    title: "Portfolio Allocation",
    description: "Current investment distribution",
    totalLabel: "Total Assets"
  },
  chartConfig: {
    equities: { label: "Equities" },
    bonds: { label: "Bonds" }
  }
}

Always:
- Generate real, contextually appropriate data
- Use proper financial formatting
- Include relevant trends and insights
- Structure data exactly as needed for the chosen chart type
- Choose the most appropriate visualization for the data

Never:
- Use placeholder or static data
- Announce the tool usage
- Include technical implementation details in responses
- NEVER SAY you are using the generate_graph_data tool, just execute it when needed.

Focus on clear financial insights and let the visualization enhance understanding."""

    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.7)
    llm_with_tools = llm.bind_tools([generate_graph_data])

    # Ensure system prompt is first
    final_messages = [SystemMessage(content=system_prompt)] + messages

    response = llm_with_tools.invoke(final_messages)
    return {"messages": [response]}

# We use prebuilt ToolNode
tool_node = ToolNode([generate_graph_data])

# --- Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# --- Demo Run ---
if __name__ == "__main__":
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Please set ANTHROPIC_API_KEY env var.")
    else:
        user_input = "Show me a pie chart of my portfolio: 60% Stocks, 30% Bonds, 10% Cash."
        print(f"User: {user_input}")

        # Stream the output
        try:
            final_state = app.invoke({"messages": [HumanMessage(content=user_input)]})

            # Check for tool calls in history
            found_tool = False
            for msg in final_state["messages"]:
                if isinstance(msg, AIMessage) and msg.tool_calls:
                    print("\nTool Call Generated:")
                    print(json.dumps(msg.tool_calls[0]["args"], indent=2))
                    found_tool = True

            if not found_tool:
                print("No tool call generated.")
                print(final_state["messages"][-1].content)
        except Exception as e:
            print(f"Error: {e}")
