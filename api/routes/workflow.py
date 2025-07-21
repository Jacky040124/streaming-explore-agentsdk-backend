from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from api.models.requests import WorkflowRequest, WorkflowStatusResponse
from workflows import create_content
from utils.models import ContentCreationResult
from workflows.content_creation import create_content_stream_generator


router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("/create", response_model=ContentCreationResult)
async def create_content_endpoint(request: WorkflowRequest):
    """Create content based on user prompt"""
    try:
        result = await create_content(
            user_prompt=request.prompt,
            save_to_markdown=request.save_markdown
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-stream")
async def create_content_stream(request: WorkflowRequest):
    """Stream content creation progress via SSE"""
    return StreamingResponse(
        create_content_stream_generator(
            request.prompt,
            request.save_markdown
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )