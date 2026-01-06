# Claude LangGraph Demos

This repository contains LangGraph implementations of the demos found in `anthropics/claude-quickstarts`.

## Demos

1.  **Customer Support Agent**:
    *   Location: `customer_support_agent/`
    *   Description: A RAG-based support agent using FAISS and Claude.
    *   Run: `python setup_kb.py` then `python agent.py`.

2.  **Financial Data Analyst**:
    *   Location: `financial_data_analyst/`
    *   Description: An agent that uses a tool to generate financial charts.
    *   Run: `python agent.py`.

3.  **Computer Use Demo**:
    *   Location: `computer_use_demo/`
    *   Description: A demonstration of the Computer Use beta (mocked execution).
    *   Run: `python agent.py`.

4.  **Autonomous Coding**:
    *   Location: `autonomous_coding/`
    *   Description: An agent that implements features based on a spec, verifying them with tools (File system + Mock Browser).
    *   Run: `python agent.py` (ensure you are in the directory or set PYTHONPATH).

5.  **Browser Use Demo**:
    *   Location: `browser_use_demo/`
    *   Description: A simpler demonstration of browser automation (mocked execution).
    *   Run: `python agent.py`.

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
