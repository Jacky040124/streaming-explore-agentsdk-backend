"""
Content Creation Workflow Orchestrator

Manages the complete pipeline:
1. Research → 2. Prompt Generation → 3. Content Creation → 4. Result Aggregation
"""

import asyncio
import uuid
from datetime import datetime
from typing import List, Optional
import json

from agents import Runner
from utils.models import ContentCreationResult, WorkflowMetadata, PromptGenerationResult, ToolUseStatus
from utils.markdown_storage import save_workflow_result
from workers.researcher import researcher
from workers.prompt_generator import prompt_generator
from workers.artist import artist
from workers.writer import writer



class ContentCreationWorkflow:
    """Orchestrates the complete content creation pipeline."""

    def __init__(self):
        self.workflow_id = str(uuid.uuid4())
        self.start_time: Optional[datetime] = None
        self.tools_used: List[ToolUseStatus] = []
        # Store results for final output
        self.research_result: Optional[str] = None
        self.prompt_result: Optional[PromptGenerationResult] = None
        self.image_result: Optional[str] = None
        self.story_result: Optional[str] = None

    async def execute(self, user_prompt: str) -> ContentCreationResult:
        """
        Execute the complete content creation workflow.

        Args:
            user_prompt: The initial user request/prompt

        Returns:
            ContentCreationResult with all generated content and metadata
        """
        self.start_time = datetime.now()

        try:
            # Phase 1: Research
            research_result = await self._research(user_prompt)

            # Phase 2: Generate specialized prompts
            prompt_result = await self._generate_prompt(research_result, user_prompt)

            # Phase 3: Create content (parallel execution)
            image_result, story_result = await self._content_creation_phase(
                prompt_result.image_prompt,
                prompt_result.story_prompt
            )

            # Phase 4: Aggregate results
            return self._create_final_result(
                research_result,
                image_result,
                story_result
            )

        except Exception as e:
            # Return error result
            return self._create_error_result(str(e))
    
    async def execute_stream(self, user_prompt: str):
        """
        Execute workflow with streaming updates.
        Yields progress events as the workflow executes.
        """
        self.start_time = datetime.now()
        
        try:
            # Phase 1: Research
            yield {"type": "tool_update", "tool": "research_tool", "status": "started"}
            self.research_result = await self._research(user_prompt)
            yield {"type": "tool_update", "tool": "research_tool", "status": "completed"}
            
            # Phase 2: Generate specialized prompts
            yield {"type": "tool_update", "tool": "prompt_tool", "status": "started"}
            self.prompt_result = await self._generate_prompt(self.research_result, user_prompt)
            yield {"type": "tool_update", "tool": "prompt_tool", "status": "completed"}
            
            # Phase 3: Create content (parallel execution)
            yield {"type": "tool_update", "tool": "image_tool", "status": "started"}
            yield {"type": "tool_update", "tool": "story_tool", "status": "started"}
            
            self.image_result, self.story_result = await self._content_creation_phase(
                self.prompt_result.image_prompt,
                self.prompt_result.story_prompt
            )
            
            yield {"type": "tool_update", "tool": "image_tool", "status": "completed"}
            yield {"type": "tool_update", "tool": "story_tool", "status": "completed"}
            
        except Exception as e:
            yield {"type": "error", "message": str(e)}
            raise
    
    async def get_final_result(self) -> ContentCreationResult:
        """Get the final result after streaming execution."""
        if self.research_result and self.image_result and self.story_result:
            return self._create_final_result(
                self.research_result,
                self.image_result,
                self.story_result
            )
        else:
            return self._create_error_result("Workflow incomplete")

    async def _research(self, user_prompt: str) -> str:
        self.tools_used.append(ToolUseStatus(name="research_tool",complete=False))
        
        research_query = f"Research and gather comprehensive information about: {user_prompt}"
        result = await Runner.run(researcher, research_query)
        self.tools_used[-1].complete = True 
        
        return result.final_output

    async def _generate_prompt(self, research_data: str, original_prompt: str) -> PromptGenerationResult:
        prompt_query = f"""
        Based on this research data about "{original_prompt}":

        {research_data}

        Generate optimized prompts for:
        1. An image that captures the key visual elements
        2. A story that incorporates the most interesting findings
        """
        self.tools_used.append(ToolUseStatus(name="prompt_tool",complete=False))
        result = await Runner.run(prompt_generator, prompt_query)
        self.tools_used[-1].complete = True 
        
        return result.final_output_as(PromptGenerationResult)

    async def _content_creation_phase(self, image_prompt: str, story_prompt: str) -> tuple[str, str]:
        """Phase 3: Generate image and story in parallel."""
        
        self.tools_used.append(ToolUseStatus(name="image_tool",complete=False))
        self.tools_used.append(ToolUseStatus(name="story_tool",complete=False))

        # Run artist and writer in parallel (Runner is async by nature)
        artist_task = Runner.run(artist, f"Create an image: {image_prompt}")
        writer_task = Runner.run(writer, f"Write a story: {story_prompt}")
        artist_result, writer_result = await asyncio.gather(artist_task, writer_task)
        
        self.tools_used[-2].complete = True
        self.tools_used[-1].complete = True 

        return artist_result.final_output, writer_result.final_output

    def _create_final_result(
        self,
        research: str,
        image: str,
        story: str
    ) -> ContentCreationResult:
        """Create the final structured result."""

        execution_time = (
            datetime.now() - self.start_time).total_seconds() if self.start_time else 0

        metadata = WorkflowMetadata(
            workflow_id=self.workflow_id,
            execution_time_seconds=execution_time,
            status="completed",
            tool_used=self.tools_used
        )

        return ContentCreationResult(
            research_summary=research,
            generated_image=image,
            generated_story=story,
            metadata=metadata
        )

    def _create_error_result(self, error_message: str) -> ContentCreationResult:
        """Create error result when workflow fails."""

        execution_time = (datetime.now(
        ) - self.start_time).total_seconds() if self.start_time else 0 if self.start_time else 0

        metadata = WorkflowMetadata(
            workflow_id=self.workflow_id,
            execution_time_seconds=execution_time,
            status=f"error: {error_message}"
        )

        return ContentCreationResult(
            research_summary=f"Workflow failed: {error_message}",
            generated_image=None,
            generated_story=f"Error occurred: {error_message}",
            metadata=metadata
        )


