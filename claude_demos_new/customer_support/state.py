from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class DebugInfo(BaseModel):
    context_used: bool

class RedirectToAgent(BaseModel):
    should_redirect: bool
    reason: Optional[str] = None

class CustomerSupportResponse(BaseModel):
    thinking: str = Field(description="Brief explanation of your reasoning")
    response: str = Field(description="Response to the user")
    user_mood: Literal["positive", "neutral", "negative", "curious", "frustrated", "confused"]
    suggested_questions: List[str]
    debug: DebugInfo
    matched_categories: Optional[List[str]] = Field(default_factory=list)
    redirect_to_agent: Optional[RedirectToAgent] = None

class AgentState(BaseModel):
    messages: List[Dict[str, Any]]
    context: str = ""
    response: Optional[CustomerSupportResponse] = None
