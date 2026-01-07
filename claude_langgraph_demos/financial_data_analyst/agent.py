
import os
from typing import Annotated, TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

from .tools import generate_chart

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def run_financial_analyst_agent():
    tools = [generate_chart]
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

    system_prompt = """You are a financial data analyst.
    Analyze the user's request and if they ask for visualization, use the generate_chart tool.
    Output your analysis and any JSON data for charts in a code block."""

    agent = create_react_agent(llm, tools, state_modifier=system_prompt)
    return agent

if __name__ == "__main__":
    agent = run_financial_analyst_agent()
    print("Financial Data Analyst Agent Initialized")
