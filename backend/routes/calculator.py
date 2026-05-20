"""
Calculator route - Agent 2: Tax Calculator
Receives salary/income params, forwards to n8n calculator agent.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import time

from services.n8n_client import call_n8n_agent

router = APIRouter()


class CalculateRequest(BaseModel):
    gross_salary: Optional[float] = None
    num_dependents: int = 0
    region: str = "I"  # I, II, III, IV
    income_type: str = "salary"  # salary, business, mixed
    revenue: Optional[float] = None  # for business type
    business_sector: Optional[str] = None
    message: Optional[str] = None  # free-form question


class CalculateResponse(BaseModel):
    calculation_steps: list[dict]
    total_tax: float
    effective_rate: float
    comparison_2025: Optional[dict] = None
    disclaimer: str = "⚠️ Kết quả chỉ mang tính tham khảo. Đối soát lại bằng Excel hoặc eTax."
    processing_time_ms: int


@router.post("/calculate")
async def calculate(request: CalculateRequest):
    """
    Tax calculation endpoint.
    Can receive structured params OR free-form message (parsed by AI).
    """
    start_time = time.time()

    payload = request.model_dump()
    result = await call_n8n_agent("taxai-calculate", payload)

    processing_time = int((time.time() - start_time) * 1000)

    if result.get("error"):
        return {
            "error": True,
            "message": result.get("message", "Có lỗi xảy ra"),
            "processing_time_ms": processing_time,
        }

    result["processing_time_ms"] = processing_time
    return result
