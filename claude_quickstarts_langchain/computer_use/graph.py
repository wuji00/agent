from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from computer_use.tools import computer, bash, str_replace_editor

SYSTEM_PROMPT = """You are a computer use agent.
You have access to a computer tool, a bash tool, and an editor tool.
Use them to accomplish the user's request.
"""

def get_app():
    # Use the latest model which supports computer use beta
    # In LangChain, we might need to pass specific headers or beta flags
    # But for this demo we assume the model supports it or we just use the tools normally.
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

    tools = [computer, bash, str_replace_editor]

    agent = create_react_agent(llm, tools, state_modifier=SYSTEM_PROMPT)
    return agent
