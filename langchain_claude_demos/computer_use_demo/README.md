# Computer Use Demo (Mock)

This is a demonstration of the "Computer Use" capability using mocked tools with LangGraph.

## Description
The original demo runs in a Docker container with VNC. This implementation mocks the tools (`computer`, `bash`, `str_replace_editor`) to demonstrate the agent loop and tool calling logic without requiring a full desktop environment.

## Features
- **Mock Tools:** Simulates mouse clicks, typing, screenshots, and shell commands.
- **Agent Loop:** Uses LangGraph to handle the tool execution loop.

## Setup

1. Install dependencies:
   ```bash
   uv pip install langchain langgraph langchain-anthropic
   ```

2. Set your Anthropic API Key:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```

## Example Usage
- "Take a screenshot."
- "Click on the start button."
- "Open terminal and list files."
