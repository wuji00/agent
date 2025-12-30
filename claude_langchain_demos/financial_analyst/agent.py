from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from tools import get_stock_price, get_company_financials, get_market_trends

def build_agent():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    tools = [get_stock_price, get_company_financials, get_market_trends]

    # create_react_agent creates a graph that loops: Call Agent -> Execute Tools -> Call Agent
    # We add a system message to instruct the model to output JSON when appropriate
    system_message = """You are a financial data analyst.
    When the user asks for data comparison or trends that can be visualized,
    you MUST output the data in a structured JSON format compatible with Recharts in addition to your text explanation.
    The JSON should be in a code block like ```json ... ```.

    The JSON structure should look like this:
    {
      "chartType": "bar" | "line" | "pie",
      "data": [
        { "name": "Category1", "value": 100 },
        { "name": "Category2", "value": 200 }
      ],
      "title": "Chart Title",
      "xAxisKey": "name",
      "dataKey": "value"
    }
    """

    agent = create_react_agent(llm, tools, state_modifier=system_message)
    return agent
