from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnum import VectorDBEnum,DistanceMethodEnum
from qdrant_client import QdrantClient,models
import logging 
from typing import List
class QdrantDBProvider(VectorDBInterface):
    def __init__(self,db_path:str,distance_method:str):
        super().__init__()
        self.db_path=db_path
        self.client=None
        self.distance_method=None
        
        if distance_method==DistanceMethodEnum.COSINE.value:
            self.distance_method=models.Distance.COSINE
        elif distance_method==DistanceMethodEnum.DOT.value:    
            self.distance_method=models.Distance.DOT
        
        self.logger=logging.getLogger(__name__) #take name of file as logger name
        
    def connect(self):
        self.client= QdrantClient(path=self.db_path)   
    def disconnect(self):
        self.client=None
        # raise NotImplementedError
    def is_collection_exists(self,collection_name:str)->bool: 
        return self.client.collection_exists(collection_name=collection_name)    
    def delete_collection(self, collection_name):
        if self.client.collection_exists(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        else:
            raise ValueError(f"{collection_name} dont exisits cannot be deleted")
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name):
        return self.client.get_collection(collection_name=collection_name)
    def create_collection(self, collection_name, embedding_size, do_reset = False):
        if do_reset:
            _=self.delete_collection(collection_name=collection_name)
        if not self.is_collection_exists(collection_name=collection_name):  
        
          _ =self.client.create_collection(
              collection_name=collection_name,
             vectors_config=models.VectorParams(size=embedding_size,distance=self.distance_method)
             )
          return True
        return False
    
    
    
    def insert_one(self, collection_name, text, vector, metadata=None, record_id = None):
        if not self.is_collection_exists(collection_name=collection_name): 
            self.logger.error(f"cannot insert new record beacuse {collection_name} not existed")
            return False
        
        try:
                _=self.client.upsert(collection_name=collection_name,points=[models.PointStruct(
                    id=record_id,
                    payload={
                        "text":text,
                        "metadata":metadata
                        },
                    vector=vector
                )])
        except Exception as e:
            self.logger.error(f"error while inseting {e}")  
            return False      
        return True
    
    
    
    
    
    
    
    def insert_many(self, collection_name:str, texts:List, vectors, metadatas = None, record_ids = None, batch_size:int = 50) -> bool:
        if metadatas==None:
            metadatas=[None]*len(texts)
        
        if record_ids==None:
            record_ids=[None]*len(texts)
        for i in range(0,len(texts),50):
            batch_end=i+batch_size
            batch_text=texts[i:batch_end]
            batch_vector=vectors[i:batch_end]
            batch_metadata=metadatas[i:batch_end]
            batch_record=[
                models.PointStruct(
                  
            payload={
                "text":batch_text[x],
                "metadata":batch_metadata[x]
                },
            vector=batch_vector[x]
        )
                
                for x in range(len(batch_text))
            ]    
            try:
              _=self.client.upsert(
                collection_name=collection_name,
                points=batch_record
              )
              
            except Exception as e:
                self.logger.error(f"err wile enserting batch{e}")
                return False
        return True    
    def search_by_vector(self, collection_name:str, vector_query:List, limit:int = 5):
        return self.client.query_points(
            collection_name=collection_name,
            query=vector_query,
            limit=limit
            
        )    
            
        
            
        
         


           
           
