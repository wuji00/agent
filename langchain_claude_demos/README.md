# LangChain + LangGraph Implementations of Claude Quickstarts

This repository contains implementations of four Claude Quickstarts using LangChain and LangGraph.

## Prerequisites

- Python 3.9+
- Anthropic API Key (`ANTHROPIC_API_KEY`)
- `pip` or `uv`

## Installation

```bash
pip install -r requirements.txt
```

## Demos

### 1. Customer Support Agent
A RAG-based agent that retrieves information from a knowledge base (mocked locally using FAISS) and categorizes user queries.

- **Source:** `langchain_claude_demos/customer-support-agent/agent.py`
- **Setup:** Run `python langchain_claude_demos/customer-support-agent/setup_kb.py` to create the local vector store.
- **Run:** `python langchain_claude_demos/customer-support-agent/agent.py`

### 2. Financial Data Analyst
An agent equipped with a `generate_graph_data` tool to analyze financial queries and produce structured data for visualization.

- **Source:** `langchain_claude_demos/financial-data-analyst/analyst.py`
- **Run:** `python langchain_claude_demos/financial-data-analyst/analyst.py`

### 3. Computer Use Demo
A demonstration of the Computer Use capability using LangGraph. The tools are mocked for safety and local execution without a VM.

- **Source:** `langchain_claude_demos/computer-use-demo/computer_agent.py`
- **Run:** `python langchain_claude_demos/computer-use-demo/computer_agent.py`

### 4. Browser Use Demo
A demonstration of browser automation using LangGraph. The tools are mocked.

- **Source:** `langchain_claude_demos/browser-use-demo/browser_agent.py`
- **Run:** `python langchain_claude_demos/browser-use-demo/browser_agent.py`

## Notes
- These implementations focus on the backend logic and agent orchestration using LangGraph.
- Vector stores are local (FAISS) instead of AWS Bedrock to ensure easy reproducibility.
- Complex tools (browser/computer) are mocked as per instructions.
