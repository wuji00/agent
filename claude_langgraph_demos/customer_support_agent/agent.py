
import os
from typing import Annotated, TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import create_retriever_tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Load env vars
load_dotenv()

from .tools import get_retriever

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def run_customer_support_agent():
    # Setup tools
    retriever = get_retriever()
    tool = create_retriever_tool(
        retriever,
        "search_knowledge_base",
        "Searches and returns documents regarding customer support."
    )
    tools = [tool]

    # Setup model
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

    # Create agent
    system_prompt = "You are a helpful customer support agent. Use the search tool to answer questions."
    agent = create_react_agent(llm, tools, state_modifier=system_prompt)

    return agent

if __name__ == "__main__":
    agent = run_customer_support_agent()
    print("Customer Support Agent Initialized")
