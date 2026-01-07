# Claude LangGraph Demos

This repository contains LangGraph implementations of the demos found in `anthropics/claude-quickstarts`.

## Demos

1.  **Autonomous Coding Agent**:
    *   Location: `autonomous_coding/`
    *   Description: A dual-phase agent that generates a feature list and iteratively implements code.
    *   Run: `python -m claude_langgraph_demos.autonomous_coding.agent`

2.  **Customer Support Agent**:
    *   Location: `customer_support_agent/`
    *   Description: A RAG-based support agent using FAISS and Claude.
    *   Run: `python -m claude_langgraph_demos.customer_support_agent.agent` (Run `setup_kb.py` first)

3.  **Financial Data Analyst**:
    *   Location: `financial_data_analyst/`
    *   Description: An agent that uses a tool to generate financial charts.
    *   Run: `python -m claude_langgraph_demos.financial_data_analyst.agent`

4.  **Computer Use Demo**:
    *   Location: `computer_use_demo/`
    *   Description: A demonstration of the Computer Use beta (mocked execution).
    *   Run: `python -m claude_langgraph_demos.computer_use_demo.agent`

## Requirements

*   Python 3.12+
*   Dependencies listed in `requirements.txt` / `pyproject.toml`
*   Anthropic API Key set in `.env` or environment variable `ANTHROPIC_API_KEY`.

## Setup

1.  Install dependencies:
    ```bash
    pip install -e .
    ```

2.  Set API Key:
    ```bash
    export ANTHROPIC_API_KEY=sk-ant-...
    ```
