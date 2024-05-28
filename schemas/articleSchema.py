from typing import TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ArticleSchema(BaseModel):
    name: str = None
    description: Optional[str] = None
    code : str
    photo: Optional[str] = None
    category_id: int = None
    company_id: int = None

class ArticleEditSchema(BaseModel):
    name: str = None
    description: Optional[str] = None
    code: str
    photo: Optional[str] = None
    category_id: int = None
