import json
from typing import Annotated, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Tools ---

@tool
def get_stock_price(symbol: str):
    """Get the current stock price for a given symbol."""
    # Mock data
    mock_prices = {
        "AAPL": 150.00,
        "GOOGL": 2800.00,
        "MSFT": 300.00,
        "AMZN": 3400.00
    }
    return mock_prices.get(symbol.upper(), 100.00) # Default to 100 if unknown

@tool
def get_company_info(symbol: str):
    """Get basic information about a company."""
    # Mock data
    mock_info = {
        "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
        "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
        "MSFT": {"name": "Microsoft Corporation", "sector": "Technology"},
        "AMZN": {"name": "Amazon.com, Inc.", "sector": "Consumer Discretionary"}
    }
    return mock_info.get(symbol.upper(), {"name": "Unknown", "sector": "Unknown"})

@tool
def get_financial_metrics(symbol: str):
    """Get financial metrics like P/E ratio, EPS, etc."""
    # Mock data
    return {
        "pe_ratio": 25.5,
        "eps": 5.4,
        "market_cap": "2.5T"
    }

# --- System Prompt ---

SYSTEM_PROMPT = """You are a helpful financial analyst.
You have access to stock prices and company info.
When asked to visualize data, you MUST output a JSON object compatible with Recharts inside a code block.
The code block should be tagged with `json`.
The JSON object should have a structure like this:
```json
{
  "type": "bar", // or "line", "area", "pie"
  "title": "Chart Title",
  "data": [
    {"name": "Category A", "value": 100},
    {"name": "Category B", "value": 200}
  ],
  "xAxis": "name",
  "yAxis": "value"
}
```
Always provide text analysis alongside the visualization.
"""

# --- Agent ---

def create_financial_analyst_agent():
    llm = ChatAnthropic(model=MODEL_NAME)
    tools = [get_stock_price, get_company_info, get_financial_metrics]

    # In langgraph 0.2+, create_react_agent supports state_modifier or prompt.
    # The memory mentions langgraph 1.0.5 requires `prompt` parameter for system instructions.

    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

# --- Entry Point ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Compare the stock prices of AAPL and MSFT and visualize them."

    print(f"Processing query: {user_query}")
    agent = create_financial_analyst_agent()

    # Run the agent
    response = agent.invoke({"messages": [HumanMessage(content=user_query)]})

    print("\n--- Response ---")
    for message in response["messages"]:
        if message.type == "ai":
             print(f"AI: {message.content}")
