"""
Chat route - Agent 1: QA Agent
Receives user questions, forwards to n8n orchestrator.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import uuid
import time

from services.n8n_client import call_n8n_agent
from services.database import get_session, async_session

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    agent: str
    sources: Optional[list[str]] = None
    warning: Optional[str] = None
    disclaimer: str = "⚠️ Thông tin chỉ mang tính tham khảo, KHÔNG thay thế tư vấn thuế chuyên nghiệp."
    session_id: str
    processing_time_ms: int


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Routes to n8n orchestrator which
    classifies intent and dispatches to the appropriate agent.
    """
    session_id = request.session_id or str(uuid.uuid4())
    start_time = time.time()

    # Call n8n orchestrator
    result = await call_n8n_agent("taxai-chat", {
        "message": request.message,
        "session_id": session_id,
    })

    processing_time = int((time.time() - start_time) * 1000)

    # Handle error from n8n
    if result.get("error"):
        return ChatResponse(
            answer=result.get("message", "Có lỗi xảy ra, vui lòng thử lại."),
            agent="error",
            session_id=session_id,
            processing_time_ms=processing_time,
        )

    # Log conversation to database
    try:
        async with async_session() as session:
            await session.execute(
                """INSERT INTO conversations 
                   (session_id, agent_type, user_message, agent_response, sources_cited, processing_time_ms)
                   VALUES (:sid, :agent, :msg, :resp, :sources::jsonb, :time)""",
                {
                    "sid": session_id,
                    "agent": result.get("agent", "qa"),
                    "msg": request.message,
                    "resp": result.get("answer", ""),
                    "sources": str(result.get("sources", [])),
                    "time": processing_time,
                },
            )
            await session.commit()
    except Exception:
        pass  # Don't fail the request if logging fails

    return ChatResponse(
        answer=result.get("answer", "Xin lỗi, tôi không thể trả lời câu hỏi này."),
        agent=result.get("agent", "qa"),
        sources=result.get("sources"),
        warning=result.get("warning"),
        session_id=session_id,
        processing_time_ms=processing_time,
    )
