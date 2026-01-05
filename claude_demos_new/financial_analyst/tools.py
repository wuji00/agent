from langchain_core.tools import tool
import random

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
def get_company_financials(ticker: str):
    """Get basic financial data for a company (PE ratio, Market Cap)."""
    # Mock data
    return {
        "ticker": ticker.upper(),
        "pe_ratio": random.uniform(10, 50),
        "market_cap": f"${random.uniform(10, 2000):.2f}B",
        "dividend_yield": f"{random.uniform(0, 5):.2f}%"
    }

@tool
def get_market_trends():
    """Get general market trends."""
    return "The market is currently bullish. Tech stocks are leading the rally."
