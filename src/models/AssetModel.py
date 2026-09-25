from .BaseDataModel import BaseDataModel
from .db_schemes.assets import Asset
from .enums.DatabaseEnums import DataBaseEnum
from bson import ObjectId
class AssetModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.Collection_ASSET_Name.value]
    @classmethod
    async def create_instance(cls,db_client:object):
            instance=cls(db_client)
            await instance.init_collection_chunck() 
            return instance  
    async def init_collection_chunck(self):
            all_collection=await self.db_client.list_collection_names()
            if DataBaseEnum.Collection_ASSET_Name.value not in all_collection:
                 self.collection=self.db_client[DataBaseEnum.Collection_ASSET_Name.value]
            indexs= Asset.get_index()  
            for index in indexs:
                await self.collection.create_index(
                                    index['key'],
                                    name=index['name'],
                                    unique=index['uniqe']
                                )
                
    async def create_asset(self,assit:Asset):
        result=await self.collection.insert_one(assit.dict(by_alias=True,exclude_unset=True))
        assit.id=result.inserted_id
        return assit 
    async def get_all_projects(self,asset_project_id:str):
        return await self.collection.find({
            "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id
        }).to_list(length=None )        