
import os
import sys
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Load vector store
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore_path = os.path.join(os.path.dirname(__file__), "faiss_index")

if not os.path.exists(vectorstore_path):
    print(f"Error: Vector store not found at {vectorstore_path}. Run setup_kb.py first.")
    sys.exit(1)

vectorstore = FAISS.load_local(
    vectorstore_path,
    embedding_model,
    allow_dangerous_deserialization=True # Safe since we created it ourselves
)
retriever = vectorstore.as_retriever()

# Define tools
from langchain_core.tools import tool

@tool
def lookup_policy(query: str) -> str:
    """Consult the knowledge base to answer customer questions about products, troubleshooting, and warranty."""
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])

tools = [lookup_policy]

# Define the state
class AgentState(TypedDict):
    messages: List[BaseMessage]

# Define the model
# Using a model that supports tools. claude-3-haiku-20240307 is good for quickstarts.
llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Define the nodes
def assistant(state: AgentState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build the graph
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

# Example run
if __name__ == "__main__":
    print("Agent initialized. Type 'q' to quit.")

    # Simple CLI loop
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["q", "quit", "exit"]:
                break

            initial_state = {"messages": [HumanMessage(content=user_input)]}

            # Streaming output
            print("Assistant: ", end="", flush=True)
            for event in graph.stream(initial_state):
                for key, value in event.items():
                    if "messages" in value:
                        last_msg = value["messages"][-1]
                        if isinstance(last_msg, AIMessage) and last_msg.content:
                            print(last_msg.content)
            print()

        except KeyboardInterrupt:
            break
