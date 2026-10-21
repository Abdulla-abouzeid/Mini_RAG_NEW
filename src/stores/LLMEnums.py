from enum import Enum
class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
class OPENAIENUM(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"    
class COHEREENUM(Enum):
    SYSTEM="SYSTEM"
    USER="USER"
    ASSISTANT="CHATBOT"   
    DOCUMENT="search_document"
    Query="search_query"    
class DocumentType(Enum):
    DOCUMENT="document"
    Query="query"
    