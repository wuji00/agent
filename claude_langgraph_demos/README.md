# Claude LangGraph Demos

This repository contains LangGraph implementations of the demos found in `anthropics/claude-quickstarts`.

## Demos

1.  **Autonomous Coding Agent**:
    *   Location: `autonomous_coding/`
    *   Description: A long-running agent that plans and implements code features.
    *   Run: `python -m claude_langgraph_demos.autonomous_coding.main`

2.  **Customer Support Agent**:
    *   Location: `customer_support_agent/`
    *   Description: A RAG-based support agent using FAISS and Claude.
    *   Run: `python -m claude_langgraph_demos.customer_support_agent.agent` (after setup)

3.  **Financial Data Analyst**:
    *   Location: `financial_data_analyst/`
    *   Description: An agent that uses a tool to generate financial charts.
    *   Run: `python -m claude_langgraph_demos.financial_data_analyst.agent`

4.  **Computer Use Demo**:
    *   Location: `computer_use_demo/`
    *   Description: A demonstration of the Computer Use beta (mocked execution).
    *   Run: `python -m claude_langgraph_demos.computer_use_demo.agent`

5.  **Browser Use Demo**:
    *   Location: `browser_use_demo/`
    *   Description: A demonstration of browser automation (mocked execution).
    *   Run: `python -m claude_langgraph_demos.browser_use_demo.agent`

## Requirements

*   Python 3.12+
*   `uv` for dependency management (optional, or use pip).
*   Anthropic API Key set in `.env` or environment variable `ANTHROPIC_API_KEY`.

## Setup

1.  Install dependencies:
    ```bash
    uv sync
    # OR
    pip install -r requirements.txt
    ```

2.  Set API Key:
    ```bash
    export ANTHROPIC_API_KEY=sk-ant-...
    ```

3.  Set PYTHONPATH (if running modules directly from root):
    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    ```

4.  For Customer Support Agent, run the setup first:
    ```bash
    cd claude_langgraph_demos/customer_support_agent
    python setup_kb.py
    ```
