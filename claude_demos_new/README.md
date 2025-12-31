# Claude LangChain/LangGraph Demos

This repository contains LangChain and LangGraph implementations of four Claude Quickstart demos.

## Demos

### 1. Customer Support Agent
A RAG-based support agent that categorizes queries and retrieves information from a knowledge base.
- **Code**: `customer_support/agent.py`
- **Data**: `customer_support/data/`

### 2. Financial Data Analyst
An agent that analyzes data and generates structured JSON for financial visualizations.
- **Code**: `financial_analyst/agent.py`

### 3. Computer Use Demo
A demonstration of the Claude Computer Use API (beta), using mock tools for local simulation.
- **Code**: `computer_use/agent.py`

### 4. Autonomous Coding Agent
An agent capable of performing file system operations (read, write, list, delete) within a safe workspace.
- **Code**: `autonomous_coding/agent.py`
- **Workspace**: `workspace/`

## Setup

1. Install dependencies (using `uv` is recommended):
   ```bash
   uv sync
   ```

2. Set your Anthropic API Key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

## Running the Demos

Each demo can be run directly as a script:

```bash
# Customer Support
uv run python customer_support/agent.py "What is Claude 3.5 Sonnet?"

# Financial Analyst
uv run python financial_analyst/agent.py "Create a bar chart for Q1 vs Q2 revenue."

# Computer Use
uv run python computer_use/agent.py "Take a screenshot."

# Autonomous Coding
uv run python autonomous_coding/agent.py "Create a file named hello.py"
```
