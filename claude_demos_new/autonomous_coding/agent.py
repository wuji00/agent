from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from .tools import read_file, write_file, list_files, delete_file

SYSTEM_PROMPT = """You are an autonomous coding agent.
You can read, write, list, and delete files in the workspace.
Your goal is to complete coding tasks requested by the user.
Always verify your work by reading the file you just wrote.
"""

def create_coding_agent():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    tools = [read_file, write_file, list_files, delete_file]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return agent
