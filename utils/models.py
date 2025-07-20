"""
Output models for structured workflow results.
Defines Pydantic models for consistent JSON output format.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ToolUseStatus(BaseModel):
    name: str
    complete: bool

class WorkflowMetadata(BaseModel):
    """Metadata for workflow execution."""
    timestamp: datetime = Field(default_factory=datetime.now)
    workflow_id: str 
    execution_time_seconds: Optional[float] = None
    status: str = "completed"
    tool_used: List[ToolUseStatus] = []


class ContentCreationResult(BaseModel):
    research_summary: str = Field(description="Summary of web research findings")
    generated_image: Optional[str] = Field(description="Generated image data or URL", default=None)
    generated_story: str = Field(description="Generated story content")
    metadata: WorkflowMetadata
    


class PromptGenerationResult(BaseModel):
    """Result from prompt generator agent."""
    image_prompt: str = Field(description="Detailed prompt for image generation")
    story_prompt: str = Field(description="Detailed prompt for story writing")
    source_research: str = Field(description="Research data used for prompt generation")