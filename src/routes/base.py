from fastapi import APIRouter,FastAPI,Depends
from helpers.config import get_settings
base_router = APIRouter(
    prefix="/api/v1",
    tags=["version1"]
)



@base_router.get("/")
async def welcome(settings =Depends (get_settings)):
    
    return {
        "message": "Welcome to all"
        ,"app_name": settings.APP_NAME
        ,"app_version": settings.APP_VERSION
    }
    