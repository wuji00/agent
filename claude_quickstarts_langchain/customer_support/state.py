from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class RedirectToAgent(BaseModel):
    should_redirect: bool
    reason: Optional[str] = None

class DebugInfo(BaseModel):
    context_used: bool

class ResponseSchema(BaseModel):
    thinking: str = Field(description="Brief explanation of reasoning")
    response: str = Field(description="Concise response to the user")
    user_mood: str = Field(description="User mood: positive, neutral, negative, curious, frustrated, confused")
    suggested_questions: List[str] = Field(description="List of suggested follow-up questions")
    debug: DebugInfo
    matched_categories: Optional[List[str]] = Field(description="List of matched category IDs")
    redirect_to_agent: Optional[RedirectToAgent]

class SupportState(TypedDict):
    messages: List[dict] # Chat history
    context: str         # Retrieved context
    response: Optional[ResponseSchema] # Structured response
