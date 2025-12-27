# Customer Support Agent

This agent uses LangGraph and LangChain to implement a customer support bot powered by Claude.
It utilizes a local FAISS vector store as a knowledge base.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the knowledge base:
   ```bash
   python setup_kb.py
   ```
   This will create a `faiss_index` directory with dummy product documents.

3. Run the agent:
   ```bash
   python agent.py
   ```

## Architecture

- **LLM**: `claude-3-haiku-20240307` via `ChatAnthropic`
- **Vector Store**: FAISS with `all-MiniLM-L6-v2` embeddings
- **Framework**: LangGraph for state management and tool execution loop

## Tools

- `lookup_policy`: Retrieves relevant documents from the knowledge base.
