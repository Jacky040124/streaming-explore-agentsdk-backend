from datetime import datetime
from agents import function_tool

@function_tool
def get_date() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")