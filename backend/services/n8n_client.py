"""
n8n Webhook Client.
Calls n8n sub-workflows via internal Docker network.
"""

import httpx
import os
from typing import Any


N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook")
TIMEOUT = 120.0  # n8n agents may take time


async def call_n8n_agent(
    endpoint: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    Call an n8n webhook endpoint and return the response.
    
    Args:
        endpoint: Webhook path (e.g., 'taxai-chat', 'taxai-calculate')
        payload: JSON body to send
    
    Returns:
        Response JSON from n8n workflow
    """
    url = f"{N8N_WEBHOOK_URL}/{endpoint}"
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {
                "error": True,
                "message": "Agent timeout - vui lòng thử lại",
            }
        except httpx.HTTPStatusError as e:
            return {
                "error": True,
                "message": f"Agent error: {e.response.status_code}",
            }
        except httpx.ConnectError:
            return {
                "error": True,
                "message": "Không thể kết nối n8n service",
            }
