import asyncio
import json
from agents import Runner
from agents.exceptions import InputGuardrailTripwireTriggered

from managers.router import router_agent
from workflows import create_content
from utils.config import config


async def test_simple_routing():
    """Test basic agent routing functionality."""
    try:
        result = await Runner.run(router_agent, "search the web and tell me about apple")
        print("=== Simple Routing Test ===")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail blocked this input:", e)


async def test_content_workflow():
    """Test the complete content creation workflow."""
    try:
        print("\n=== Content Creation Workflow Test ===")
        print("Starting workflow: Create content about space exploration...")
        
        result = await create_content("space exploration and Mars missions")
        
        # Print formatted JSON result
        print("\n=== Workflow Result ===")
        print(json.dumps(result.model_dump(), indent=2, default=str))
        
    except Exception as e:
        print(f"Workflow error: {e}")


async def main():
    """Main function to test both routing and workflow."""
    # Test simple routing
    # await test_simple_routing()
    
    # Test full content creation workflow
    await test_content_workflow()

if __name__ == "__main__":
    asyncio.run(main())