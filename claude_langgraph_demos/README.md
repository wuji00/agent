# Claude LangGraph Demos

This repository contains LangGraph implementations of the demos found in `anthropics/claude-quickstarts`.

## Demos

1.  **Customer Support Agent**:
    *   Location: `customer_support_agent/`
    *   Description: A RAG-based support agent using FAISS and Claude.
    *   Run:
        ```bash
        cd customer_support_agent
        python setup_kb.py # First time only
        python agent.py
        ```

2.  **Financial Data Analyst**:
    *   Location: `financial_data_analyst/`
    *   Description: An agent that uses a tool to generate financial charts.
    *   Run: `python -m claude_langgraph_demos.financial_data_analyst.agent` (from root)

3.  **Computer Use Demo**:
    *   Location: `computer_use_demo/`
    *   Description: A demonstration of the Computer Use beta (mocked execution).
    *   Run: `python -m claude_langgraph_demos.computer_use_demo.agent` (from root)

4.  **Autonomous Coding Agent**:
    *   Location: `autonomous_coding/`
    *   Description: An agent that can initialize and implement a coding project autonomously.
    *   Run:
        ```bash
        # Run from root directory
        python -m claude_langgraph_demos.autonomous_coding.main --project-dir workspace
        ```
    *   Features:
        *   Initializer Prompt: Creates a feature list from `app_spec.txt`.
        *   Coding Prompt: Implements features iteratively.
        *   Tools: File read/write, bash execution (restricted).

## Requirements

*   Python 3.12+
*   `uv` for dependency management (optional, or use pip).
*   Anthropic API Key set in `.env` or environment variable `ANTHROPIC_API_KEY`.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Set API Key:
    ```bash
    export ANTHROPIC_API_KEY=sk-ant-...
    ```
