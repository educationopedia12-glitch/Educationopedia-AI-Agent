import hmac

from fastapi import Header
from app.config import RAG_SYNC_SECRET

from typing import Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.change_detection import has_rag_relevant_changes
from app.rag.sync import delete_university, sync_university


router = APIRouter(
    prefix="/internal/rag",
    tags=["Internal RAG"],
)


class RagSyncRequest(BaseModel):
    event_type: Literal["create", "update", "delete"]

    before: Optional[dict] = None
    after: Optional[dict] = None
    university_id: Optional[str] = None


@router.post("/sync")
def sync_rag(
    request: RagSyncRequest,
    x_internal_secret: str | None = Header(default=None),
):
    if not RAG_SYNC_SECRET:
        raise HTTPException(
            status_code=500,
            detail="RAG sync secret is not configured.",
        )

    if not x_internal_secret or not hmac.compare_digest(
        x_internal_secret,
        RAG_SYNC_SECRET,
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized.",
        )
    try:
        if request.event_type == "create":
            if not request.after:
                raise HTTPException(
                    status_code=400,
                    detail="'after' university data is required for create.",
                )

            sync_university(request.after)

            return {
                "success": True,
                "action": "created",
            }

        if request.event_type == "update":
            if not request.before or not request.after:
                raise HTTPException(
                    status_code=400,
                    detail="'before' and 'after' data are required for update.",
                )

            if not has_rag_relevant_changes(
                request.before,
                request.after,
            ):
                return {
                    "success": True,
                    "action": "skipped",
                    "reason": "No RAG-relevant fields changed.",
                }

            sync_university(request.after)

            return {
                "success": True,
                "action": "updated",
            }

        if request.event_type == "delete":
            university_id = (
                request.university_id
                or (request.before or {}).get("id")
            )

            if not university_id:
                raise HTTPException(
                    status_code=400,
                    detail="University ID is required for delete.",
                )

            delete_university(university_id)

            return {
                "success": True,
                "action": "deleted",
            }

        raise HTTPException(
            status_code=400,
            detail="Unsupported event type.",
        )

    except HTTPException:
        raise

    except Exception as error:
        print(f"RAG sync failed: {error}")

        raise HTTPException(
            status_code=500,
            detail="RAG synchronization failed.",
        )