from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from .tools import list_files, read_file, write_file, delete_file

def build_agent():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    tools = [list_files, read_file, write_file, delete_file]

    agent = create_react_agent(llm, tools)
    return agent
