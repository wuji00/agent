from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from .tools import computer_tool, bash_tool, edit_tool
from typing import List, Dict

class ComputerUseAgent:
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        # Computer use requires betas
        self.llm = ChatAnthropic(
            model=model_name,
            temperature=0,
            model_kwargs={"betas": ["computer-use-2024-10-22"]}
        )
        self.tools = [computer_tool, bash_tool, edit_tool]

        system_prompt = """You are a computer use agent. You can use the computer, run bash commands, and edit files.
        """

        self.agent = create_react_agent(self.llm, self.tools, prompt=system_prompt)

    def invoke(self, messages: List[Dict[str, str]]):
        return self.agent.invoke({"messages": messages})
