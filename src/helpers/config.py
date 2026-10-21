from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION:str
    OPEN_AI_API_KEY:str
    File_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE : int  # 512 KB
    MONGO_URI: str
    MONGO_DB_NAME: str
    
    GENARTION_BACKEND:str
    EMBEDDING_BACKEND:str

    OPENAI_API_KEY:str=None
    OPENAI_API_URL:str=None 
    COHERE_API_KEY:str=None
    GENERATION_MODEL_ID:str=None
    EMBEDDING_MODEL_ID:str=None
    EMBDDING_MODEL_SIZE:int=None
    INPUT_DEFAULT_MAX_CHARCTERS:int=None
    GENERATION_DEFAULT_MAX_CHARCTERS:int=None
    GENERATION_DEFAULT_TEMPERATURE:float=None
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
      
def get_settings():
    return Settings()      