from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from .tools import read_file, write_file, list_files, delete_file
from typing import List, Dict

class AutonomousCodingAgent:
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        self.llm = ChatAnthropic(model=model_name, temperature=0.5)
        self.tools = [read_file, write_file, list_files, delete_file]

        system_prompt = """You are an autonomous coding agent.
You can read, write, list, and delete files in your workspace.
Use these tools to accomplish coding tasks.
Always verify your work by reading the files you create or modify.
"""
        self.agent = create_react_agent(self.llm, self.tools, prompt=system_prompt)

    def invoke(self, messages: List[Dict[str, str]]):
        return self.agent.invoke({"messages": messages})
