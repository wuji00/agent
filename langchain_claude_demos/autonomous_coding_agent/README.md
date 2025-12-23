# Autonomous Coding Agent

A simplified version of the Autonomous Coding Agent using LangGraph. It demonstrates a multi-step workflow where an agent initializes a project plan and then systematically implements features.

## Features
- **Two-Stage Workflow:**
    1.  **Initializer:** Sets up the project and defines a feature list.
    2.  **Coding Agent:** Iterates through the feature list and implements each feature.
- **State Persistence:** Keeps track of the current feature index in the state.

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

## Workflow Description
The agent starts by creating a `feature_list.json`. Then, it enters a loop where it picks the next feature, uses Claude to generate code (simulated), and updates the progress until all features are done.
