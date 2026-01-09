"""
Autonomous Coding Agent
=======================

A LangGraph implementation of the autonomous coding agent.
"""

import os
import asyncio
from pathlib import Path
from typing import Annotated, TypedDict, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

from .tools import ALL_TOOLS, set_workspace, WORKSPACE_DIR

# Configuration
PROMPTS_DIR = Path(__file__).parent / "prompts"

def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / f"{name}.md"
    return prompt_path.read_text()

def get_initializer_prompt() -> str:
    """Load the initializer prompt."""
    return load_prompt("initializer_prompt")

def get_coding_prompt() -> str:
    """Load the coding agent prompt."""
    return load_prompt("coding_prompt")

def copy_spec_to_project(project_dir: Path) -> None:
    """Copy the app spec file into the project directory for the agent to read."""
    spec_source = PROMPTS_DIR / "app_spec.txt"
    spec_dest = project_dir / "app_spec.txt"
    if not spec_dest.exists():
        spec_dest.parent.mkdir(parents=True, exist_ok=True)
        spec_dest.write_text(spec_source.read_text())
        print(f"Copied app_spec.txt to {project_dir}")

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    iteration: int
    max_iterations: int
    is_first_run: bool

async def run_autonomous_agent(
    project_dir: Path,
    model_name: str = "claude-3-5-sonnet-20241022",
    max_iterations: int = 10,
):
    """
    Run the autonomous agent loop using LangGraph.
    """
    # Initialize workspace
    set_workspace(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    # Check if this is a fresh start
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()

    if is_first_run:
        print("Fresh start - copying spec to project.")
        copy_spec_to_project(project_dir)

    # Initialize LLM
    llm = ChatAnthropic(model=model_name, temperature=0)

    # Create the agent
    # We will use create_react_agent for simplicity as the core logic is loop-based tool use.
    # However, we need to inject the correct system prompt based on the phase.

    # Since the prompt changes between runs (Initializer vs Coding), we can treat each "iteration"
    # as a call to the agent with a specific system prompt.

    while True:
        # Determine prompt
        if is_first_run:
            system_prompt = get_initializer_prompt()
            print("\nStarting INITIALIZER Phase (Creating feature list)...")
        else:
            system_prompt = get_coding_prompt()
            print("\nStarting CODING Phase (Implementing features)...")

        # Create agent for this phase
        agent = create_react_agent(llm, ALL_TOOLS, state_modifier=system_prompt)

        # Determine the user input/trigger
        # The prompts imply the agent drives itself, but usually needs an initial "Go" or status update.
        # In the original demo, it seems to just run.
        # The prompts say:
        # Initializer: "You are the Initializer Agent..."
        # Coding: "You are the Coding Agent..."

        # We need to pass the conversation history or start fresh?
        # The original code creates a NEW client every iteration: `client = create_client(project_dir, model)`
        # And sends the prompt.

        # So we should treat each iteration as a fresh conversation with the agent,
        # but the agent has access to the filesystem (persistent state).

        initial_message = "Start working. Check the status of the project and proceed."
        if is_first_run:
             initial_message = "Read the app_spec.txt and generate the feature_list.json."

        print(f"Project Directory: {project_dir}")

        # Run the agent
        # We limit the recursion depth to prevent infinite loops within one "session"
        config = {"recursion_limit": 50}

        print("Thinking...", flush=True)
        events = agent.stream(
            {"messages": [HumanMessage(content=initial_message)]},
            config=config
        )

        async for event in events:
            if "messages" in event:
                pass # Can add logging here if needed
            if "agent" in event:
                 msg = event["agent"]["messages"][0]
                 print(f"Agent: {msg.content[:100]}...", flush=True)
            if "tools" in event:
                 msg = event["tools"]["messages"][0]
                 print(f"Tool Result: {msg.name} - {str(msg.content)[:100]}...", flush=True)


        # Check if we should continue
        is_first_run = False # After first run, we are always in coding mode

        # In a real loop, we would check for max_iterations or if the agent signals completion.
        # For this demo, we'll just break after one pass of each if this is a test,
        # but the request is to implement the loop.

        max_iterations -= 1
        if max_iterations <= 0:
            print("Reached max iterations.")
            break

        print("Session complete. Starting next session in 3 seconds...")
        await asyncio.sleep(3)

if __name__ == "__main__":
    # Test run
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default="./workspace", type=Path)
    parser.add_argument("--max-iterations", default=2, type=int)
    args = parser.parse_args()

    asyncio.run(run_autonomous_agent(args.project_dir, max_iterations=args.max_iterations))
