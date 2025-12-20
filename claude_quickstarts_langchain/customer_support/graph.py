import json
import os
from typing import Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from customer_support.state import SupportState, ResponseSchema
from customer_support.rag import retrieve_context

# Load categories
CATEGORIES_PATH = "./customer_support/categories.json"
if not os.path.exists(CATEGORIES_PATH):
    CATEGORIES_PATH = "claude_quickstarts_langchain/customer_support/categories.json"
if not os.path.exists(CATEGORIES_PATH):
    CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

with open(CATEGORIES_PATH, "r") as f:
    CATEGORIES_DATA = json.load(f)

CATEGORY_LIST_STRING = ", ".join([c["id"] for c in CATEGORIES_DATA["categories"]])

SYSTEM_PROMPT = """You are acting as an Anthropic customer support assistant chatbot.
You are chatting with a human user who is asking for help about Anthropic's products and services.
Aim to provide concise and helpful responses while maintaining a polite and professional tone.

To help you answer, we have retrieved the following information (RAG):
{context}

Please provide responses that only use the information you have been given. If no information is available or irrelevant, redirect the user to a human agent.

We also have these customer support categories: {categories}
Check if your response fits into any category and include the category IDs in your response.

If the question is unrelated to Anthropic, redirect the user.

You must return a structured JSON response matching the schema provided.
"""

def retrieve(state: SupportState):
    """Retrieve context based on the last message."""
    messages = state["messages"]
    last_message = messages[-1]
    query = last_message.content if hasattr(last_message, "content") else str(last_message)

    print(f"Retrieving context for: {query}")
    context = retrieve_context(query)
    return {"context": context}

def generate(state: SupportState):
    """Generate a response using the retrieved context."""
    messages = state["messages"]
    context = state["context"]

    # Format system prompt
    formatted_system = SYSTEM_PROMPT.format(
        context=context if context else "No information found.",
        categories=CATEGORY_LIST_STRING
    )

    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.3)
    structured_llm = llm.with_structured_output(ResponseSchema)

    # Construct messages with system prompt
    lc_messages = []
    lc_messages.append(SystemMessage(content=formatted_system))

    for msg in messages:
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
        else:
            lc_messages.append(msg)

    response = structured_llm.invoke(lc_messages)

    return {"response": response}

# Build Graph
workflow = StateGraph(SupportState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()
