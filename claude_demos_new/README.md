# Claude Quickstarts - LangChain & LangGraph Implementations

This repository contains implementations of Anthropic's Claude Quickstarts using LangChain and LangGraph.

## Prerequisites

- Python 3.9+
- An Anthropic API Key (set in `.env` as `ANTHROPIC_API_KEY`)

## Setup

1.  Navigate to the directory:
    ```bash
    cd claude_demos_new
    ```

2.  Install dependencies using `uv` (recommended) or pip:
    ```bash
    uv sync
    # OR
    pip install -r requirements.txt # (You'd need to generate this from pyproject.toml)
    ```

3.  Create a `.env` file:
    ```bash
    touch .env
    ```
    Add your API key:
    ```
    ANTHROPIC_API_KEY=your_api_key_here
    ```

## Demos

### 1. Customer Support Agent

A RAG-based support agent that categorizes queries and retrieves answers from a knowledge base.

- **Source:** `customer_support/agent.py`
- **Data:** `customer_support/knowledge.txt`, `customer_support/categories.json`
- **Run:**
    ```bash
    python -m customer_support.agent "What is Claude 3.5 Sonnet?"
    ```

### 2. Financial Analyst

An agent that analyzes mock financial data and outputs Recharts-compatible JSON for visualization.

- **Source:** `financial_analyst/agent.py`
- **Run:**
    ```bash
    python -m financial_analyst.agent "Compare AAPL and MSFT stock prices"
    ```

### 3. Computer Use Demo

A ReAct agent demonstrating the "Computer Use" capability (using mock tools for safety/compatibility in this environment).

- **Source:** `computer_use/agent.py`
- **Run:**
    ```bash
    python -m computer_use.agent "Take a screenshot"
    ```

### 4. Autonomous Coding Agent

An agent capable of file system operations to write and manage code.

- **Source:** `autonomous_coding/agent.py`
- **Workspace:** `autonomous_coding/workspace/`
- **Run:**
    ```bash
    python -m autonomous_coding.agent "Create a fibonacci.py script"
    ```

## Implementation Details

- **LangGraph**: Used for state management and agent loops (`create_react_agent` and `StateGraph`).
- **FAISS**: Used for vector storage in the Customer Support agent.
- **Tools**: Custom tools implemented using `@tool` decorator.
