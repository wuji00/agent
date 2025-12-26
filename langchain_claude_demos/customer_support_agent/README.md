# Customer Support Agent Demo

This demo implements a Customer Support Agent using LangChain and LangGraph, inspired by the Anthropic Claude Quickstart.

## Features

-   **RAG (Retrieval Augmented Generation):** Retrieves relevant context from a knowledge base to answer user queries.
-   **Categorization:** Categorizes user inquiries into predefined categories.
-   **Sentiment Analysis:** Analyzes the user's mood.
-   **Human Handoff:** Determines if the query requires human intervention.
-   **Structured Output:** Returns a structured JSON response.

## Setup

1.  Ensure you have the required dependencies installed:
    ```bash
    pip install langchain langchain-anthropic langchain-community langgraph faiss-cpu langchain-huggingface
    ```
2.  Set your Anthropic API Key:
    ```bash
    export ANTHROPIC_API_KEY=your_api_key
    ```
3.  (Optional) For the RAG component, this demo uses a local FAISS vector store with HuggingFace embeddings instead of AWS Bedrock.

## Usage

Run the agent script:

```bash
python customer_support_agent.py
```
