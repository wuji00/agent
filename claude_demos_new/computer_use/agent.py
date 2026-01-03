from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from .tools import computer_tool, bash_tool, edit_tool

SYSTEM_PROMPT = """You are a computer use agent. You can control a computer to perform tasks.
You have access to tools to interact with the computer.
"""

def create_computer_use_agent():
    # Memory: "Implementations using Anthropic's Computer Use features via `ChatAnthropic` require the model `claude-3-5-sonnet-20241022` and the `betas` parameter to include `computer-use-2024-10-22`."
    # Also "The Computer Use demo implementation should use mock tools... to log actions without execution when running in environments without a GUI."

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        model_kwargs={"betas": ["computer-use-2024-10-22"]}
    )

    tools = [computer_tool, bash_tool, edit_tool]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return agent
