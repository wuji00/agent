# Claude LangChain Demos

This repository contains four example applications implemented using [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/).
Based on [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts), these demos showcase how to replicate these capabilities using the LangChain ecosystem.

## Table of Contents

1.  [Environment Setup](#environment-setup)
2.  [Customer Support Agent](#customer-support-agent)
3.  [Financial Data Analyst](#financial-data-analyst)
4.  [Computer Use Demo](#computer-use-demo)
5.  [Autonomous Coding Agent](#autonomous-coding-agent)

## Environment Setup

This project uses `uv` for dependency management. Ensure `uv` is installed.

1.  Enter the project directory:
    ```bash
    cd claude_langchain_demos
    ```

2.  Install dependencies:
    ```bash
    uv sync
    ```

3.  Configure API Key:
    Copy `.env.example` to `.env` and fill in your Anthropic API Key.
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```
    ANTHROPIC_API_KEY=sk-ant-api03-...
    ```

## Demos

All demos are run via the command line.

### Customer Support Agent

A RAG (Retrieval-Augmented Generation) application. It loads a local text file as a knowledge base (simulating Anthropic documentation), retrieves relevant information to answer customer support queries, and simultaneously categorizes the issue.

**Run:**
```bash
uv run python customer_support/main.py
```

**Example Inputs:**
- "How do I update my billing info?"
- "What is Claude?"

### Financial Data Analyst

An intelligent agent capable of calling tools to get stock prices and company information. It uses mock stock data for demonstration. It is configured to output structured JSON for charting when appropriate.

**Run:**
```bash
uv run python financial_analyst/main.py
```

**Example Inputs:**
- "What is the stock price of Apple?"
- "Compare the PE ratio of MSFT and AAPL." (Check the output for JSON data suitable for charts)

### Computer Use Demo

Demonstrates how Claude can control a computer via the Computer Use API (Beta). As this runs in a headless environment, it simulates computer interaction tools (logs actions instead of executing them).

**Run:**
```bash
uv run python computer_use/main.py
```

**Example Inputs:**
- "Take a screenshot of the current screen."
- "Move the mouse to the start button and click."

### Autonomous Coding Agent

A coding agent that can read and write files, simulating autonomous coding capabilities. For safety, file operations are restricted to the `autonomous_coding/workspace/` directory.

**Run:**
```bash
uv run python autonomous_coding/main.py
```

**Example Inputs:**
- "Create a file named hello.py that prints 'Hello, LangChain!'."
- "List all files in the workspace."
- "Delete hello.py."

## Project Structure

```
claude_langchain_demos/
├── customer_support/    # Customer Support (RAG + LangGraph StateGraph)
├── financial_analyst/   # Financial Analyst (ReAct Agent + JSON Output)
├── computer_use/        # Computer Use (Mock Tools)
├── autonomous_coding/   # Autonomous Coding (File Tools + Safety Checks)
├── pyproject.toml       # Dependency configuration
├── notes.md             # Development notes
└── README.md            # Documentation
```
