from fastapi import FastAPI
from routes import base,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv(".env") # Load environment variables from .env file
from helpers.config import get_settings
from stores.VectorDB.VectorDBProviderFactory import VectorDBProviderFactory
from stores.LLMProviderFactory import LLMProviderFactory

app = FastAPI()
#dicrator
async def startup_span():
    settings= get_settings()
    
    app.mongo_conn=AsyncIOMotorClient(settings.MONGO_URI)
    app.db_client=app.mongo_conn[settings.MONGO_DB_NAME]
    
    llm_provider_factory=LLMProviderFactory(settings)
    vector_db_provider=VectorDBProviderFactory(settings)
    
    
    # genertion_client
    app.generation_client=llm_provider_factory.create(provider_name=settings.GENARTION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    
    # embeding_client
    app.embedding_client=llm_provider_factory.create(provider_name=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBDDING_MODEL_SIZE)
    
    #vector_db_client
    app.vectordb_client=vector_db_provider.create(
        provider_name=settings.VECTORDB_BACKEND
    )
    app.vectordb_client.connect()
    
async def shutdown_span():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()
    
    
    
    
app.add_event_handler("startup", startup_span)
app.add_event_handler("shutdown", shutdown_span)
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)