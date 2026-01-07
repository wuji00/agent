import os
import asyncio
from pathlib import Path
from typing import Annotated, Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict

from .tools import ALL_TOOLS, WORKSPACE_DIR
from .prompts import get_initializer_prompt, get_coding_prompt, copy_spec_to_project

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    iteration: int

def get_model():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        max_tokens=4096,
        timeout=None,
        stop=None
    )

async def run_autonomous_agent(
    project_dir: Path = WORKSPACE_DIR,
    model: str = "claude-3-5-sonnet-20241022",
    max_iterations: int | None = None,
):
    """
    Run the autonomous agent loop using LangGraph.
    """
    print(f"Starting Autonomous Coding Agent in {project_dir}")
    project_dir.mkdir(parents=True, exist_ok=True)

    # Ensure app_spec.txt is in the workspace
    if not (project_dir / "app_spec.txt").exists():
        # We need to copy it from prompts/app_spec.txt
        # Since copy_spec_to_project expects project_dir, let's use it
        # But we need to make sure PROMPTS_DIR is correct in prompts.py or pass it
        copy_spec_to_project(project_dir)

    iteration = 0

    while True:
        iteration += 1
        if max_iterations and iteration > max_iterations:
            print("Reached max iterations.")
            break

        # Check if feature_list.json exists to decide prompt
        is_first_run = not (project_dir / "feature_list.json").exists()

        if is_first_run:
            print("First run: Initializing project...")
            system_prompt = get_initializer_prompt()
        else:
            print(f"Iteration {iteration}: Coding phase...")
            system_prompt = get_coding_prompt()

        # Create a fresh agent for this session
        agent = create_react_agent(get_model(), ALL_TOOLS, state_modifier=system_prompt)

        # Run the agent
        # We pass an empty message list to start, relying on the system prompt to drive action
        # However, create_react_agent usually expects a user message to start.
        # The prompts in this demo are designed as system prompts that instruct the model what to do.
        # But the model needs a trigger.

        initial_message = "Please proceed with the current task."

        print(f"--- Session {iteration} Started ---")
        try:
            # We treat each iteration as a single "turn" or a short conversation until the model stops?
            # The original code runs `client.query(message)` where message is the prompt.
            # But here `state_modifier` sets the system prompt.
            # We can send a "Go" message.

            # Using ainvoke directly
            result = await agent.ainvoke({"messages": [HumanMessage(content=initial_message)]})

            # Print the last message content
            last_message = result["messages"][-1]
            print("Agent Output:")
            print(last_message.content)

        except Exception as e:
            print(f"Error in session {iteration}: {e}")

        print(f"--- Session {iteration} Finished ---")

        # Simple delay for demo purposes
        await asyncio.sleep(2)

if __name__ == "__main__":
    # Ensure we can run this file directly
    asyncio.run(run_autonomous_agent())
