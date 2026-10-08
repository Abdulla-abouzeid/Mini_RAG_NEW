from pydantic import BaseModel
from typing import Optional
class PrcessRequest(BaseModel):
    file_id: str =None
    chunck_size: Optional[int] = 400
    overlap_size: Optional[int] = 20
    do_reset: Optional[int]= 0
    