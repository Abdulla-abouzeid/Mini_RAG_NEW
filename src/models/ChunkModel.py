from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunck
from .enums.DatabaseEnums import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.Collection_Chunck_Name.value]
    async def create_chunk(self,chunk:DataChunck):
        result=self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        chunk._id=result.inserted_id
        return chunk
    async def get_chunk(self,chunk_id:str):
        result= await self.collection.find_one(
            {
                "_id":ObjectId(chunk_id)
            }
        ) 
        if result is None:
            return None
        return DataChunck(**result)   
    async def insert_many_chunks(self,chunks:list,batch_size:int=100):
        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]
            opeations=[
                InsertOne(chunk.dict(by_alias=True,exclude_unset=True))
                for chunk in batch
            ]
            await self.collection.bulk_write(opeations)
        return len(chunks)    
    async def delete_chunks_By_Projectid(self,Project_id:ObjectId):
        result=await self.collection.delete_many({
            
            "chunk_project_id":Project_id
        }
        )
        return result.deleted_count
            