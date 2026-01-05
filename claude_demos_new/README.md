# Claude Demos New

This directory contains LangChain and LangGraph implementations of Claude Quickstarts.
It corresponds to the "new" clean implementation.

## Structure

- `customer_support/`: RAG agent for customer support.
- `financial_analyst/`: Agent with tools for financial data (mocked).
- `computer_use/`: Agent simulating computer control (mocked).
- `autonomous_coding/`: Agent with file system access for coding tasks.

## Setup

1.  Navigate to `claude_demos_new`.
2.  Install dependencies:
    ```bash
    uv sync
    ```
    (Or install dependencies listed in `pyproject.toml` manually if not using `uv`)

3.  Set `ANTHROPIC_API_KEY` in environment variables or `.env`.

## Usage

Run each demo from the `claude_demos_new` directory (or ensure PYTHONPATH includes it).

- **Customer Support**: `python customer_support/main.py`
- **Financial Analyst**: `python financial_analyst/main.py`
- **Computer Use**: `python computer_use/main.py`
- **Autonomous Coding**: `python autonomous_coding/main.py`
