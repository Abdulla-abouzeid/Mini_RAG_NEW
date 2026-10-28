from .BaseController import BaseController
from models.db_schemes import Project,DataChunck
from stores.LLMEnums import DocumentType
from typing import List

class NLPController(BaseController):
    def __init__(self,generation_client,embedding_client,vectordb_client):
        super().__init__()
        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client=embedding_client
    def create_collection_name(self,project_id):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        self.vectordb_client.delete_collection(collection_name=collection_name)
        
        
    def get_vector_db_collection(self,project:Project):
            collection_name=self.create_collection_name(project_id=project.project_id)
            collection_info=self.vectordb_client.get_collection_info(collection_name=collection_name)
            return collection_info
    def index_vector_db_collection(self,project:Project,chunks:List[DataChunck],do_reset:bool = False):
        
        # get collection name 
        collection_name=self.create_collection_name(project_id=project.project_id)
        # mange items 
        texts=[c.chunk_text for c in chunks]
        metadatas=[c.chunk_metadata for c in chunks]
        vectors=[ self.embedding_client.embed_text(
            text=text,document_type=DocumentType.DOCUMENT.value)
                 for text in texts
                 ]
        # CREATE COLLECTION 
        _=self.vectordb_client.create_collection(
            collection_nameLstr=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )
        
        # insert into vectordb
        _=self.vectordb_client.create_collection(
                    collection_name=collection_name,
                    texts=texts,
                    vectors=vectors,
                    metadatas=metadatas                    
                )
        return True
        
        
        
        
        
        

        
        
        
    


        
            
        
        