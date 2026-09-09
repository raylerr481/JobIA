from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

CONTRACT = "jobia-v1"


class RequestContext(BaseModel):
    """Minimal routing context used to preserve identity and isolation across modules."""

    request_id: str = Field(min_length=1, max_length=128)
    user_id: str = Field(min_length=1, max_length=256)
    tenant_id: str = Field(min_length=1, max_length=256)
    module: str = "jobia"
    session_id: str = Field(min_length=1, max_length=256)
    source: str = "bitey-web"
    authorization_scope: list[str] = Field(default_factory=list)


class DelegationRequest(BaseModel):
    contract: str = CONTRACT
    capability: str = "jobia"
    message: str = Field(min_length=1, max_length=12000)
    context: RequestContext
    mode: str = "specialized"


def handle_delegation(request: DelegationRequest) -> dict[str, Any]:
    return {
        "contract": CONTRACT,
        "capability": "jobia",
        "delegated": True,
        "delegation_status": "accepted",
        "specialization": "employment-and-work",
        "message": request.message,
        "context": request.context.model_dump(),
        "next_capabilities": ["opportunities", "matching", "profiles", "applications", "alerts"],
        "note": "JobIA accepted the delegated employment capability. Use its versioned employment endpoints for domain operations.",
    }
