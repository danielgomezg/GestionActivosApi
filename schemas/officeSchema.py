from typing import TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class OfficeSchema(BaseModel):
    description: str
    floor: int
    name_in_charge: str
    sucursal_id: int

class OfficeEditSchema(BaseModel):
    description: Optional[str]
    floor: int
    name_in_charge: str


