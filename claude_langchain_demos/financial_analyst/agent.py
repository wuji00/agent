from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from tools import get_stock_price, get_company_financials, get_market_trends

def build_agent():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    tools = [get_stock_price, get_company_financials, get_market_trends]

    # create_react_agent creates a graph that loops: Call Agent -> Execute Tools -> Call Agent
    agent = create_react_agent(llm, tools)
    return agent
