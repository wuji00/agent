import json
import os
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from .state import AgentState, CustomerSupportResponse
from .utils import RAGSystem

# Load categories
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "categories.json"), "r") as f:
    CATEGORIES_DATA = json.load(f)

CATEGORY_LIST_STRING = ", ".join([c["id"] for c in CATEGORIES_DATA["categories"]])

class CustomerSupportAgent:
    def __init__(self, model_name: str = "claude-3-haiku-20240307"):
        self.rag = RAGSystem(os.path.join(current_dir, "knowledge.txt"))
        self.llm = ChatAnthropic(model=model_name, temperature=0.3)
        self.workflow = self._build_workflow()

    def _retrieve(self, state: AgentState) -> Dict[str, Any]:
        """Retrieve context based on the last user message."""
        messages = state.messages
        last_message = messages[-1]["content"] if messages else ""
        context = self.rag.retrieve(last_message)
        return {"context": context}

    def _generate(self, state: AgentState) -> Dict[str, Any]:
        """Generate response using Claude."""
        context = state.context

        # Construct system prompt
        system_prompt = f"""You are acting as an Anthropic customer support assistant chatbot.

To help you answer the user's question, we have retrieved the following information:
{context if context else "No information found for this query."}

Please provide responses that only use the information you have been given. If no information is available or if the information is not relevant, you can redirect the user to a human agent.

To help with our internal classification, categorize inquiries. The available categories are: {CATEGORY_LIST_STRING}

You must format your response as a valid JSON object matching the following structure:
{{
    "thinking": "Brief explanation of your reasoning",
    "response": "Your concise response to the user",
    "user_mood": "positive|neutral|negative|curious|frustrated|confused",
    "suggested_questions": ["Question 1?", "Question 2?"],
    "debug": {{ "context_used": true|false }},
    "matched_categories": ["category_id"],
    "redirect_to_agent": {{ "should_redirect": boolean, "reason": "optional reason" }}
}}
"""

        # We need to construct the message history for LangChain
        # Assuming state.messages is a list of dicts {role: "user"|"assistant", content: "..."}
        lc_messages = [SystemMessage(content=system_prompt)]
        for msg in state.messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))

        # Force JSON output by appending a prefill or using structured output
        # Here we follow the prompt engineering approach of the reference, but we can also use with_structured_output if the model supports it well.
        # The reference explicitly prompts for JSON.

        # We'll use the LLM to generate the JSON string directly, then parse it.
        # Ideally we use `with_structured_output` if we want robust parsing, but let's try to stick to the prompt-based approach first or combine them.
        # Given the complex schema, `with_structured_output` is safer.

        structured_llm = self.llm.with_structured_output(CustomerSupportResponse)
        response = structured_llm.invoke(lc_messages)

        return {"response": response}

    def _build_workflow(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("generate", self._generate)

        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    def invoke(self, messages: List[Dict[str, str]]):
        initial_state = AgentState(messages=messages)
        return self.workflow.invoke(initial_state)
