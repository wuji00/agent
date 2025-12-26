import json
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

from autonomous_coding.prompts import INITIALIZER_PROMPT, CODER_SYSTEM_PROMPT
from autonomous_coding.tools import get_tools, WORKSPACE_DIR
from langgraph.prebuilt import create_react_agent

class AgentState(TypedDict):
    request: str
    features: List[str]
    completed_features: List[str]
    current_task: Optional[str]
    messages: List[HumanMessage] # For the coder history

def initializer(state: AgentState):
    request = state["request"]
    print("Initializing project...")

    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)
    # Force JSON output
    response = llm.invoke(INITIALIZER_PROMPT.format(request=request))
    content = response.content

    # Simple parsing (robustness would use structured output)
    try:
        data = json.loads(content)
        features = data.get("features", [])
    except:
        # Fallback if markdown json
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
            data = json.loads(content)
            features = data.get("features", [])
        else:
            features = [content] # Fallback

    return {"features": features, "completed_features": []}

def planner(state: AgentState):
    features = state["features"]
    completed = state["completed_features"]

    remaining = [f for f in features if f not in completed]

    if not remaining:
        return {"current_task": None}

    task = remaining[0]
    print(f"Planning next task: {task}")
    return {"current_task": task}

def coder(state: AgentState):
    task = state["current_task"]
    completed = state["completed_features"]

    print(f"Coding task: {task}")

    tools = get_tools()
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

    system_msg = CODER_SYSTEM_PROMPT.format(
        project_dir=str(WORKSPACE_DIR),
        current_task=task
    )

    # We use a single-run react agent for this task
    agent = create_react_agent(llm, tools, state_modifier=system_msg)

    # Run the agent until it stops
    result = agent.invoke({"messages": [HumanMessage(content=f"Please implement: {task}. When done, just say 'Task Completed'.")]})

    # We assume it succeeded
    return {
        "completed_features": completed + [task],
        "current_task": None
    }

def route(state: AgentState):
    if state["current_task"] is None:
        if len(state["completed_features"]) == len(state["features"]) and len(state["features"]) > 0:
            return END
        else:
             if len(state["features"]) == 0:
                 return END
             return "coder"
    return "coder"

workflow = StateGraph(AgentState)
workflow.add_node("initializer", initializer)
workflow.add_node("planner", planner)
workflow.add_node("coder", coder)

workflow.set_entry_point("initializer")
workflow.add_edge("initializer", "planner")

def check_finished(state):
    if state["current_task"] is None:
        return END
    return "coder"

workflow.add_conditional_edges("planner", check_finished)
workflow.add_edge("coder", "planner")

app = workflow.compile()
