# Financial Data Analyst

A financial data analyst agent powered by Claude.
It mocks fetching stock data and generating chart configurations suitable for frontend libraries.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```bash
   python agent.py
   ```

## Tools
- `get_stock_price`: Returns mock historical data for a symbol.
- `generate_chart_config`: Converts data into a Recharts-compatible JSON structure.
