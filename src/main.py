from fastapi import FastAPI
from routes import base
from dotenv import load_dotenv
load_dotenv(".env") # Load environment variables from .env file

app = FastAPI()
#dicrator
app.include_router(base.base_router)
    