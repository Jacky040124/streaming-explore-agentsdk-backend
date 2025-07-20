from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

from utils.config import config

class PoliticOutput(BaseModel):
    is_politic: bool
    reasoning: str
    
# guardrail agents
politic_guardrail_agent = Agent(
    name="Guardrail check",
    model=config.MINI_MODEL,
    instructions="Check if the user is asking about politic.",
    output_type=PoliticOutput
)  
    
async def politic_guardrail(ctx, agent, input_data):
    result = await Runner.run(politic_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(PoliticOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_politic,
    )