from langchain_core.tools import tool
import random
from datetime import datetime, timedelta

@tool
def get_stock_price(ticker: str):
    """Get the current stock price for a given ticker symbol (e.g. AAPL, MSFT)."""
    # Mock data
    prices = {
        "AAPL": 150.0,
        "MSFT": 300.0,
        "GOOGL": 2800.0,
        "AMZN": 3400.0,
        "TSLA": 700.0
    }
    price = prices.get(ticker.upper())
    if price:
        # Add some random fluctuation
        price += random.uniform(-5, 5)
        return f"{ticker.upper()} price: ${price:.2f}"

    return f"{ticker.upper()} price: ${random.uniform(10, 1000):.2f}"

@tool
def get_stock_history(ticker: str, days: int = 30):
    """
    Get historical stock prices for a given ticker symbol.
    Returns a JSON list of objects with 'date' and 'price' keys, suitable for charting.
    days: Number of days of history to return (default 30).
    """
    base_price = 100.0
    if ticker.upper() == "AAPL": base_price = 150.0
    elif ticker.upper() == "MSFT": base_price = 300.0
    elif ticker.upper() == "GOOGL": base_price = 2800.0

    history = []
    today = datetime.now()

    current_price = base_price
    for i in range(days):
        date = (today - timedelta(days=days-i)).strftime("%Y-%m-%d")
        # Random walk
        change = random.uniform(-0.02, 0.02)
        current_price = current_price * (1 + change)
        history.append({
            "date": date,
            "price": round(current_price, 2)
        })

    return history

@tool
def get_company_financials(ticker: str):
    """Get basic financial data for a company (PE ratio, Market Cap)."""
    # Mock data
    return {
        "ticker": ticker.upper(),
        "pe_ratio": round(random.uniform(10, 50), 2),
        "market_cap": f"${random.uniform(10, 2000):.2f}B",
        "dividend_yield": f"{random.uniform(0, 5):.2f}%"
    }

@tool
def get_market_trends():
    """Get general market trends."""
    return "The market is currently bullish. Tech stocks are leading the rally."
