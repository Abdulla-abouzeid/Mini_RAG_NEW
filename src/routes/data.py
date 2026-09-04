from fastapi import APIRouter,FastAPI,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controlles import DataController 
from controlles import ProjectController
import aiofiles 
from fastapi.responses import JSONResponse
import os
from models.enums.ResponseEnums import ResponseSignal
import logging
logger=logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["version1", "data"]
    
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file : UploadFile, app_settings : Settings = Depends (get_settings)):
    #Validate file type and size
    data_obj=DataController()
    is_vaild,message=data_obj.validate_file(file=file)
    if not is_vaild:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':message
            }
        )
      
    # return {
    #      "is_valid": is_vaild,
    #       "message": message
    #     }
    project_dirc=ProjectController().get_project_id(project_id=project_id)
    file_path=data_obj.generate_random_filename(original_filename=file.filename, project_id=project_id)
    try:   
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
    except Exception as e:
        logger.error(f"error beacuse of file saving")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'signal':ResponseSignal.file_upload_failed.value,
                
            }
        )                
    return JSONResponse(
        
        content={
            'signal':ResponseSignal.file_uploaded_successfully.value
        }
    )        
