from __future__ import annotations

from pydantic import BaseModel, Field

CONTRACT = "jobia-v1"


class RequestContext(BaseModel):
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


def validate_context(request: DelegationRequest) -> None:
    """Fail closed on malformed cross-module identity context."""
    context = request.context
    if context.module != "jobia":
        raise ValueError("invalid module context")
    if not context.user_id.strip() or not context.tenant_id.strip() or not context.session_id.strip():
        raise ValueError("incomplete authorization context")


def handle_delegation(request: DelegationRequest) -> dict:
    validate_context(request)
    return {
        "contract": CONTRACT,
        "capability": request.capability,
        "mode": request.mode,
        "message": request.message,
        "context": request.context.model_dump(),
        "next_capabilities": ["opportunities", "matching", "applications"],
    }
