# LangChain Claude Demos

This repository contains four implementations of Anthropic's Claude Quickstarts, rewritten using **LangChain** and **LangGraph**.

## Demos

1.  **[Customer Support Agent](./customer_support_agent/)**: A RAG-based support agent that categorizes queries and handles human handoff.
2.  **[Financial Data Analyst](./financial_data_analyst/)**: An agent capable of generating structured data for financial visualizations.
3.  **[Computer Use Demo](./computer_use_demo/)**: An agent that demonstrates computer control capabilities (mocked for this environment).
4.  **[Browser Use Demo](./browser_use_demo/)**: An agent that demonstrates browser automation capabilities (mocked for this environment).

## Prerequisites

-   Python 3.9+
-   Anthropic API Key

## Installation

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Set your API Key:
    ```bash
    export ANTHROPIC_API_KEY=your_key_here
    ```

## Usage

Navigate to each demo folder and run the python script. Refer to the README in each folder for specific instructions.
