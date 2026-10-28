from typing import Optional, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.llm_service import llm_service, JobIntentSchema, ControlledTools

router = APIRouter(prefix="/llm", tags=["LLM"])

class IntentRequest(BaseModel):
    text: str = Field(..., description="User voice transcript or message text")
    execute_tools: bool = Field(False, description="Whether to also execute sandboxed tools and return matched jobs")

class IntentResponse(BaseModel):
    intent: JobIntentSchema
    tool_results: Optional[Dict[str, Any]] = None

@router.post("/intent", response_model=IntentResponse)
async def extract_intent(req: IntentRequest):
    """
    Extracts structured intent from Telugu, Hindi, or English natural speech/text.
    Strictly validates against Pydantic schema and prevents LLM fabrication.
    """
    intent = await llm_service.parse_intent(req.text)
    tool_results = None

    if req.execute_tools and intent.intent == "find_job":
        matches = ControlledTools.find_jobs(job_type=intent.job_type, location=intent.location)
        tool_results = {"matched_jobs": matches, "count": len(matches)}

    return IntentResponse(intent=intent, tool_results=tool_results)