# Main workflow function
async def create_content(user_prompt: str, save_to_markdown: bool = True) -> ContentCreationResult:
    """
    Main entry point for content creation workflow.

    Args:
        user_prompt: User's request for content creation
        save_to_markdown: Whether to save the result as markdown file

    Returns:
        Complete content creation result as structured JSON
    """
    workflow = ContentCreationWorkflow()
    result = await workflow.execute(user_prompt)

    # Save to markdown if requested
    if save_to_markdown and result.metadata.status == "completed":
        try:
            file_path = save_workflow_result(result)
            print(f"\n=== Result saved to: {file_path} ===")
        except Exception as e:
            print(f"Warning: Failed to save markdown: {e}")

    return result

async def create_content_stream_generator(user_prompt: str, save_markdown: bool):
    """Generate SSE events for workflow progress"""
    workflow = ContentCreationWorkflow()
    
    try:
        # Stream progress events
        async for event in workflow.execute_stream(user_prompt):
            # Format as SSE
            yield f"data: {json.dumps(event)}\n\n"
        
        # Get final result
        result = await workflow.get_final_result()
        
        # Save to markdown if requested and successful
        if save_markdown and result.metadata.status == "completed":
            try:
                file_path = save_workflow_result(result)
                print(f"\n=== Result saved to: {file_path} ===")
            except Exception as e:
                print(f"Warning: Failed to save markdown: {e}")
        
        # Send final result - use model_dump with mode='json' to handle datetime serialization
        try:
            result_dict = result.model_dump(mode='json')
            yield f"data: {json.dumps({'type': 'complete', 'result': result_dict})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'Failed to serialize result: {str(e)}'})}\n\n"
            
    except Exception as e:
        # Handle any unexpected errors during streaming
        print(f"Streaming error: {e}")
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"