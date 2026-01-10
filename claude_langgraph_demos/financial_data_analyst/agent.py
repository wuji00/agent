import json
import os
from typing import Annotated, TypedDict, List, Optional, Dict, Any, Union
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# --- Tools ---

@tool
def generate_graph_data(
    chartType: str,
    config: Dict[str, Any],
    data: List[Dict[str, Any]],
    chartConfig: Dict[str, Any]
):
    """
    Generate structured JSON data for creating financial charts and graphs.

    Args:
        chartType: The type of chart to generate. Allowed values: "bar", "multiBar", "line", "pie", "area", "stackedArea".
        config: Configuration for the chart (title, description, trend, footer, totalLabel, xAxisKey).
        data: The actual data points for the chart.
        chartConfig: Configuration for chart labels and stacking.
    """
    # In a real app, this might store data or do some processing.
    # Here we just return it so the agent sees it "generated" successfully.
    return {
        "status": "success",
        "chart_data": {
            "chartType": chartType,
            "config": config,
            "data": data,
            "chartConfig": chartConfig
        }
    }

# --- State ---

class AgentState(TypedDict):
    messages: List[BaseMessage]

# --- Nodes ---

def call_model(state: AgentState):
    messages = state["messages"]

    # System prompt
    system_prompt = """You are a financial data visualization expert. Your role is to analyze financial data and create clear, meaningful visualizations using generate_graph_data tool:

Here are the chart types available and their ideal use cases:

1. LINE CHARTS ("line") - Time series data showing trends
2. BAR CHARTS ("bar") - Single metric comparisons
3. MULTI-BAR CHARTS ("multiBar") - Multiple metrics comparison
4. AREA CHARTS ("area") - Volume or quantity over time
5. STACKED AREA CHARTS ("stackedArea") - Component breakdowns over time
6. PIE CHARTS ("pie") - Distribution analysis

When generating visualizations:
1. Structure data correctly based on the chart type
2. Use descriptive titles and clear descriptions
3. Include trend information when relevant (percentage and direction)
4. Add contextual footer notes
5. Use proper data keys that reflect the actual metrics

Always:
- Generate real, contextually appropriate data
- Use proper financial formatting
- Include relevant trends and insights
- Structure data exactly as needed for the chosen chart type
- Choose the most appropriate visualization for the data

Focus on clear financial insights and let the visualization enhance understanding."""

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    llm_with_tools = llm.bind_tools([generate_graph_data])

    # Ensure system prompt is first
    from langchain_core.messages import SystemMessage
    prompt_messages = [SystemMessage(content=system_prompt)] + messages

    response = llm_with_tools.invoke(prompt_messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# --- Graph ---

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
tool_node = ToolNode([generate_graph_data])
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    import sys
    from langchain_core.runnables import RunnableLambda

    # Fake LLM for testing
    class FakeLLM:
        def bind_tools(self, tools, **kwargs):
            return self

        def invoke(self, input, config=None):
             # Just return a message saying we generated a chart if requested
             messages = input if isinstance(input, list) else input.get("messages", [])
             last_msg = messages[-1]
             if "chart" in last_msg.content.lower():
                 return AIMessage(content="I generated the chart.", tool_calls=[
                     {"name": "generate_graph_data", "args": {
                         "chartType": "bar",
                         "config": {"title": "Sales"},
                         "data": [{"month": "Jan", "sales": 100}],
                         "chartConfig": {}
                     }, "id": "call_1"}
                 ])
             elif isinstance(last_msg, ToolMessage):
                 return AIMessage(content="Here is the chart.")
             else:
                 return AIMessage(content="How can I help you?")

    # Mock ChatAnthropic for test mode
    if os.environ.get("TEST_MODE"):
        print("Running in TEST MODE")
        # Monkey patch ChatAnthropic
        global ChatAnthropic
        ChatAnthropic = lambda **kwargs: FakeLLM()
        # Re-compile app with mocked LLM (nodes need to be re-defined if they capture ChatAnthropic at definition time,
        # but here call_model is a function that instantiates ChatAnthropic, so it should pick up the global override)


    print("Financial Data Analyst (Type 'quit' to exit)")

    messages = []

    # Non-interactive mode handling
    import select
    if select.select([sys.stdin,],[],[],0.0)[0]:
         # Input available
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                user_input = line.strip()
                if not user_input or user_input.lower() in ["quit", "exit"]:
                    break

                print(f"User: {user_input}")
                messages.append(HumanMessage(content=user_input))
                state = {"messages": messages}

                print("... thinking ...")

                for event in app.stream(state):
                    for key, value in event.items():
                        if key == "agent":
                            msg = value["messages"][0]
                            if msg.tool_calls:
                                print(f"Tool Call: {msg.tool_calls[0]['name']}")
                            else:
                                print(f"Assistant: {msg.content}")
                                messages.append(msg)
                        elif key == "tools":
                            pass
        except Exception as e:
            # print(f"Error: {e}")
            # If error is about generate_graph_data missing args, it might be the ToolNode execution
            # In test mode, we might get errors if fake llm tool call args don't match exactly what ToolNode expects
            # But the fake llm provides args.
            # The previous error "generate_graph_data() missing 1 required positional argument: 'config'" suggests
            # that maybe ToolNode invokes the function and there's a mismatch.
            # generate_graph_data signature is (chartType, config, data, chartConfig)
            # The fake llm provided all 4.
            # Maybe the error comes from something else.
            # Let's print the traceback or error to debug if it happens again
            import traceback
            traceback.print_exc()

    else:
        while True:
            try:
                user_input = input("User: ")
            except EOFError:
                break
            if user_input.lower() in ["quit", "exit"]:
                break

            messages.append(HumanMessage(content=user_input))
            state = {"messages": messages}

            print("... thinking ...")
            for event in app.stream(state):
                for key, value in event.items():
                    if key == "agent":
                        msg = value["messages"][0]
                        if msg.tool_calls:
                            print(f"Tool Call: {msg.tool_calls[0]['name']}")
                        else:
                            print(f"Assistant: {msg.content}")
                            messages.append(msg)
                    elif key == "tools":
                        # Tool output is internal, but we can inspect if needed
                        pass
