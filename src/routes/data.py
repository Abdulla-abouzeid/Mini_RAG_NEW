from fastapi import APIRouter,FastAPI,Depends,Upload_File,File
from helpers.config import get_settings ,Settings
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["version1", "data"]
    
)

@data_router.get("/upload/{project_id}")
async def upload_data(project_id: str,file : Upload_File, app_settings : Settings = Depends (get_settings)):    
    
    
