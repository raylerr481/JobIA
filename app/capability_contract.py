from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field

CONTRACT = "jobia-v1"

class DelegationRequest(BaseModel):
    contract: str = CONTRACT
    capability: str = "jobia"
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None
    source: str = "bitey-web"
    mode: str = "specialized"


def handle_delegation(request: DelegationRequest) -> dict[str, Any]:
    return {
        "contract": CONTRACT,
        "capability": "jobia",
        "delegated": True,
        "delegation_status": "accepted",
        "specialization": "employment-and-work",
        "message": request.message,
        "conversation_id": request.conversation_id,
        "source": request.source,
        "next_capabilities": ["opportunities", "matching", "profiles", "applications", "alerts"],
        "note": "JobIA accepted the delegated employment capability. Use its versioned employment endpoints for domain operations.",
    }
