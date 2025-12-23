# Customer Support Agent

This is a Python implementation of the Customer Support Agent demo using LangGraph and LangChain.

## Features
- **RAG (Retrieval Augmented Generation):** Uses FAISS and SentenceTransformers (via `langchain-huggingface`) to retrieve context from a local knowledge base.
- **Mood Detection:** Analyzes user input to detect mood (Positive, Neutral, Negative) and adjusts the response tone.
- **State Management:** Uses LangGraph to manage the conversation state and workflow.

## Setup

1. Install dependencies:
   ```bash
   uv pip install langchain langgraph langchain-anthropic langchain-community faiss-cpu langchain-huggingface sentence-transformers
   ```

2. Set your Anthropic API Key:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

3. Ingest data (creates the vector store):
   ```bash
   python ingest.py
   ```

4. Run the agent:
   ```bash
   python agent.py
   ```

## Workflow

1. **User Input:** The user provides a query.
2. **Mood Detection:** The agent analyzes the query to determine the user's mood.
3. **Retrieval:** The agent retrieves relevant information from the local FAISS index.
4. **Generation:** The agent generates a response using Claude, considering the context and the user's mood.
