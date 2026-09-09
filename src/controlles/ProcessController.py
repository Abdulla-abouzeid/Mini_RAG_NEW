from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import PyMuPDFLoader,TextLoader
from models.enums.ResponseEnums import ResponseSignal
from models.enums.ProcesingEnums import ProcessingStatusEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_id(project_id=project_id)
        
        
        
        
    def get_file_extentsion(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    
    
    
    
    def get_file_loader(self,file_id:str):
        file_ext=self.get_file_extentsion(file_id=file_id)
        file_path=os.path.join(self.project_path,file_id)
        if file_ext==ProcessingStatusEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_ext==ProcessingStatusEnum.TXT.value:
            return TextLoader(file_path)
        else:
            return ResponseSignal.File_type_not_allowed
        
        
        
        
        
    def get_file_content(self,file_id:str):
        file_loader=self.get_file_loader(file_id=file_id)
        return file_loader.load()
    
    
    
    
    
    
    
    
    def process_file_content(self,file_id:str,file_context:list,chunk_size: int=100 ,overlap_size: int=20):
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        file_content_text=[
            rec.page_content
            for rec in file_context
        ]
        file_content_metadata=[
            rec.metadata
            for rec in file_context
        ]
        chuncks=text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
            
        )
        return chuncks
        