from pickle import NONE
from .. .LLMEnums import OPENAIENUM
from .. .LLMinterface import LLMInterface
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):
    def __init__(self,api_key:str=None,api_url:str=None,default_input_max_characters:int=1000,
                 default_generation_max_output_tokens:int=1000,
                 defaut_temperature:float=0.1):
        self.api_key=api_key,
        self.api_url=api_url,
        self.default_input_max_characters=default_input_max_characters,
        self.default_generation_max_output_tokens=default_generation_max_output_tokens,
        self.default_temperature=defaut_temperature
        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None #for vetor database
        self.client=OpenAI(
            api_key=self.api_key,
            
            )
        
        
        self.logger=logging.getLogger(__name__) #take name of file as logger name
        
        
    def set_generation_model(self,model_id:str):
        self.generation_model_id=model_id
        
        
        
    def set_embedding_model(self,model_id:str,embedding_size:int):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size
        
        
        
    def generate_text(self,prompt:str,
                      max_output_token:int = None,
                      chat_history:list =[],
                      temparture: float =None):
        if not self.client:
            self.logger.error(" OpenAI client is not initialized. Please provide a valid API key and URL.")
            return None
        if not self.generation_model_id:
            self.logger.error("Generation model is not set. Please set the generation model before calling generate_text.")
            return None
        max_output_token=max_output_token if max_output_token else self.default_generation_max_output_tokens
        temparture=temparture if temparture else self.default_temperature
        chat_history.append(
            self.construct_prompt(prompt=prompt,role=OPENAIENUM.USER.value)
        )
        response=self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_token,
            temperature=temparture
        )
        if not response or not response.choices or len(response.choices)==0 or not response.choices[0].message:
            self.logger.error("Failed to get response from OpenAI API.")
            return None
        else:
            return response.choices[0].message["content"]
    
    
    
    def embed_text(self,text:str,document_type:str):
       if not self.client:
           self.logger.error(" OpenAI client is not initialized. Please provide a valid API key and URL.")
       if not self.embedding_model_id:
           self.logger.error("Embedding model is not set. Please set the embedding model before calling embed_text.")    
                    
       respones=self.client.embeddings.create(
           model=self.embedding_model_id,
           input=text
       ) 
       if not respones or not respones.data or len(respones.data)==0 or not respones.data[0].embedding:
           self.logger.error("Failed to get embedding from OpenAI API.")
           return None
       return respones.data[0].embedding
   
   
    def process_text(self,text:str):
        return text[:self.default_input_max_characters].strip()    
   
   
    def construct_prompt(self,prompt:str,role:str):
        return{
            "role" : role,
            "content": self.process_text(prompt)
        }    
        
                
        
        
        