import sys
from typing import TypedDict, List, Annotated
import operator
import pandas as pd
import matplotlib.pyplot as plt
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Define tools
@tool
def get_financial_data() -> str:
    """Returns the financial data as a CSV string."""
    try:
        df = pd.read_csv("financial_data.csv")
        return df.to_markdown(index=False)
    except Exception as e:
        return f"Error: {e}"

@tool
def generate_plot(code: str):
    """Executes matplotlib code to generate a plot. The code should use 'df' variable which is pre-loaded."""
    try:
        df = pd.read_csv("financial_data.csv")
        # Unsafe execution for demo purposes
        exec(code, {"pd": pd, "plt": plt, "df": df})
        plt.savefig("plot.png")
        plt.close()
        return "Plot saved to plot.png"
    except Exception as e:
        return f"Error generating plot: {e}"

tools = [get_financial_data, generate_plot]

# Initialize Claude with tools
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
llm_with_tools = llm.bind_tools(tools)

# Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# Nodes
def agent(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent)
tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    print("Financial Data Analyst (Type 'quit' to exit)")
    print("Ask something like: 'Analyze the financial data and show me the trend in revenue.'")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        inputs = {"messages": [HumanMessage(content=user_input)]}
        final_state = app.invoke(inputs)
        print(f"Agent: {final_state['messages'][-1].content}")
