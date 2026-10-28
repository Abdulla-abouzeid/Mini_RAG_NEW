from .LLMEnums import LLMEnums
from .llm.provider.CohereProvider import CoHereProvider
from .llm.provider.OpenAIProvider import OpenAIProvider
from helpers.config import Settings,get_settings
from fastapi import Depends
class LLMProviderFactory:
    def __init__(self, config:Settings = Depends (get_settings)):
        self.config = config
    def create(self, provider_name:str):
        if provider_name == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARCTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_CHARCTERS,
                defaut_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
            
            
        elif provider_name == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARCTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_CHARCTERS,
                defaut_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        return None
     
      
        