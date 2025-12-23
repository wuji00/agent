# LangChain & LangGraph Claude Demos

This repository contains four demos inspired by [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts), reimplemented using [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/).

## Demos

1.  **[Customer Support Agent](customer_support_agent/)**
    -   A RAG-based support agent that uses a local vector store (FAISS) to answer questions and detects user mood.

2.  **[Financial Data Analyst](financial_data_analyst/)**
    -   An agent that can analyze financial data from CSV files and generate plots using Python code execution tools.

3.  **[Computer Use Demo](computer_use_demo/)**
    -   A demonstration of the "Computer Use" capability using mock tools (Screen, Mouse, Keyboard) within a LangGraph agent loop.

4.  **[Autonomous Coding Agent](autonomous_coding_agent/)**
    -   A multi-step agent workflow that plans a project (creating a feature list) and then iteratively implements each feature.

## Getting Started

### Prerequisites

-   Python 3.9+
-   `uv` (recommended) or `pip`
-   Anthropic API Key

### Installation

1.  Create a virtual environment:
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    uv pip install langchain langgraph langchain-anthropic langchain-community faiss-cpu langchain-huggingface sentence-transformers pandas matplotlib
    ```

3.  Set your API key:
    ```bash
    export ANTHROPIC_API_KEY=your_api_key_here
    ```

### Running a Demo

Navigate to the specific demo folder and follow the `README.md` inside. For example:

```bash
cd customer_support_agent
python ingest.py  # specific setup for this demo
python agent.py
```
