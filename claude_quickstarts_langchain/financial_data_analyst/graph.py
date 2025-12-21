import json
from typing import Annotated, TypedDict, List, Optional, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# --- Tool Definition ---
# We define the tool schema using Pydantic, but for the @tool decorator we can also use type hints.
# The reference uses a JSON schema. LangChain tools can accept arbitrary dicts if typed as such.

@tool
def generate_graph_data(chartType: str, config: dict, data: List[dict], chartConfig: dict):
    """
    Generate structured JSON data for creating financial charts and graphs.

    Args:
        chartType: The type of chart to generate (bar, multiBar, line, pie, area, stackedArea).
        config: Configuration for the chart (title, description, etc.).
        data: The data points for the chart.
        chartConfig: Configuration for the data series (labels, colors).
    """
    # In this demo, we just return the data as is, effectively validating it was generated.
    return {
        "chartType": chartType,
        "config": config,
        "data": data,
        "chartConfig": chartConfig
    }

# --- System Prompt ---
SYSTEM_PROMPT = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using generate_graph_data tool:

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

# --- State ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# --- Nodes ---
def call_model(state: AgentState):
    messages = state["messages"]

    # Use a powerful model for data analysis
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.7)
    llm_with_tools = llm.bind_tools([generate_graph_data])

    # Add system prompt
    prompt_messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(prompt_messages)
    return {"messages": [response]}

tool_node = ToolNode([generate_graph_data])

# --- Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
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
