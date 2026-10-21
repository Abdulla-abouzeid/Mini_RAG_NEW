from helpers.config import Settings, get_settings
import os 
import random
import string
class BaseController:
    def __init__(self):
        self.app_settings= get_settings()
        self.base_dirc=os.path.dirname(os.path.dirname(__file__))
        self.file_dir=os.path.join(
            self.base_dirc,
            "assets/files"
        )
        self.db_dirc=os.path.join(
            self.base_dirc,
            "assets/databases"
        )
    def generate_random_string(self, length: int = 8) -> str:
        """Generate a random string of specified length."""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))
    def get_database_path(self,db_name:str):
        db_path=os.path.join(
            self.db_dirc,db_name
        )
        if not os.path.exists(db_path):
            os.mkdir(db_path)
        return db_path    
    
    