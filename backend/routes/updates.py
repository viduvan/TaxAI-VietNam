"""
Updates route - Agent 4: Law Update / Crawler
Manages law updates feed, upload, and crawler triggers.
"""

from fastapi import APIRouter, UploadFile, File
from typing import Optional
import time

from services.n8n_client import call_n8n_agent
from services.database import async_session

router = APIRouter()


@router.get("/updates")
async def get_updates(
    impact_level: Optional[str] = None,
    limit: int = 20,
):
    """Get recent law updates from the crawler."""
    try:
        async with async_session() as session:
            query = "SELECT * FROM law_updates ORDER BY crawled_at DESC LIMIT :limit"
            params = {"limit": limit}

            if impact_level:
                query = """SELECT * FROM law_updates 
                          WHERE impact_level = :level 
                          ORDER BY crawled_at DESC LIMIT :limit"""
                params["level"] = impact_level

            result = await session.execute(query, params)
            rows = result.fetchall()

            return {
                "updates": [dict(row._mapping) for row in rows],
                "total": len(rows),
            }
    except Exception as e:
        return {"error": True, "message": str(e)}


@router.get("/notifications")
async def get_notifications(unread_only: bool = True):
    """Get notifications about high-impact law changes."""
    try:
        async with async_session() as session:
            if unread_only:
                query = "SELECT * FROM notifications WHERE is_read = FALSE ORDER BY created_at DESC"
            else:
                query = "SELECT * FROM notifications ORDER BY created_at DESC LIMIT 50"

            result = await session.execute(query)
            rows = result.fetchall()

            return {
                "notifications": [dict(row._mapping) for row in rows],
                "unread_count": len(rows) if unread_only else None,
            }
    except Exception as e:
        return {"error": True, "message": str(e)}


@router.post("/update/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new legal document for AI analysis."""
    start_time = time.time()

    content = await file.read()
    text = content.decode("utf-8")

    result = await call_n8n_agent("taxai-update", {
        "trigger": "manual_upload",
        "filename": file.filename,
        "content": text,
    })

    result["processing_time_ms"] = int((time.time() - start_time) * 1000)
    return result


@router.post("/update/crawl")
async def trigger_crawl():
    """Manually trigger the law crawler agent."""
    start_time = time.time()

    result = await call_n8n_agent("taxai-update", {
        "trigger": "manual_crawl",
    })

    result["processing_time_ms"] = int((time.time() - start_time) * 1000)
    return result
