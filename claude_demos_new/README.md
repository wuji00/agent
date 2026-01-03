# Claude Quickstart Demos (LangChain & LangGraph)

This directory contains LangChain and LangGraph implementations of four Anthropic Claude quickstart demos.

## 1. Customer Support Agent

A RAG-based customer support agent that categorizes queries, retrieves information from a knowledge base, and generates responses.

- **Location**: `claude_demos_new/customer_support`
- **Architecture**: LangGraph `StateGraph` (Categorize -> Retrieve -> Generate)
- **Data**: Uses mock `knowledge.txt` and `categories.json` in `data/` directory.
- **Run**: `python -m claude_demos_new.customer_support.demo`

## 2. Financial Data Analyst

A financial analyst agent that can fetch simulated financial data and provide insights with structured JSON for visualization.

- **Location**: `claude_demos_new/financial_analyst`
- **Architecture**: LangGraph `create_react_agent`
- **Features**: Outputs Recharts-compatible JSON.
- **Run**: `python -m claude_demos_new.financial_analyst.demo`

## 3. Computer Use Demo

A demo showcasing the "Computer Use" capability (simulated/mocked for this environment) using LangChain tools.

- **Location**: `claude_demos_new/computer_use`
- **Architecture**: LangGraph `create_react_agent` with specialized tools.
- **Tools**: Mock `computer_tool`, `bash_tool`, `edit_tool`.
- **Run**: `python -m claude_demos_new.computer_use.demo`

## 4. Autonomous Coding Agent

An autonomous coding agent capable of performing file system operations within a safe workspace.

- **Location**: `claude_demos_new/autonomous_coding`
- **Architecture**: LangGraph `create_react_agent`
- **Tools**: `read_file`, `write_file`, `list_files`, `delete_file` (with path validation).
- **Run**: `python -m claude_demos_new.autonomous_coding.demo`

## Setup

1.  Install dependencies:
    ```bash
    pip install langchain-anthropic langchain-community langchain-huggingface langgraph faiss-cpu sentence-transformers langchain-text-splitters python-dotenv
    ```

2.  Set `ANTHROPIC_API_KEY` in your environment.

3.  Run the demos as indicated above.
