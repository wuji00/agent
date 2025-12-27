# LangChain Claude Demos

This directory contains implementations of the Claude Quickstarts demos using **LangChain** and **LangGraph**.

## Demos

1. **[Customer Support Agent](./customer_support)**
   - Uses RAG with a local FAISS vector store.
   - Powered by `claude-3-haiku-20240307`.

2. **[Financial Data Analyst](./financial_analyst)**
   - Mocks stock data retrieval and chart configuration generation.
   - Demonstrates generating structured JSON for frontend visualization.

3. **[Computer Use Demo](./computer_use)**
   - Demonstrates the `computer-use-2024-10-22` beta capability.
   - Uses mock tools for mouse and keyboard actions to run in headless environments.

4. **[Browser Use Demo](./browser_use)**
   - Demonstrates browser automation using mock tools for navigation and interaction.

## General Usage

Each demo has its own `requirements.txt` and `agent.py`.

1. Navigate to the demo directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the agent: `python agent.py`
