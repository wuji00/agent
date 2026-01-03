from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import categorize, retrieve, generate

def create_customer_support_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("categorize", categorize)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("categorize")

    workflow.add_edge("categorize", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()
