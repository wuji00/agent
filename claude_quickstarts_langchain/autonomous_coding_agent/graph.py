import os
import subprocess
import sys
from typing import Annotated, TypedDict, List, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# Workspace setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# Prompts
def load_prompt(name):
    path = os.path.join(BASE_DIR, "prompts", name)
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error loading prompt {name}: {e}"

INITIALIZER_PROMPT = load_prompt("initializer_prompt.md")
CODING_PROMPT = load_prompt("coding_prompt.md")

# Tools
file_tools = FileManagementToolkit(root_dir=WORKSPACE_DIR).get_tools()

@tool
def bash_command(command: str):
    """Run a bash command in the workspace directory. Use this to run git, run tests, list files, etc."""
    try:
        # Security warning: In a real app, sandbox this!
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_DIR,
            timeout=60
        )
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nReturn Code: {result.returncode}"
        return output
    except Exception as e:
        return f"Error: {e}"

tools = file_tools + [bash_command]
tool_node = ToolNode(tools)

# State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    stage: str # "initializer" or "coding"

# Node
def agent_node(state: AgentState):
    stage = state.get("stage", "initializer")
    messages = state["messages"]

    # Select prompt
    if stage == "initializer":
        sys_prompt = INITIALIZER_PROMPT
    else:
        sys_prompt = CODING_PROMPT

    # We prepend the system prompt.
    prompt_messages = [SystemMessage(content=sys_prompt)] + messages

    # Use a capable model
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.5, max_tokens=4096)
    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(prompt_messages)
    return {"messages": [response]}

# Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()
