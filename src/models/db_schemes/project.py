from pydantic import BaseModel, Field,validator
from typing import Optional
from bson.objectid import ObjectId
class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str =Field(...,min_length=1)
    # another valdation if fields didnt work 
    @validator('project_id')
    def vaildate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must not be alphanumeric')
        return value
    class Config:
        arbitarty_type_allowed=True
     