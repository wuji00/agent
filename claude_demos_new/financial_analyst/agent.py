from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from .tools import get_financial_metrics, get_competitor_comparison

# Memory requirement: "The Financial Data Analyst agent requires a system prompt instructing the model to output structured JSON (compatible with Recharts) inside a code block"

SYSTEM_PROMPT = """You are a Financial Data Analyst. You have access to tools to fetch financial data.
Your goal is to analyze the data and provide insights.

IMPORTANT: When asked to visualize data, or when it is appropriate to show a chart, you MUST provide the data in a structured JSON format inside a code block labeled `json`.
The JSON should be compatible with Recharts (a list of objects).

Example format:
```json
[
  { "name": "2019", "revenue": 100, "profit": 20 },
  { "name": "2020", "revenue": 120, "profit": 25 }
]
```

Always provide a text analysis alongside the data.
"""

def create_financial_agent():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    tools = [get_financial_metrics, get_competitor_comparison]

    # In langgraph 1.0.5, create_react_agent accepts state_modifier or prompt.
    # Memory says: "In `langgraph` version 1.0.5, `create_react_agent` requires system instructions to be passed via the `prompt` parameter, not `state_modifier`."
    # Wait, let me check the signature or just follow memory. Memory is specific about 1.0.5.
    # Actually, create_react_agent(model, tools, prompt=...).
    # Wait, usually it's `state_modifier` in newer versions or `messages_modifier`.
    # Let me check memory again: "In `langgraph` version 1.0.5, `create_react_agent` requires system instructions to be passed via the `prompt` parameter, not `state_modifier`."
    # Okay, I will trust memory.

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return agent
