import os
import sys
from typing import Annotated, TypedDict, List
from pathlib import Path

# Add the parent directory to sys.path to resolve internal relative imports if needed
sys.path.append(str(Path(__file__).parent.parent))

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from tools import read_file, write_file, list_files, delete_file, browser_tool
from prompts import get_initializer_prompt, get_coding_prompt, copy_spec_to_project

# Ensure the prompt loading works with correct path
# We might need to adjust prompts.py PROMPTS_DIR if it doesn't align with where we copied things
# But since we copied prompts/ folder alongside prompts.py, it should work.

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def create_autonomous_agent(is_first_run: bool):
    tools = [read_file, write_file, list_files, delete_file, browser_tool]

    # Choose prompt based on session type
    if is_first_run:
        prompt_content = get_initializer_prompt()
    else:
        prompt_content = get_coding_prompt()

    system_prompt = SystemMessage(content=prompt_content)

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    def call_model(state: AgentState):
        messages = state["messages"]
        # Prepend system prompt if not present?
        # Actually create_react_agent usually handles this, but here we build custom graph for clarity or use create_react_agent.
        # Let's use custom graph to ensure we insert system prompt correctly.

        # Ensure system prompt is the first message or added to context
        # If we just add it to messages, it works.

        # Filter out system messages to avoid duplication if we persist state?
        # For this demo, we can just prepend it.

        if not isinstance(messages[0], SystemMessage):
             messages = [system_prompt] + messages
        else:
             # Replace the existing system prompt if needed, or assume it's correct
             messages[0] = system_prompt

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()

if __name__ == "__main__":
    print("Autonomous Coding Agent (LangGraph) - Demo")

    project_dir = Path("workspace")
    project_dir.mkdir(exist_ok=True)

    # Check if this is a fresh start or continuation
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()

    if is_first_run:
        print("Fresh start - using initializer prompt")
        copy_spec_to_project(project_dir)
        # We also need to make sure the agent works in the 'workspace' directory.
        # The tools currently default to current working directory.
        # We should probably change cwd or update tools to respect project_dir.
        # For simplicity, we'll change cwd.
        os.chdir(project_dir)
    else:
        print("Continuing existing project")
        os.chdir(project_dir)

    app = create_autonomous_agent(is_first_run)

    # We need to start the conversation.
    # The prompt expects the agent to start.
    # We can send a dummy user message "Start session" or similar.

    initial_message = HumanMessage(content="Start the session. Follow your instructions.")

    print("... Agent starting ...")
    try:
        for event in app.stream({"messages": [initial_message]}, stream_mode="values"):
            message = event["messages"][-1]
            if isinstance(message, tuple):
                 # Sometimes stream returns tuples? No, usually dict with 'messages'
                 pass

            message.pretty_print()

    except Exception as e:
        print(f"Error: {e}")
