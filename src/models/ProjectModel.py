from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DatabaseEnums import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.Collection_Project_Name.value]
    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance
            
        
        
        
    async def init_collection(self):
        all_collection=await self.db_client.list_collection_names()
        if DataBaseEnum.Collection_Project_Name.value not in all_collection:
            self.collection=self.db_client[DataBaseEnum.Collection_Project_Name.value]
            indexs = Project.get_index()
            for index in indexs:
                await self.collection.create_index(
                    index['key'],
                    name=index['name'],
                    unique=index['uniqe']
                )
    async def create_Project(self,project : Project):
        result= await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))    
        project.id=result.inserted_id
        return project
    async def get_project_id_or_create_one(self,project_id:str):
        record=await self.collection.find_one(
            {
                "project_id":project_id
            }
        )
        if record is None:
            project=Project(project_id=project_id)
            project = await self.create_Project(project=project)
            return project
        return Project(**record)  # to convert dict to ProjectModel
    async def get_all_projects(self,page:int=1,page_size: int =10):
         tota_documents=await self.collection.count_documents({})
         total_pages=tota_documents // page_size
         if total_pages %page_size>0:
             total_pages+=1
         cursor=self.collection.find().skip((page-1)*page_size).limit(page_size)    
         projects=[]
         for document in cursor:
             projects.append(
                 Project(**document)
             )
         return  projects,total_pages