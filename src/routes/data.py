from fastapi import APIRouter,FastAPI,Depends,UploadFile,status,Request     
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
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunck
from models.ChunkModel import ChunkModel

logger=logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["version1", "data"]
    
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request, project_id: str,file : UploadFile, app_settings : Settings = Depends (get_settings)):
    
    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    project= await project_model.get_project_id_or_create_one(project_id=project_id)
    
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
            "file_id":file_id,
            "project_id": str(project.id)
        }
    )    
    
    
    
    
    
        
@data_router.post("/process/{project_id}")
async def process_endpoint(request_app:Request,project_id:str, request:PrcessRequest ):
    file_id=request.file_id
    chunck_size=request.chunck_size
    overlap_size=request.overlap_size
    do_reset=request.do_reset
    
    
    project_model=ProjectModel(db_client=request_app.app.db_client)
    project= await project_model.get_project_id_or_create_one(project_id=project_id)
    
    
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

    File_chunk_models=[
        DataChunck(
                chunk_text=chunk.page_content,
            
                chunk_metadata= chunk.metadata,
            
                chunk_order= i+1,
            
                chunk_project_id= project.id
            
            
        )
        for i,chunk in enumerate(file_chuncks)   
    ]    
    chunk_model= await ChunkModel.create_instance(
                db_client=request_app.app.db_client
            )    
    if do_reset==1:
           _=await chunk_model.delete_chunks_By_Projectid(
               project_id=project.id
               )
    
    no_records= await chunk_model.insert_many_chunks(chunks=File_chunk_models)
    return JSONResponse(
        content={
            "signal":ResponseSignal.Proceassing_successfully.value,
            "Inserted_Chunks":no_records
        }
        
    )