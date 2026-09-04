from .BaseController import BaseController
from fastapi import UploadFile
from models.enums.ResponseEnums import ResponseSignal
from .ProjectController import ProjectController
import re,os
class DataController(BaseController): #inherit from base controller
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 # to convert file max size to bytes 
        
        
    def validate_file(self, file: UploadFile):    
        if file.content_type not in self.app_settings.File_ALLOWED_TYPES:
            return False, ResponseSignal.File_type_not_allowed.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.File_size_exceeds_maximum.value
        return True , ResponseSignal.file_uploaded_successfully.value
    
    
    
    
    def generate_random_filename(self, original_filename: str, project_id: str) -> str:
        """Generate a random filename based on the original filename."""
        random_string = self.generate_random_string()
        project_path=ProjectController().get_project_id(project_id=project_id)
        cleaned_filename = self.get_clean_filename(original_filename)
        new_file_path=os.path.join(project_path, f"{random_string}_{cleaned_filename}")
        while os.path.exists(new_file_path):
            random_string = self.generate_random_string()
            new_file_path=os.path.join(project_path, f"{random_string}_{cleaned_filename}")
        return new_file_path    
        
    def get_clean_filename(self, original_filename: str) :
        """Generate a clean filename by removing special characters."""
        cleaned_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', original_filename)
        return cleaned_filename
        
        
    