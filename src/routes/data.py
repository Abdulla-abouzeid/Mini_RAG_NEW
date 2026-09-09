from fastapi import APIRouter,FastAPI,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controlles import DataController 
from controlles import ProjectController,ProcessController
import aiofiles 
from fastapi.responses import JSONResponse
import os
from models.enums.ResponseEnums import ResponseSignal
import logging
from .schemes.data import PrcessRequest


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
    file_path,file_id=data_obj.generate_random_filepath(
        original_filename=file.filename, project_id=project_id
        )
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
            'signal':ResponseSignal.file_uploaded_successfully.value,
            "file_id":file_id
        }
    )        
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str, request:PrcessRequest ):
    file_id=request.file_id
    chunck_size=request.chunck_size
    overlap_size=request.overlap_size
    
    ProcessController_obj=ProcessController(project_id=project_id)
    file_content=ProcessController_obj.get_file_content(file_id=file_id)
    file_chuncks=ProcessController_obj.process_file_content(
        file_id=file_id,
        file_context=file_content,
        chunk_size=chunck_size,
        overlap_size=overlap_size
    )
    if file_chuncks is None or len(file_chuncks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseSignal.Proceassing_failed.value
            }
        )
    return file_chuncks    