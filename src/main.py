from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv(".env") # Load environment variables from .env file
from helpers.config import get_settings
from .stores.LLMProviderFactory import LLMProviderFactory


app = FastAPI()
#dicrator
async def startup_db_client():
    settings= get_settings()
    
    app.mongo_conn=AsyncIOMotorClient(settings.MONGO_URI)
    app.db_client=app.mongo_conn[settings.MONGO_DB_NAME]
    
    llm_provider_factory=LLMProviderFactory(settings)
    app.generation_client=llm_provider_factory.create(provider_name=settings.GENARTION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    app.embedding_client=llm_provider_factory.create(provider_name=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBDDING_MODEL_SIZE)
async def shutdown_db_client():
    app.mongo_conn.close()
app.router.lifespan.on_start_up.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)
app.include_router(base.base_router)
app.include_router(data.data_router)
