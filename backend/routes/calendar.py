"""
Calendar route - Agent 3: Tax Calendar
Returns deadlines, SOP steps, and checklists.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import time

from services.n8n_client import call_n8n_agent

router = APIRouter()


class CalendarRequest(BaseModel):
    user_type: Optional[str] = None  # salaried, freelancer, hkd_over_1ty, hkd_under_1ty
    message: Optional[str] = None


@router.get("/calendar")
async def get_deadlines(user_type: Optional[str] = None):
    """Get upcoming tax deadlines, optionally filtered by user type."""
    start_time = time.time()

    result = await call_n8n_agent("taxai-calendar", {
        "action": "deadlines",
        "user_type": user_type,
    })

    result["processing_time_ms"] = int((time.time() - start_time) * 1000)
    return result


@router.post("/calendar/ask")
async def ask_calendar(request: CalendarRequest):
    """Ask calendar agent a free-form question about deadlines or SOP."""
    start_time = time.time()

    result = await call_n8n_agent("taxai-calendar", {
        "action": "ask",
        "message": request.message,
        "user_type": request.user_type,
    })

    result["processing_time_ms"] = int((time.time() - start_time) * 1000)
    return result
