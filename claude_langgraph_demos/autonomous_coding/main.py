#!/usr/bin/env python3
"""
Autonomous Coding Agent Demo Entry Point
"""

import asyncio
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the repository root to sys.path to ensure modules can be imported
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from claude_langgraph_demos.autonomous_coding.agent import run_autonomous_agent

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Autonomous Coding Agent Demo")
    parser.add_argument("--project-dir", type=Path, default=Path("./autonomous_workspace"), help="Directory for the project")
    parser.add_argument("--max-iterations", type=int, default=10, help="Maximum number of iterations")
    parser.add_argument("--model", type=str, default="claude-3-5-sonnet-20241022", help="Model to use")

    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set.")
        return

    print(f"Starting Autonomous Coding Agent...")
    print(f"Project Directory: {args.project_dir}")
    print(f"Model: {args.model}")

    try:
        asyncio.run(run_autonomous_agent(
            project_dir=args.project_dir,
            model_name=args.model,
            max_iterations=args.max_iterations
        ))
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
