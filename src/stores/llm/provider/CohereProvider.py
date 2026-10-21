from .. .LLMinterface import LLMInterface
from .. .LLMEnums import COHEREENUM,DocumentType
import cohere
import logging

class CoHereProvider(LLMInterface):
    def __init__(self,api_key:str=None ,default_input_max_characters:int=1000,
                 default_generation_max_output_tokens:int=1000,
                 defaut_temperature:float=0.1):    
                self.api_key=api_key,
        
                self.default_input_max_characters=default_input_max_characters,
                self.default_generation_max_output_tokens=default_generation_max_output_tokens,
                self.default_temperature=defaut_temperature
                self.generation_model_id=None
                self.embedding_model_id=None
                self.embedding_size=None #for vetor database
                self.client=co = cohere.ClientV2(api_key=self.api_key)

                self.logger=logging.getLogger(__name__) #take name of file as logger name
                
                
    def set_generation_model(self,model_id:str):
            self.generation_model_id=model_id
            
            
            
    def set_embedding_model(self,model_id:str,embedding_size:int):
            self.embedding_model_id=model_id
            self.embedding_size=embedding_size
                        
    def process_text(self,text:str):
            return text[:self.default_input_max_characters].strip()    
       
       
    def construct_prompt(self,prompt:str,role:str):
            return{
                "role" : role,
                "text": self.process_text(prompt)
            }   
            
    def embed_text(self,text:str,document_type:str=None):
                if not self.client:
                        self.logger.error(" Cohere client is not initialized. Please provide a valid API key and URL.")
                        return None
                if not self.embedding_model_id:
                        self.logger.error("Embedding model is not set. Please set the embedding model before calling embed_text.")
                        return None
                input_type=COHEREENUM.DOCUMENT
                if document_type==DocumentType.Query:
                    input_type=COHEREENUM.Query
                response=self.client.embed(
                        model=self.embedding_model_id,
                        texts=[self.process_text(text)],
                        input_type=input_type.value,
                        embedding_type=['float']
                )     
                if not response or not response.embeddings or not response.embeddings.float  :
                    self.logger.error("No embedding received from the Cohere API.")
                    return None
                else:
                    return response.embeddings.float[0]
                
                     
    def generate_text(self,prompt:str,max_output_token:int=None,chat_history:list =[] ,temparture: float =None,):
            if not self.client:
                    self.logger.error(" OpenAI client is not initialized. Please provide a valid API key and URL.")
                    return None
            if not self.generation_model_id:
                    self.logger.error("Generation model is not set. Please set the generation model before calling generate_text.")
                    return None
            max_output_token=max_output_token if max_output_token else self.default_generation_max_output_tokens
            temparture=temparture if temparture else self.default_temperature    
            response=self.client.chat(
                model=self.generation_model_id,
                chat_history=chat_history,
                message=self.process_text(prompt),
                max_tokens=max_output_token,
                temperature=temparture
                
            )
            if not response or not response.text:
                self.logger.error("No response received from the Cohere API.")
                return None
            else:
                return response.text
            
                
                        
                        