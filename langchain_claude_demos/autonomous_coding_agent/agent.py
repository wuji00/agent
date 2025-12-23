from typing import TypedDict, List, Annotated
import operator
import json
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END

# Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    project_dir: str
    feature_list: List[str]
    current_feature_index: int

# Initialize Claude
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

# Nodes
def initializer(state: AgentState):
    """Initializes the project and feature list."""
    project_dir = state.get("project_dir", "my_project")
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    # Mocking the creation of feature list
    feature_list = [
        "Setup React project",
        "Create Header component",
        "Create Footer component",
        "Implement Login page"
    ]

    with open(os.path.join(project_dir, "feature_list.json"), "w") as f:
        json.dump(feature_list, f)

    return {
        "messages": [HumanMessage(content="Project initialized. Feature list created.")],
        "feature_list": feature_list,
        "current_feature_index": 0
    }

def coding_agent(state: AgentState):
    """Implement features one by one."""
    feature_list = state["feature_list"]
    idx = state["current_feature_index"]

    if idx >= len(feature_list):
        return {"messages": [HumanMessage(content="All features implemented.")]}

    feature = feature_list[idx]

    # Simulate coding
    prompt = f"Implement feature: {feature}. Write the code."
    response = llm.invoke([HumanMessage(content=prompt)])

    # In a real agent, we would write files here based on response
    # For demo, we just log it

    return {
        "messages": [response],
        "current_feature_index": idx + 1
    }

def supervisor(state: AgentState):
    """Decides what to do next."""
    idx = state.get("current_feature_index", 0)
    feature_list = state.get("feature_list", [])

    if not feature_list:
        return "initializer"

    if idx < len(feature_list):
        return "coding_agent"

    return END

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("initializer", initializer)
workflow.add_node("coding_agent", coding_agent)

workflow.set_entry_point("initializer")

workflow.add_conditional_edges(
    "initializer",
    lambda x: "coding_agent"
)

workflow.add_conditional_edges(
    "coding_agent",
    supervisor,
    {
        "coding_agent": "coding_agent",
        END: END
    }
)

app = workflow.compile()

if __name__ == "__main__":
    print("Autonomous Coding Agent Demo")

    inputs = {
        "project_dir": "autonomous_demo_project",
        "messages": [HumanMessage(content="Start building.")]
    }

    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Finished node: {key}")
            if "messages" in value:
                print(f"Message: {value['messages'][-1].content[:100]}...")
