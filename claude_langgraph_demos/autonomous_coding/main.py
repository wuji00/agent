import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.runnables import Runnable

# Adjust path to include the tools module if run as a script
sys.path.append(str(Path(__file__).parent))

from tools import TOOLS, WORKSPACE_DIR

class FakeLLM(Runnable):
    def bind_tools(self, tools, **kwargs):
        # We need to mimic bind_tools returning a runnable that mimics the model with tools
        # For simplicity, we just return self because invoke() will handle logic.
        return self

    def invoke(self, input: Any, config: Any = None) -> AIMessage:
        # Simple fake response that pretends to do something
        # If the input contains "feature_list.json", we pretend we are writing it.
        messages = input if isinstance(input, list) else input.get("messages", [])

        # Flatten messages just in case
        flat_messages = []
        for m in messages:
            if isinstance(m, list):
                flat_messages.extend(m)
            else:
                flat_messages.append(m)
        messages = flat_messages

        last_message = messages[-1] if messages else None
        last_content = last_message.content if last_message else ""

        # Debug print
        # print(f"DEBUG: Last message type: {type(last_message)}")
        # print(f"DEBUG: Last message content: {last_content}")

        # If it's a tool output (ToolMessage), we should say something about it
        if last_message and last_message.type == "tool":
             return AIMessage(content="Tool executed successfully. I am done.")

        if "initializer_prompt" in str(last_content) or "app_spec.txt" in str(last_content):
            # Simulate writing the feature list
            # The agent will receive this, see tool_calls, and run the tool.
            return AIMessage(content="I will create the feature list.", tool_calls=[
                {"name": "write_file", "args": {"path": "feature_list.json", "content": '["feature1", "feature2"]'}, "id": "call_1"}
            ])
        elif "coding_prompt" in str(last_content):
             return AIMessage(content="I will implement feature1.", tool_calls=[
                {"name": "write_file", "args": {"path": "src/feature1.py", "content": 'print("feature1")'}, "id": "call_2"}
            ])
        else:
            return AIMessage(content="I am done.")

def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = Path(__file__).parent / "prompts" / f"{name}.md"
    return prompt_path.read_text()

def get_initializer_prompt() -> str:
    return load_prompt("initializer_prompt")

def get_coding_prompt() -> str:
    return load_prompt("coding_prompt")

def copy_spec_to_project(project_dir: Path) -> None:
    spec_source = Path(__file__).parent / "prompts" / "app_spec.txt"
    spec_dest = project_dir / "app_spec.txt"
    if not spec_dest.exists():
        if not project_dir.exists():
             project_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(spec_source, spec_dest)
        print("Copied app_spec.txt to project directory")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Coding Agent Demo")
    parser.add_argument("--project-dir", type=str, default="workspace", help="Directory for the project")
    parser.add_argument("--model", type=str, default="claude-3-5-sonnet-20241022", help="Claude model to use")
    parser.add_argument("--max-iterations", type=int, default=10, help="Maximum number of iterations")
    parser.add_argument("--test-mode", action="store_true", help="Run with mock LLM for testing")

    args = parser.parse_args()

    # Update WORKSPACE_DIR
    import tools
    tools.WORKSPACE_DIR = Path(args.project_dir).resolve()
    project_dir = tools.WORKSPACE_DIR

    print(f"Project directory: {project_dir}")
    project_dir.mkdir(parents=True, exist_ok=True)

    # Check if first run
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()

    if is_first_run:
        print("First run detected. Initializing project...")
        copy_spec_to_project(project_dir)
        prompt_content = get_initializer_prompt()
        system_message = "You are an expert software architect. You are initializing a new project."
    else:
        print("Continuing existing project...")
        prompt_content = get_coding_prompt()
        system_message = "You are an expert full-stack developer. You are building a web application."

    # Initialize LLM
    if args.test_mode:
        print("Running in TEST MODE with FakeLLM")
        llm = FakeLLM()
    else:
        llm = ChatAnthropic(model=args.model, temperature=0)

    # Initialize Agent
    agent = create_react_agent(llm, TOOLS, prompt=system_message)

    # Run Agent
    print("Starting agent loop...")

    iteration = 0
    while iteration < args.max_iterations:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")

        if is_first_run:
            prompt_content = get_initializer_prompt()
        else:
            prompt_content = get_coding_prompt()

        inputs = {"messages": [HumanMessage(content=prompt_content)]}

        # We invoke the agent
        final_state = agent.invoke(inputs)

        # Print the last message
        last_message = final_state["messages"][-1]
        print(f"Agent Response: {last_message.content}")

        # Check if we should switch from initializer to coding
        if is_first_run:
            if (project_dir / "feature_list.json").exists():
                print("Initialization complete. Switching to coding mode.")
                is_first_run = False
            else:
                 print("Warning: feature_list.json not found after initialization. Agent might have failed to create it.")

        # Small check to avoid infinite loops if it's stuck
        if "ALL TASKS COMPLETED" in str(last_message.content) or "I am done" in str(last_message.content):
            print("Tasks appear to be completed.")
            break

if __name__ == "__main__":
    main()
