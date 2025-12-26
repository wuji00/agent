import json
import os
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- Data Models ---
class RedirectToAgent(BaseModel):
    should_redirect: bool = Field(description="Whether to redirect to a human agent")
    reason: Optional[str] = Field(None, description="Reason for redirection")

class ResponseSchema(BaseModel):
    thinking: str = Field(description="Brief explanation of reasoning")
    response: str = Field(description="Concise response to the user")
    user_mood: Literal["positive", "neutral", "negative", "curious", "frustrated", "confused"] = Field(description="User's mood")
    suggested_questions: List[str] = Field(description="Suggested follow-up questions")
    debug: dict = Field(description="Debug information")
    matched_categories: Optional[List[str]] = Field(description="List of matched category IDs")
    redirect_to_agent: Optional[RedirectToAgent] = Field(description="Redirection details")

# --- RAG Setup (Mock/Local) ---
def setup_vector_store():
    # Dummy knowledge base
    docs = [
        Document(page_content="To reset your password, go to Settings > Account > Password and click 'Reset'."),
        Document(page_content="We accept Visa, Mastercard, and American Express. Billing occurs monthly."),
        Document(page_content="Our API rate limits are 1000 requests per minute for the Pro plan."),
        Document(page_content="To contact human support, email support@example.com or call 1-800-123-4567."),
        Document(page_content="Anthropic's latest model is Claude 3.5 Sonnet, optimized for speed and intelligence.")
    ]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

# Global vector store instance (lazy loaded)
_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        print("Initializing Vector Store...")
        _vector_store = setup_vector_store()
    return _vector_store

# Define RAG as a tool for the agent
@tool
def retrieve_knowledge_base(query: str):
    """Retrieve relevant information from the knowledge base."""
    try:
        vector_store = get_vector_store()
        results = vector_store.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in results])
        if not context:
            return "No information found."
        return context
    except Exception as e:
        print(f"RAG Error: {e}")
        return "Error retrieving information."

# --- Agent Logic ---

def customer_support_agent(query: str, mock_llm=None):
    # Load categories
    try:
        with open("customer_support_categories.json", "r") as f:
            categories_data = json.load(f)
            categories_list = ", ".join([c["id"] for c in categories_data["categories"]])
    except FileNotFoundError:
        categories_list = "technical_support, billing, account_management, feature_request, general_inquiry"

    # Initialize LLM
    if mock_llm:
        llm = mock_llm
    else:
        llm = ChatAnthropic(model=MODEL_NAME, temperature=0.3)

    tools = [retrieve_knowledge_base]

    # System Prompt
    system_prompt = f"""You are acting as an Anthropic customer support assistant chatbot.

    You have access to a knowledge base via the 'retrieve_knowledge_base' tool.
    ALWAYS use this tool to find information before answering.

    Please provide responses that only use the information you have been given. If no information is available or if the information is not relevant for answering the question, you can redirect the user to a human agent.

    To help with our internal classification, categorize inquiries into: {categories_list}.

    You must format your entire response as a valid JSON object matching the following structure:
    {{
      "thinking": "Brief explanation of reasoning",
      "response": "Concise response",
      "user_mood": "positive|neutral|negative|curious|frustrated|confused",
      "suggested_questions": ["Question 1?", "Question 2?"],
      "debug": {{"context_used": true|false}},
      "matched_categories": ["category_id"],
      "redirect_to_agent": {{"should_redirect": boolean, "reason": "reason"}}
    }}
    """

    agent = create_react_agent(llm, tools)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    final_output = None

    try:
        for event in agent.stream({"messages": messages}, stream_mode="values"):
            message = event["messages"][-1]
            if isinstance(message, AIMessage) and not message.tool_calls:
                final_output = message.content
    except Exception as e:
        print(f"Error during agent execution: {e}")
        return None

    if final_output:
        try:
            # Clean up potential markdown code blocks if the LLM wraps the JSON
            cleaned_output = final_output.strip()
            if cleaned_output.startswith("```json"):
                cleaned_output = cleaned_output[7:]
            if cleaned_output.endswith("```"):
                cleaned_output = cleaned_output[:-3]

            # Parse JSON
            parsed_data = json.loads(cleaned_output)
            return ResponseSchema(**parsed_data)
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
            print("Raw output:", final_output)
            return None
        except Exception as e:
            print(f"Validation Error: {e}")
            return None
    return None

# --- Mock LLM ---
class MockChatModel(BaseChatModel):
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs) -> ChatResult:
        last_msg = messages[-1]

        # If it's a ToolMessage (result of RAG), return the final JSON
        if isinstance(last_msg, ToolMessage):
             content = """
            {
                "thinking": "User is asking about password reset. I have context for that.",
                "response": "To reset your password, please navigate to Settings > Account > Password and click 'Reset'.",
                "user_mood": "curious",
                "suggested_questions": ["How do I change my email?", "Is 2FA supported?"],
                "debug": {"context_used": true},
                "matched_categories": ["account_management"],
                "redirect_to_agent": {"should_redirect": false}
            }
            """
             return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

        # If it's the initial query (HumanMessage or System+Human), call the tool
        # We need to check if we already called the tool.
        # In a real agent loop, the history is passed.
        # If the last message is Human, we call tool.

        tool_call = {
            "name": "retrieve_knowledge_base",
            "args": {"query": "reset password"},
            "id": "call_mock_rag_123"
        }

        msg = AIMessage(content="", tool_calls=[tool_call])
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self) -> str:
        return "mock"

    def bind_tools(self, tools, **kwargs):
        return self

# --- Main Execution ---

if __name__ == "__main__":

    # Check for API Key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    use_mock = not api_key or api_key == "dummy_key_for_now_since_i_cant_set_real_one"

    if use_mock:
        print("⚠️  No valid ANTHROPIC_API_KEY found. Using Mock LLM for demonstration.")
        llm = MockChatModel()
    else:
        llm = None # Default to real one

    # Test queries
    queries = [
        "How do I reset my password?",
    ]

    print("--- Starting Customer Support Agent Demo ---")

    for q in queries:
        print(f"\nUser Query: {q}")
        result = customer_support_agent(q, mock_llm=llm)
        if result:
            print(f"Thinking: {result.thinking}")
            print(f"Response: {result.response}")
            print(f"Mood: {result.user_mood}")
            print(f"Categories: {result.matched_categories}")
            if result.redirect_to_agent and result.redirect_to_agent.should_redirect:
                print(f"Redirecting: YES ({result.redirect_to_agent.reason})")
            else:
                print("Redirecting: NO")
        else:
            print("Failed to get response.")
