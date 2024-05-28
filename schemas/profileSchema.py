from typing import TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ProfileSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

class ProfileEditSchema(BaseModel):
    name: str
    description: str

