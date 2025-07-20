from agents import InputGuardrail, Agent

from workers.researcher import researcher
from workers.artist import artist
from workers.writer import writer
from workers.prompt_generator import prompt_generator
from guardrails.politic_guard import politic_guardrail
from utils.config import config

# management agents
router_agent = Agent(
    name="Router Agent",
    model=config.MINI_MODEL,
    instructions="""You are a smart router that determines which agent or workflow to use based on the user's request.

Available agents:
- researcher: For web research and information gathering
- artist: For image generation tasks
- writer: For story, article, or text writing tasks
- prompt_generator: For creating optimized prompts

For complex requests that need multiple agents (like "create a story and image about X"), 
route to the researcher first and mention that a full content creation workflow is needed.

For simple single-agent tasks, route directly to the appropriate specialist.""",
    handoffs=[researcher, artist, writer, prompt_generator],
    input_guardrails=[
        InputGuardrail(guardrail_function=politic_guardrail),
    ],)













