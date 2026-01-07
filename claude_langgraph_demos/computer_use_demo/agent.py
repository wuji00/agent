
import os
from typing import Annotated, TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

from .tools import computer_tool, bash_tool, edit_tool

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def run_computer_use_agent():
    tools = [computer_tool, bash_tool, edit_tool]

    # Configure model with beta header as per memory
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        model_kwargs={'extra_headers': {'anthropic-beta': 'computer-use-2024-10-22'}}
    )

    system_prompt = "You are an agent capable of using a computer. Use the available tools to perform actions."

    agent = create_react_agent(llm, tools, state_modifier=system_prompt)
    return agent

if __name__ == "__main__":
    agent = run_computer_use_agent()
    print("Computer Use Agent Initialized")
