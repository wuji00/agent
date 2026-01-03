import json
import random
from typing import Dict, Any, List
from langchain_core.tools import tool

@tool
def get_financial_metrics(ticker: str) -> Dict[str, Any]:
    """
    Get financial metrics for a company by its ticker symbol.
    Returns simulated data for revenue, profit, and margin.
    """
    # Mock data generation
    base = random.randint(100, 1000)
    revenue = [base * (1 + 0.1 * i) + random.randint(-20, 20) for i in range(5)]
    profit = [r * 0.2 + random.randint(-10, 10) for r in revenue]
    margin = [(p/r)*100 for p, r in zip(profit, revenue)]

    return {
        "ticker": ticker.upper(),
        "years": ["2019", "2020", "2021", "2022", "2023"],
        "revenue": revenue,
        "profit": profit,
        "margin": margin
    }

@tool
def get_competitor_comparison(ticker: str) -> List[Dict[str, Any]]:
    """
    Get comparison data for competitors.
    """
    competitors = ["COMP1", "COMP2", "COMP3"]
    data = []
    for comp in competitors:
        data.append({
            "ticker": comp,
            "market_share": random.randint(10, 30),
            "growth": random.randint(5, 15)
        })
    return data
