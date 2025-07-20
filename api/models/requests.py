from pydantic import BaseModel, Field
from typing import Optional


class WorkflowRequest(BaseModel):
    """Request model for content creation workflow"""
    prompt: str = Field(..., min_length=1,
                        description="The prompt for content creation")
    save_markdown: bool = Field(
        default=True, description="Whether to save result as markdown")


class WorkflowStatusResponse(BaseModel):
    """Response for workflow status"""
    status: str
    message: str
    workflow_id: Optional[str] = None
    markdown_path: Optional[str] = None
