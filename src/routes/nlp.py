from fastapi import FastAPI,APIRouter,status,Request
from fastapi.responses import JSONResponse
import logging
from routes.schemes.nlp import PushRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel

from models.enums.ResponseEnums import ResponseSignal
from controlles.NLPController import NLPController
logger=logging.getLogger('uvicorn.error')


nlp_router=APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1","nlp"]
    )

@nlp_router.post("/index/push/{project_id}")

async def index_project(request:Request,project_id:str,push_rquest:PushRequest):
    project_model= await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    
    chunck_model= await ChunkModel.create_instance(
        db_client=request.app.db_client
    )
    
    project=project_model.get_project_id_or_create_one(
        project_id=project_id
    )
    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.Project_not_found_error.value
            }
        )
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )    