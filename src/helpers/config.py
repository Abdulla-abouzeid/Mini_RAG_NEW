from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION:str
    OPEN_AI_API_KEY:str
    File_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE : int  # 512 KB
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
      
def get_settings():
    return Settings()      