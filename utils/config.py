"""
Configuration management for the agents backend.
Centralizes environment variable loading and API configurations.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for managing API keys and settings."""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Model Configuration
    DEFAULT_MODEL: str = os.getenv('DEFAULT_MODEL', 'gpt-4o')
    MINI_MODEL: str = os.getenv('MINI_MODEL', DEFAULT_MODEL)
    RESEARCHER_MODEL: str = os.getenv('RESEARCHER_MODEL', DEFAULT_MODEL)
    
    # Agent Configuration
    MAX_TOKENS: Optional[int] = int(os.getenv('MAX_TOKENS', '0')) or None
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Debug and Logging
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True
    
    @classmethod
    def get_model_config(cls, model_type: str = 'default') -> dict:
        """Get model configuration for different agent types."""
        model_configs = {
            'default': cls.DEFAULT_MODEL,
            'mini': cls.MINI_MODEL,
            'researcher': cls.RESEARCHER_MODEL,
        }
        
        return {
            'model': model_configs.get(model_type, cls.DEFAULT_MODEL),
            'temperature': cls.TEMPERATURE,
        }


# Initialize and validate configuration on import
config = Config()
config.validate()