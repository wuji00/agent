# Financial Data Analyst

A financial data analysis agent powered by Claude and LangGraph. It can read financial data from a CSV file and generate plots.

## Features
- **Data Access:** Reads a local `financial_data.csv` file.
- **Data Analysis:** Claude analyzes the data to answer questions.
- **Visualization:** Can generate Python code to plot data using Matplotlib and save it as `plot.png`.
- **Tool Use:** Uses LangChain's tool calling capabilities.

## Setup

1. Install dependencies:
   ```bash
   uv pip install pandas matplotlib langchain langgraph langchain-anthropic
   ```

2. Set your Anthropic API Key:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```

## Example Usage
- "Show me the revenue over time."
- "What is the total profit?"
- "Plot the expenses."
