
from abc import ABC, abstractmethod
class LLMInterfae(ABC):
    @abstractmethod
    def set_gentertion_model(self,model_id: str):
        pass
    @abstractmethod
    def set_embedding_model(self,model_id: str,embedding_size:int):
        pass
    @abstractmethod
    def generate_text(self,prompt:str,max_output_token:int=None,chat_history:list =[] ,temparture: float =None,):
        pass
    @abstractmethod
    def embed_text(self,document_typr:str):
        pass
    @abstractmethod
    def construct_prompt(self,prompt:str,role:str):
        pass