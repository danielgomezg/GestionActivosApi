from typing import TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class CategorySchema(BaseModel):
    description: str
    code: str
    parent_id: int

class CategoryEditSchema(BaseModel):
    description: str
    code: str
