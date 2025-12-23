import os
import sys
from typing import TypedDict, List, Annotated
import operator

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langgraph.graph import StateGraph, END

# Define state
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    mood: str
    context: str

# Load vector store
INDEX_PATH = "faiss_index"
if not os.path.exists(INDEX_PATH):
    print("Error: Vector store not found. Run ingest.py first.")
    sys.exit(1)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever()

# Initialize Claude
# Note: Ensure ANTHROPIC_API_KEY is set in environment
llm = ChatAnthropic(model="claude-3-haiku-20240307")

# Nodes
def detect_mood(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a mood detector. Analyze the user's message and determine their mood. Return only one word: 'Positive', 'Neutral', or 'Negative'."),
        ("user", "{text}")
    ])
    chain = prompt | llm
    response = chain.invoke({"text": last_message.content})
    mood = response.content.strip()
    return {"mood": mood}

def retrieve_context(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    docs = retriever.invoke(last_message.content)
    context = "\n".join([doc.page_content for doc in docs])
    return {"context": context}

def generate_response(state: AgentState):
    messages = state["messages"]
    mood = state.get("mood", "Neutral")
    context = state.get("context", "")

    system_prompt = f"""You are a helpful customer support agent.
    The user's current mood is detected as: {mood}.
    Use the following context to answer the user's question:

    {context}

    If the context doesn't contain the answer, politely say you don't know but offer to connect them to a human agent.
    Adjust your tone based on the user's mood. If Negative, be empathetic and apologetic. If Positive, be cheerful.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}")
    ])

    chain = prompt | llm
    response = chain.invoke({"messages": messages})
    return {"messages": [response]}

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("detect_mood", detect_mood)
workflow.add_node("retrieve", retrieve_context)
workflow.add_node("generate", generate_response)

workflow.set_entry_point("detect_mood")
workflow.add_edge("detect_mood", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

if __name__ == "__main__":
    print("Customer Support Agent (Type 'quit' to exit)")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        inputs = {"messages": [HumanMessage(content=user_input)]}
        # Use invoke to get the final state directly
        final_state = app.invoke(inputs)
        print(f"Agent ({final_state['mood']}): {final_state['messages'][-1].content}")
