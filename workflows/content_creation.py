"""
Content Creation Workflow Orchestrator

Manages the complete pipeline:
1. Research → 2. Prompt Generation → 3. Content Creation → 4. Result Aggregation
"""

import asyncio
import uuid
from datetime import datetime
from typing import Optional

from agents import Runner
from utils.models import ContentCreationResult, WorkflowMetadata, PromptGenerationResult
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
            research_result = await self._research_phase(user_prompt)
            
            # Phase 2: Generate specialized prompts
            prompt_result = await self._prompt_generation_phase(research_result, user_prompt)
            
            # Phase 3: Create content (parallel execution)
            image_result, story_result = await self._content_creation_phase(
                prompt_result.image_prompt, 
                prompt_result.story_prompt
            )
            
            # Phase 4: Aggregate results
            return self._create_final_result(
                research_result,
                prompt_result,
                image_result,
                story_result
            )
            
        except Exception as e:
            # Return error result
            return self._create_error_result(str(e))
    
    async def _research_phase(self, user_prompt: str) -> str:
        """Phase 1: Web research for relevant information."""
        research_query = f"Research and gather comprehensive information about: {user_prompt}"
        result = await Runner.run(researcher, research_query)
        return result.final_output
    
    async def _prompt_generation_phase(self, research_data: str, original_prompt: str) -> PromptGenerationResult:
        """Phase 2: Generate specialized prompts for image and story creation."""
        prompt_query = f"""
        Based on this research data about "{original_prompt}":

        {research_data}

        Generate optimized prompts for:
        1. An image that captures the key visual elements
        2. A story that incorporates the most interesting findings
        """
        
        result = await Runner.run(prompt_generator, prompt_query)
        return result.final_output_as(PromptGenerationResult)
    
    async def _content_creation_phase(self, image_prompt: str, story_prompt: str) -> tuple[str, str]:
        """Phase 3: Generate image and story in parallel."""
        
        # Run artist and writer in parallel
        artist_task = Runner.run(artist, f"Create an image: {image_prompt}")
        writer_task = Runner.run(writer, f"Write a story: {story_prompt}")
        
        artist_result, writer_result = await asyncio.gather(artist_task, writer_task)
        
        return artist_result.final_output, writer_result.final_output
    
    def _create_final_result(
        self, 
        research: str, 
        prompts: PromptGenerationResult, 
        image: str, 
        story: str
    ) -> ContentCreationResult:
        """Create the final structured result."""
        
        execution_time = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        metadata = WorkflowMetadata(
            workflow_id=self.workflow_id,
            execution_time_seconds=execution_time,
            status="completed"
        )
        
        return ContentCreationResult(
            research_summary=research,
            image_prompt=prompts.image_prompt,
            story_prompt=prompts.story_prompt,
            generated_image=image,
            generated_story=story,
            metadata=metadata
        )
    
    def _create_error_result(self, error_message: str) -> ContentCreationResult:
        """Create error result when workflow fails."""
        
        execution_time = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0 if self.start_time else 0
        
        metadata = WorkflowMetadata(
            workflow_id=self.workflow_id,
            execution_time_seconds=execution_time,
            status=f"error: {error_message}"
        )
        
        return ContentCreationResult(
            research_summary=f"Workflow failed: {error_message}",
            image_prompt="",
            story_prompt="",
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