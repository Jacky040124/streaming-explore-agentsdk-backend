from agents import Agent, WebSearchTool
from utils.config import config

researcher = Agent(
    name = "researcher",
    model = config.RESEARCHER_MODEL,
    handoff_description = "Deep thinker specialise in researcher in the web",
    instructions = "You are a researcher agent specializing in gathering, analyzing, and synthesizing information from the web. When given a query, conduct thorough research, evaluate sources for credibility, and provide a clear, well-structured summary of your findings. Always cite your sources and explain your reasoning behind conclusions.",
    tools = [WebSearchTool()]
)


