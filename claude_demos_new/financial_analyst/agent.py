from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

# Define schema for the chart tool
class ChartTrend(BaseModel):
    percentage: float
    direction: Literal["up", "down"]

class ChartConfig(BaseModel):
    title: str
    description: str
    trend: Optional[ChartTrend] = None
    footer: Optional[str] = None
    totalLabel: Optional[str] = None
    xAxisKey: Optional[str] = None

class ChartConfigItem(BaseModel):
    label: str
    stacked: Optional[bool] = None
    color: Optional[str] = None

class ChartDataInput(BaseModel):
    chartType: Literal["bar", "multiBar", "line", "pie", "area", "stackedArea"] = Field(description="The type of chart to generate")
    config: ChartConfig
    data: List[Dict[str, Any]] = Field(description="The data points for the chart")
    chartConfig: Dict[str, ChartConfigItem] = Field(description="Configuration for data keys (e.g. labels)")

# Define the tool
@tool
def generate_graph_data(
    chartType: Literal["bar", "multiBar", "line", "pie", "area", "stackedArea"],
    config: ChartConfig,
    data: List[Dict[str, Any]],
    chartConfig: Dict[str, ChartConfigItem]
):
    """
    Generate structured JSON data for creating financial charts and graphs.
    Call this tool when the user asks to visualize data or when you want to present data in a chart.
    """
    # In the reference implementation, this tool doesn't actually "do" anything other than structure the output.
    # The frontend then renders it.
    # So we just return the input as the result, which acts as the "artifact".
    return {
        "chartType": chartType,
        "config": config.model_dump(),
        "data": data,
        "chartConfig": {k: v.model_dump() for k, v in chartConfig.items()}
    }

class FinancialAnalystAgent:
    def __init__(self, model_name: str = "claude-3-haiku-20240307"):
        self.llm = ChatAnthropic(model=model_name, temperature=0.7)
        self.tools = [generate_graph_data]

        system_prompt = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using generate_graph_data tool.

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

Focus on clear financial insights and let the visualization enhance understanding.
"""
        # Using prompt as per library verification (langgraph 1.0.5)
        self.agent = create_react_agent(self.llm, self.tools, prompt=system_prompt)

    def invoke(self, messages: List[Dict[str, str]]):
        return self.agent.invoke({"messages": messages})
