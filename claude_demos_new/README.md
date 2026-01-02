# Claude Demos (LangChain/LangGraph Implementation)

This repository contains LangChain and LangGraph implementations of Anthropic's Claude Quickstarts.

## Prerequisites

- Python 3.9+
- `uv` (recommended) or `pip`
- Anthropic API Key

## Setup

1. Install dependencies:
   ```bash
   uv pip install -e .
   # OR
   pip install -e .
   ```

2. Set environment variables:
   Create a `.env` file or export `ANTHROPIC_API_KEY`.

## Demos

### 1. Customer Support Agent
Located in `claude_demos_new/customer_support`.
- Uses a StateGraph (Retrieve -> Generate).
- Uses FAISS for RAG.
- Categorizes inquiries and suggests follow-up actions.

To run:
```bash
python claude_demos_new/customer_support/test_agent.py
```

### 2. Financial Data Analyst
Located in `claude_demos_new/financial_analyst`.
- Uses a ReAct agent with `generate_graph_data` tool.
- Generates structured JSON for Recharts visualization.

To run:
```bash
python claude_demos_new/financial_analyst/test_agent.py
```

### 3. Computer Use Demo
Located in `claude_demos_new/computer_use`.
- Uses a ReAct agent with computer use tools (mocked for this demo).
- Requires `anthropic-beta` headers.

To run:
```bash
python claude_demos_new/computer_use/test_agent.py
```

### 4. Autonomous Coding Agent
Located in `claude_demos_new/autonomous_coding`.
- Uses a ReAct agent with file system tools.
- Constrained to a `workspace` directory for safety.

To run:
```bash
python claude_demos_new/autonomous_coding/test_agent.py
```

## Reference
Original repository: [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts)
