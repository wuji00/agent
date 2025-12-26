from typing import Dict, List, Any, Optional, Literal
from langchain_core.tools import tool
import yfinance as yf

@tool
def get_stock_price(symbol: str):
    """Get the current stock price and info for a given symbol (e.g. AAPL, MSFT)."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol,
            "currentPrice": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),
            "currency": info.get("currency"),
            "longName": info.get("longName")
        }
    except Exception as e:
        return f"Error fetching data for {symbol}: {e}"

@tool
def get_stock_history(symbol: str, period: str = "1mo"):
    """Get historical stock data. period can be 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        # Convert to list of dicts with date as string
        data = []
        for index, row in hist.iterrows():
            data.append({
                "date": index.strftime("%Y-%m-%d"),
                "close": row["Close"],
                "volume": row["Volume"]
            })
        return data
    except Exception as e:
        return f"Error fetching history for {symbol}: {e}"

@tool
def generate_graph_data(
    chartType: Literal["bar", "line", "pie"],
    config: Dict[str, Any],
    data: List[Dict[str, Any]],
    chartConfig: Dict[str, Any]
):
    """
    Generate structured JSON data for creating financial charts.
    Call this tool when you want to visualize the data you have analyzed.

    chartType: The type of chart (bar, line, pie)
    config: {title: str, description: str, ...}
    data: List of data points
    chartConfig: Configuration for data keys (e.g. {revenue: {label: "Revenue"}})
    """
    # In a real app, this would send data to frontend.
    # Here we just return it so it's part of the conversation history or side effect.
    return {
        "status": "generated",
        "chartType": chartType,
        "title": config.get("title"),
        "data_points": len(data)
    }
