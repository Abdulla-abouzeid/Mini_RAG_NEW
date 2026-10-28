from .providerDB import QdrantDBProvider
from helpers.config import Settings,get_settings
from .VectorDBEnum import VectorDBEnum,DistanceMethodEnum
from fastapi import Depends
from controlles.BaseController import BaseController

class VectorDBProviderFactory:
    def __init__(self,config:Settings =Depends(get_settings)):
        self.config=config
        self.base_controller=BaseController()
    def create(self,provider_name:str):
        if provider_name==VectorDBEnum.QDRANT.value:
            db_path=self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_METHOD
            )
        return None         