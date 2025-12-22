# Claude Quickstarts - LangChain & LangGraph Implementation

This repository contains implementations of 4 key Claude Quickstarts using LangChain and LangGraph.

## Demos

### 1. Customer Support Agent
Located in `customer_support_agent/`.
- **Description**: A RAG-based support agent that retrieves info from a local knowledge base and categorizes inquiries.
- **Implementation**: Uses FAISS for vector storage and LangGraph for the workflow.
- **Run**: `python customer_support_agent/agent.py`

### 2. Financial Data Analyst
Located in `financial_data_analyst/`.
- **Description**: An agent that analyzes financial queries and generates structured data for charts using a defined tool.
- **Implementation**: Uses `generate_graph_data` tool with structured output validation.
- **Run**: `python financial_data_analyst/agent.py`

### 3. Computer Use Demo
Located in `computer_use_demo/`.
- **Description**: Demonstrates the "Computer Use" capability with mock tools.
- **Implementation**: Defines `computer`, `bash`, and `edit` tools and uses a LangGraph agent loop.
- **Run**: `python computer_use_demo/agent.py`

### 4. Browser Use Demo
Located in `browser_use_demo/`.
- **Description**: Demonstrates "Browser Use" capability with mock browser tools.
- **Implementation**: Defines `browser` tool with various actions.
- **Run**: `python browser_use_demo/agent.py`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Note: `torch` and `transformers` are required for embeddings in the Customer Support Agent.

2. Set your Anthropic API Key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

3. Run any agent:
   ```bash
   python customer_support_agent/agent.py
   ```
