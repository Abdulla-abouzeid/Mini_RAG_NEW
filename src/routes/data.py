from fastapi import APIRouter,FastAPI,Depends, File,UploadFile,status,Request     
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
from models.db_schemes import DataChunck,Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum
from bson import ObjectId

logger=logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["version1", "data"]
    
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request, project_id: str,file : UploadFile = File(...), app_settings : Settings = Depends (get_settings)):
    
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
    # store asssets to database
    asset_model= await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource=Asset(
        asset_project_id=ObjectId(project.id),
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    asset_record=await asset_model.create_asset(assit=asset_resource)
            
    return JSONResponse(
        
        content={
            'signal':ResponseSignal.file_uploaded_successfully.value,
            "file_id":str(asset_record.id),
            
        }
    )    
    
    
    
    
    
        
@data_router.post("/process/{project_id}")
async def process_endpoint(request_app:Request,project_id:str, request:PrcessRequest ):
    
    chunck_size=request.chunck_size
    overlap_size=request.overlap_size
    do_reset=request.do_reset
    
    
    project_model=ProjectModel(db_client=request_app.app.db_client)
    project= await project_model.get_project_id_or_create_one(project_id=project_id)
    asset_model= await AssetModel.create_instance(db_client=request_app.app.db_client)
    project_file_ids={}
    if request.file_id :
        asset_record=await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=request.file_id
        )
        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'signal':ResponseSignal.No_files_found.value
                    
                }
            )
        project_file_ids={
            asset_record.id: asset_record.asset_name
        }
    else:
            
            project_files= await asset_model.get_all_projects(
                asset_project_id=project.id,
                asset_type=AssetTypeEnum.FILE.value
            )
            project_file_ids={
            record.id: record.asset_name 
            for record in project_files
            }
    if len(project_file_ids)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseSignal.No_files_found.value
                
            }
        )        

            
    no_records=0
    no_files=0    
    chunk_model= await ChunkModel.create_instance(
                            db_client=request_app.app.db_client
                        )
    if do_reset==1:
                    _=await chunk_model.delete_chunks_By_Projectid(
                        project_id=project.id
                        )
    
    for assit_id,file_id in project_file_ids.items():
            ProcessController_obj=ProcessController(project_id=project_id)
            file_content=ProcessController_obj.get_file_content(file_id=file_id)
            
            if file_content is None :
                logger.error(f"cannot read file content for file_id: {file_id}")
                continue
                
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
                    
                        chunk_project_id= project.id,
                        chunk_asset_id=assit_id
                    
                    
                )
                for i,chunk in enumerate(file_chuncks)   
            ]    
                
            
            
            no_records += await chunk_model.insert_many_chunks(chunks=File_chunk_models)
            no_files+=1
    return JSONResponse(
        content={
            "signal":ResponseSignal.Proceassing_successfully.value,
            "Inserted_Chunks":no_records,
            "Processed_Files":no_files
        }
        
    ) 