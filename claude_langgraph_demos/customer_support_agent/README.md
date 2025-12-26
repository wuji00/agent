# Customer Support Agent

This directory contains a LangGraph implementation of the Customer Support Agent.

## Setup

1.  Ensure you have run `setup_kb.py` to create the local FAISS index.
    ```bash
    python setup_kb.py
    ```

## Running the Agent

You can run the agent interactively:

```bash
python agent.py
```

## Description

The agent uses a local FAISS vector store (simulating the Bedrock Knowledge Base) to retrieve relevant context. It then uses Claude (via LangChain's `ChatAnthropic`) to generate a response, structured according to a Pydantic model.

The agent handles:
*   Context Retrieval (RAG)
*   Response Generation
*   Categorization
*   Mood Detection
*   Redirection Logic
