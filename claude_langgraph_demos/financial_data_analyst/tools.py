from langchain_core.tools import tool

@tool
def generate_chart(data: str) -> str:
    """
    Generates a chart based on the provided financial data.
    The input should be a JSON string representing the data to visualize.
    """
    return f"Chart generated for data: {data}"
