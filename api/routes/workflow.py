from fastapi import APIRouter, HTTPException
from api.models.requests import WorkflowRequest, WorkflowStatusResponse
from utils.models import ContentCreationResult
from workflows import create_content

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


@router.get("/health", response_model=WorkflowStatusResponse)
async def health_check():
    """Check if the API is running"""
    return WorkflowStatusResponse(
        status="healthy",
        message="Content creation API is running"
    )
