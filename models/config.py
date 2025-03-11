"""
Configuration for LLM models and endpoints
"""

import streamlit as st
from enum import Enum
from typing import Dict, Any
# from dotenv import load_dotenv

# # Load environment variables from .env.local
# env_path = Path(__file__).parent.parent / 'env' / '.env.local'
# load_dotenv(env_path)

class ModelProvider(Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"

class ModelConfig:
    # Default configurations
    DEFAULT_PROVIDER = ModelProvider.OPENAI
    DEFAULT_MODEL = "gpt-4o"
    DEFAULT_TEMPERATURE = 0.3
    
    # Model mappings
    AVAILABLE_MODELS = {
        ModelProvider.OPENAI: [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4"
        ],
        ModelProvider.GOOGLE: [
            "gemini-pro",
            "gemini-pro-vision",
        ],
        ModelProvider.ANTHROPIC: [
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-2.1",
        ]
    }
    
    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from Streamlit secrets"""
        config = {
            "provider": st.secrets.get("LLM_PROVIDER", ModelConfig.DEFAULT_PROVIDER.value),
            "model": st.secrets.get("LLM_MODEL", ModelConfig.DEFAULT_MODEL),
            "temperature": float(st.secrets.get("LLM_TEMPERATURE", ModelConfig.DEFAULT_TEMPERATURE)),
            "api_keys": {
                "openai": st.secrets.get("OPENAI_API_KEY", ""),
                "google": st.secrets.get("GOOGLE_API_KEY", ""),
                "anthropic": st.secrets.get("ANTHROPIC_API_KEY", ""),
            }
        }
        
        # Validate required API keys
        provider = config["provider"]
        api_key = config["api_keys"].get(provider)
        if not api_key:
            raise ValueError(f"API key for provider {provider} not found in secrets")
            
        return config

    @staticmethod
    def get_available_models(provider: ModelProvider) -> list:
        """Get available models for a provider"""
        return ModelConfig.AVAILABLE_MODELS.get(provider, []) 