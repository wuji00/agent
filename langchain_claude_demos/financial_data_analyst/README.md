# Financial Data Analyst Demo

This demo implements a Financial Data Analyst using LangChain and LangGraph. It is capable of generating structured data for charts based on user queries.

## Features

-   **Tool Use:** Uses a custom tool `generate_graph_data` to create visualization data.
-   **Structured Output:** Generates JSON data suitable for frontend charting libraries (like Recharts, used in the reference implementation).
-   **Financial Domain Knowledge:** Prompted to act as a financial data expert.

## Setup

1.  Dependencies:
    ```bash
    pip install langchain langchain-anthropic langchain-community langgraph
    ```
2.  Set `ANTHROPIC_API_KEY`.

## Usage

Run the script:

```bash
python financial_data_analyst.py
```
