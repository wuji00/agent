from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from financial_analyst.tools import get_stock_price, get_stock_history, generate_graph_data

SYSTEM_PROMPT = """You are a financial data visualization expert.
Your role is to analyze financial data and create clear, meaningful visualizations using the generate_graph_data tool.
You have access to tools to fetch real market data: get_stock_price and get_stock_history.
Always use real data when asked.

When generating visualizations:
1. Structure data correctly based on the chart type.
2. Use descriptive titles and clear descriptions.
3. Call generate_graph_data to "display" the chart.

Do not output the JSON manually in text. Use the tool.
"""

def get_app():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.5)
    tools = [get_stock_price, get_stock_history, generate_graph_data]

    agent = create_react_agent(llm, tools, state_modifier=SYSTEM_PROMPT)
    return agent
