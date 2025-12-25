# Financial Data Analyst

This directory contains a LangGraph implementation of the Financial Data Analyst.

## Running the Agent

You can run the agent interactively:

```bash
python agent.py
```

## Description

The agent is designed to be a financial data visualization expert. It uses a tool `generate_graph_data` to generate structured JSON for charts.

The implementation uses LangGraph's prebuilt `ToolNode` pattern.
The system prompt guides Claude to use the tool correctly to visualize financial data.
